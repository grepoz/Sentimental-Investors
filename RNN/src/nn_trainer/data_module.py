from pathlib import Path

import numpy
import pandas as pd
import pytorch_lightning as pl
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader

from requestModels import ModelParams
from data_master.data_manager import DataManager
from data_master.file_manager import FileManager
from data_master.params import Params
from nn_trainer.time_series_dataset import TimeseriesDataset


class DataModule(pl.LightningDataModule):
    def __init__(self, model_params: ModelParams, data_dir: str = "./dataset"):  # TODO: make constant
        super().__init__()
        self.X_scaler = MinMaxScaler()
        self.y_scaler = MinMaxScaler()
        self.data_dir = data_dir

        self.lookback = model_params.look_back
        self.batch_size = model_params.batch_size
        self.is_with_twitter = model_params.is_twitter
        self.token = model_params.token
        params = Params(model_params.start_date, model_params.end_date)
        self.data_manager = DataManager(params)

        self.input_size = None
        self.data = None
        self.x_train, self.x_val, self.x_test = None, None, None
        self.y_train, self.y_val, self.y_test = None, None, None

    def setup(self, stage=None):
        # Assign train/val datasets for use in dataloaders
        data = [
            self.data_manager.get_stock_data(self.token)
        ]
        if self.is_with_twitter:
            data.append(self.data_manager.get_preprocessed_dataframe(
                filename=FileManager.find_full_datafile_name(
                    self.token, Path("dataset/sentiment")
                )
            )
            )
        self.data = pd.concat(data, axis=1)
        self.input_size = len(self.data.columns)
        self._split_and_transform_data()

    def train_dataloader(self):
        ds = TimeseriesDataset(self.x_train, self.y_train, seq_len=self.lookback)
        return DataLoader(ds, batch_size=self.batch_size, drop_last=True)

    def val_dataloader(self):
        ds = TimeseriesDataset(self.x_val, self.y_val, seq_len=self.lookback)
        return DataLoader(ds, batch_size=self.batch_size, drop_last=True)

    def test_dataloader(self):
        ds = TimeseriesDataset(self.x_test, self.y_test, seq_len=self.lookback)
        return DataLoader(ds, batch_size=self.batch_size)

    def predict_dataloader(self):
        ds = TimeseriesDataset(self.x_test, self.y_test, seq_len=self.lookback)
        return DataLoader(ds)

    def _split_and_transform_data(self):
        y_data = self.data["Close"]
        self.y_train, self.y_val, self.y_test = self._prepare_data(y_data.to_numpy().reshape(-1, 1), self.y_scaler)
        self.x_train, self.x_val, self.x_test = self._prepare_data(self.data.to_numpy(), self.X_scaler)

    def _prepare_data(self, data: numpy.ndarray, scaler: MinMaxScaler):
        train, val, test = self.data_manager.split_data(data)
        train = scaler.fit_transform(train)
        val = scaler.transform(val)
        test = scaler.transform(test)
        return train, val, test
