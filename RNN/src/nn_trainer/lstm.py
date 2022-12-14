import pytorch_lightning as pl
import torch
import torch.nn as nn

from nn_trainer import LEARNING_RATE


def is_accurate(start, pred, expected) -> bool:
    start_val = start[-1][3]
    return bool((start_val <= pred[0] and start_val <= expected[0]) or (start_val >= pred[0] and start_val >= expected[0]))


def calc_accuracy(x, y, y_pred):
    good_bad_table = [is_accurate(start, pred, expected) for start, pred, expected in zip(x, y_pred, y)]
    return sum(good_bad_table)/len(good_bad_table)


class LSTM(pl.LightningModule):

    def __init__(
            self,
            input_dim,
            hidden_dim,
            num_layers,
            output_dim,
            learning_rate,
            x_scaler,
            y_scaler,
            is_twitter,
            lookback,
            token,
    ):
        super(LSTM, self).__init__()
        self.save_hyperparameters()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.learning_rate = learning_rate
        self.is_twitter = is_twitter
        self.x_scaler = x_scaler
        self.y_scaler = y_scaler
        self.lookback = lookback
        self.token = token
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self._criterion = torch.nn.MSELoss(reduction='mean')
        self.l1_criterion = torch.nn.L1Loss()

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        # funkcje ReLu
        return out

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=LEARNING_RATE)
        lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer)
        return {"optimizer": optimizer, "lr_scheduler": lr_scheduler, "monitor": "val_loss"}

    def training_step(self, train_batch, batch_idx):
        x, y = train_batch
        y_pred = self(x)
        loss = self._criterion(y_pred, y)
        self.log('train_loss', loss)
        self.log('batch_idx', batch_idx)
        return loss

    def validation_step(self, val_batch, batch_idx):
        x, y = val_batch
        y_pred = self(x)
        loss = self._criterion(y_pred, y)
        accuracy = calc_accuracy(x, y, y_pred)
        mean_absolute_error = self.l1_criterion(y_pred, y)

        self.log("val_abs_error", mean_absolute_error)
        self.log("val_acc", accuracy)
        self.log('val_loss', loss)

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self(x)
        loss = self._criterion(y_pred, y)
        accuracy = calc_accuracy(x, y, y_pred)
        mean_absolute_error = self.l1_criterion(y_pred, y)

        self.log("test_abs_error", mean_absolute_error)
        self.log("test_acc", accuracy)
        self.log('test_loss', loss)

    def predict_step(self, batch, batch_idx: int, dataloader_idx: int = 0):
        x, y = batch
        y_pred = self(x)
        return y_pred


