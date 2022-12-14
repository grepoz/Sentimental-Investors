import datetime
from unittest import TestCase

from predicter import get_val_loss, get_best_model, predict


class Test(TestCase):
    def test_get_val_loss(self):
        self.assertEqual(0.02, get_val_loss("val_loss=0.02-epoch=535.ckpt"))

    def test_get_best_model(self):
        get_best_model("BTC_2014-09-17_2022-09-17_1_0.0008_1_5_30_True")

    def test_predict(self):
        predict("BTC_2014-09-17_2022-09-17_1_0.0008_1_5_30_True", datetime.date(2022, 9, 1))

