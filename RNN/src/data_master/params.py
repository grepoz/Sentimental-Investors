import datetime


class Params:
    def __init__(self, start_time: datetime.date, end_time: datetime.date):
        self.start_time = start_time
        self.end_time = end_time
