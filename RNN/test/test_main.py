from unittest import TestCase

import numpy as np
import torch

import main
from nn_trainer.main_train import create_name
from request_models import ModelParams


class Test(TestCase):
    def test_convert_to_tensor(self):
        arr1 = np.array([1, 2, 3, 4, 5])
        arr2 = np.array([5, 5, 5, 5, 5])

        t1, t2 = main.convert_to_tensor(arr1, arr2)
        arr1 = torch.from_numpy(arr1).type(torch.Tensor)

        self.assertTrue(torch.equal(t1, arr1))

    def test_creat_name(self):
        payload = {
            "token": "AMZN",
            "start_time": "2019-12-30",
            "end_time": "2022-10-01",
            "number_of_layers": 1,
            "hidden_dim": 1,
            "learning_rate": 0.0008,
            "look_back": 5,
            "batch_size": 64,
            "is_twitter": True
        }
        params = ModelParams.parse_obj(payload)
        self.assertEqual("AMZN_2019-12-30_2022-10-01_1_0.0008_1_5_64_True", create_name(params))
