import os
from pathlib import Path

from flask import Flask, request
from requestModels import ModelParams, PredictParams
from data_master import ASSETS
from nn_trainer.main_train import train_model
from predicter import predict

app = Flask(__name__)


@app.post("/train")
def train():
    data = ModelParams.parse_obj(request.json)
    return train_model(data)


@app.post("/predict")
def post_predict():
    data = PredictParams.parse_obj(request.json)
    return {"model_prediction": predict(data.model_name, data.date, data.lookback)}


@app.get("/models")
def collect_models():
    model_names = [os.path.basename(f.path) for f in os.scandir("models") if f.is_dir()]
    app.logger.info(f"model_names: {model_names}")

    return {"model_names": model_names}


@app.get("/assets")
def get_assets():
    assets_names = [os.path.basename(f.path) for f in os.scandir(Path("dataset/sentiment")) if f.is_file()]
    app.logger.info(f"assets_names: {assets_names}")
    app.logger.info(f"assets_dict: {[get_asset_dic(asset) for asset in assets_names]}")

    return {"assets_names": [get_asset_dic(asset) for asset in assets_names]}


def get_asset_dic(asset: str) -> dict:
    split = asset.split(".")[0].split("_")
    token = split[0]

    if token not in ASSETS:
        app.logger.info(f"empty")
        app.logger.info(f"ASSETS: {ASSETS}")

        return {}

    return {
        "token": token,
        "name": ASSETS[token],
        "start_time": split[1],
        "end_time": split[2]
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=4000)
