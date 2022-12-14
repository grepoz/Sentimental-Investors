import datetime
from typing import Optional

from pydantic import BaseModel, validator

from nn_trainer import *


class ModelParams(BaseModel):
    token: str = "AMZN"
    start_date: datetime.date = datetime.date.fromisocalendar(2018, 1, 1)
    end_date: datetime.date = datetime.date.today()
    number_of_layers: int = NUM_LAYERS
    hidden_dim: int = HIDDEN_DIM
    learning_rate: float = LEARNING_RATE
    look_back: int = LOOKBACK
    batch_size: int = BATCH_SIZE
    is_twitter: bool

    @validator('start_time', 'end_time', pre=True)
    def pre_process(cls, v: str):
        v = v.split("T")[0]  # JSON format '2022-10-13T17:51:24.986Z'
        return v


class PredictParams(BaseModel):
    model_name: str
    date: datetime.date = datetime.date.today()
    lookback: Optional[int]
