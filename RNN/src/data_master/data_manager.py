import logging
import os
from datetime import timedelta
from io import StringIO

import numpy
import numpy as np
import pandas as pd
import requests
import yfinance as yf

from data_master import ASSETS
from data_master.data_manipulator import DataManipulator
from data_master.file_manager import FileManager


class DataManager:

    def __init__(self, _params):
        self.params = _params
        self.file_manager = FileManager()
        self.data_manipulator = DataManipulator(_params)
        print(os.getcwd())

    """static vars"""
    ratio_of_sets = 0.1

    @staticmethod
    def split_data(_data: numpy.ndarray) -> [[np.float64]]:

        test_set_size = validation_set_size = int(np.round(DataManager.ratio_of_sets * len(_data)))
        train_set_size = len(_data) - test_set_size - validation_set_size

        train_set = _data[:train_set_size]
        validation_set = _data[train_set_size:train_set_size + validation_set_size]
        test_set = _data[train_set_size + validation_set_size:]

        return train_set, validation_set, test_set

    def get_preprocessed_dataframe(self, specific_cols=None, filename=None) -> pd.DataFrame:
        if specific_cols is None:
            df = self.read_all_columns_from_csv(filename)
        else:
            df = self.read_all_columns_from_csv(filename)[specific_cols]

        if self.is_in_wrong_order(df):
            df = df.iloc[::-1]

        return self.data_manipulator.preprocess_dataframe(df)

    def read_all_columns_from_csv(self, filename=None) -> pd.DataFrame:
        if filename is None:
            filename = self.file_manager.compose_filename_of_csv(self.params)

        df = pd.read_csv(filename)
        return df

    def get_stock_data(self, token: str):
        return self.data_manipulator.reindex_and_fillnan(
            yf.download(
                token,
                self.params.start_time,
                self.params.end_time + timedelta(1),  # default is <start date,end date)
                keepna=True,
                prepost=True
            )
        )

    def get_twitter_data(self, token: str):
        rnn_app_dockerenv = os.environ.get('RNN_APP_DOCKERENV')

        url = "http://engine:5000/scrap-tweets" if rnn_app_dockerenv else "http://127.0.0.1:5000/scrap-tweets"
        logger = logging.getLogger('main')
        logger.info(f"chosen url: {url}")
        data = {
            "asset_name": ASSETS[token],
            "token": token,
            "start_time": str(self.params.start_time),
            "end_time": str(self.params.end_time)
        }
        response = requests.post(url, json=data)

        s = str(response.content, 'utf-8')
        data = StringIO(s)
        data = pd.read_csv(data)
        return self.data_manipulator.preprocess_dataframe(data)

    @staticmethod
    def is_in_wrong_order(df: pd.DataFrame) -> bool:
        if len(df.columns) < 2:
            print(f"not enough columns [{len(df.columns)}] !")
        return df["Date"].iloc[0] > df["Date"].iloc[-1]
