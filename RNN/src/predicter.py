import datetime
import os
from pathlib import Path

import pandas as pd
import torch

from data_master.data_manager import DataManager
from data_master.params import Params
from nn_trainer.lstm import LSTM


def predict(model_name: str, date: datetime.date = datetime.date.today(), lookback=None) -> float:
    model = get_best_model(model_name)
    if lookback is None:
        lookback = model.lookback
    data_manager = DataManager(Params(date - datetime.timedelta(lookback - 1), date))
    data = prepare_data(model, data_manager)

    model.eval()
    with torch.no_grad():
        pred = model(data)
        pred = model.y_scaler.inverse_transform(pred)
    return float(pred.squeeze())


def get_best_model(model_name: str) -> LSTM:
    models_path = Path("models") / model_name
    try:
        check_points_names = [os.path.basename(f.path) for f in os.scandir(models_path) if f.is_file()]
    except BaseException as e:
        print(e)
        raise e
    val_loss_to_name = {get_val_loss(name): name for name in check_points_names}
    best_val_loss = min(val_loss_to_name.keys())
    model = LSTM.load_from_checkpoint(f"{models_path}/{val_loss_to_name[best_val_loss]}")
    return model


def get_val_loss(name: str) -> float:
    val_loss_str = "val_loss="
    index = name.find(val_loss_str)
    index += len(val_loss_str)  # jump over val_loss_str
    val_loss = float(name[index:].split("-")[0])
    return val_loss


def prepare_data(model, data_manager: DataManager):
    data = [data_manager.get_stock_data(model.token)]
    if model.is_twitter:
        data.append(data_manager.get_twitter_data(model.token))
    data = pd.concat(data, axis=1)
    data = torch.tensor(model.x_scaler.transform(data)).float()
    return data.expand(1, -1, -1)
