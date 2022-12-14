import copy

import pytorch_lightning as pl
import wandb
from pytorch_lightning import seed_everything, Callback
from pytorch_lightning.callbacks import EarlyStopping, LearningRateMonitor, ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger

from requestModels import ModelParams
from nn_trainer import *
from nn_trainer.data_module import DataModule


def train_model(model_params: ModelParams):
    seed_everything(0, workers=True)
    dm = DataModule(model_params)
    dm.setup()

    name = create_name(model_params)

    metric_call_back = MetricsCallback()
    checkpoint_callback = ModelCheckpoint(
        dirpath=f"models/{name}",
        filename='{val_loss:.4f}-{epoch}',
    )

    model = lstm.LSTM(
        input_dim=dm.input_size,
        hidden_dim=model_params.hidden_dim,
        output_dim=OUTPUT_DIM,
        num_layers=model_params.number_of_layers,
        learning_rate=model_params.learning_rate,
        x_scaler=dm.X_scaler,
        y_scaler=dm.y_scaler,
        is_twitter=dm.is_with_twitter,
        lookback=dm.lookback,
        token=dm.token,
    )
    wandb_logger = WandbLogger(
        project="Sentimental-Investors",
        name=name
    )
    trainer = pl.Trainer(
        callbacks=[
            EarlyStopping("val_loss", patience=3, min_delta=0.00002),
            LearningRateMonitor(logging_interval='step'),
            metric_call_back,
            checkpoint_callback
        ],
        logger=wandb_logger,
        deterministic=True,
        log_every_n_steps=1,
    )
    trainer.fit(model, dm)
    trainer.test(model, dm)
    wandb.finish()
    return metric_call_back.json()


def create_name(p: ModelParams) -> str:
    return f"{p.token}_{p.start_date}_{p.end_date}_{p.number_of_layers}\
_{p.learning_rate}_{p.hidden_dim}_{p.look_back}_{p.batch_size}_{p.is_twitter}"


class MetricsCallback(Callback):
    def __init__(self):
        super().__init__()
        self.val_metric = []
        self.train_metric = []
        self.test_metric = []

    def on_validation_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        each_me = copy.deepcopy(trainer.callback_metrics)
        self.val_metric.append(each_me)

    def on_train_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        each_me = copy.deepcopy(trainer.callback_metrics)
        self.train_metric.append(each_me)

    def on_test_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        each_me = copy.deepcopy(trainer.callback_metrics)
        self.test_metric.append(each_me)

    def json(self):
        self.val_metric.pop(0)  # First record don't have sens
        return {
            "val_loss": [float(metric["val_loss"]) for metric in self.val_metric],
            "train_loss": [float(metric["train_loss"]) for metric in self.train_metric],
            "test_loss": float(self.test_metric[0]["test_loss"]),
        }
