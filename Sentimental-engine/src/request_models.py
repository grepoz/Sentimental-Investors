from pydantic import BaseModel, validator

from secret import BEARER_TOKEN


class ScrapParams(BaseModel):
    asset_name: str
    token: str
    start_time: str
    end_time: str
    query: str = ""
    bearer_token: str = BEARER_TOKEN

    @validator('start_time', 'end_time', pre=True)
    def pre_proces(cls, v: str):
        v = v.split("T")[0]  # JSON format '2022-10-13T17:51:24.986Z'
        return v


class UserScrapParams(ScrapParams):
    email: str
