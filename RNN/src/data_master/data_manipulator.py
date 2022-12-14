import pandas as pd


class DataManipulator:

    def __init__(self, _params):
        self.params = _params

    # noinspection SpellCheckingInspection
    def preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        df.set_index('Date', inplace=True)
        return self.reindex_and_fillnan(df)

    def reindex_and_fillnan(self, df: pd.DataFrame):
        df = df.tz_localize(None)  # Make index native

        try:
            df = df.drop("Adj Close", axis=1)
        except KeyError:
            pass
        df = df.reindex(self.get_weekdays_helper())
        # noinspection SpellCheckingInspection
        df = df.fillna(method='ffill')
        return self.fill_potentially_remaining_nan(df)

    def get_weekdays_helper(self):
        """Getting all weekdays between start_time and end_time"""
        all_weekdays = pd.date_range(
            start=self.params.start_time,
            end=self.params.end_time,
            freq='D',
        )
        return all_weekdays

    # noinspection SpellCheckingInspection
    @staticmethod
    def fill_potentially_remaining_nan(columns: pd.DataFrame) -> pd.DataFrame:
        # noinspection SpellCheckingInspection
        """somehow pandas method fillna(method='ffill') leaves Nan values at the beginning of columns
                    this solution is NOT OPTIMAL!"""
        # TODO make optimally
        # TODO TODO
        # noinspection SpellCheckingInspection
        return columns if columns is None else columns.fillna(method='bfill')
