import os
from tqdm import tqdm
import pandas as pd
import iso8601
from datetime import datetime
import time

import sentiment_analyzer
from plotter import Plotter
from utilities.file_manager import FileManager
from utilities.time_manager import TimeManager
from RNN.src.data_master.data_manager import DataManager
from RNN.src.data_master.params import Params
from sklearn.preprocessing import MinMaxScaler

columns_names = ['Date', 'VaderSentiment', 'FlairSentiment', 'TweetCounter']


def sum_rows(row_local, new_row_local):
    return list(map(sum, zip(row_local.tolist(), new_row_local)))


def __calculate_average_of_sentiment_values(data_local):

    for index, row in data_local.iterrows():
        if row[2] > 0:
            row_proc = [el / float(row[2]) for el in row.tolist()[:2]]
            data_local.loc[index, columns_names[1:3]] = row_proc

    return data_local


def __to_dataframe(data_local) -> pd.DataFrame:
    df = pd.DataFrame(data_local, columns=columns_names)
    df.set_index('Date', inplace=True)

    return df


def create_directories(_chart_directory, _csv_directory):
    exist = os.path.exists(_chart_directory)
    if not exist:
        os.makedirs(_chart_directory)

    exist = os.path.exists(_csv_directory)
    if not exist:
        os.makedirs(_csv_directory)


if __name__ == "__main__":

    should_calc = False

    chart_name = "chart_" + time.strftime("%Y-%m-%d_%H-%M-%S")
    chart_directory = "data\\chart\\"
    csv_directory = "data\\csv\\"
    create_directories(chart_directory, csv_directory)
    file_with_processed_data = csv_directory + "processed_data_2022-11-26_23-26-44.csv"

    start_time = datetime(2014, 1, 1).date()
    end_time = datetime(2022, 10, 10).date()
    params_dict = {"start_time": start_time, "end_time": end_time}
    params = Params(start_time, end_time)
    company_data = "INTC_2014-01-01_2022-10-10"
    tweet_directory = "C:\\Users\\grzeg\\PycharmProjects\\sentimental-app-scrapped-data\\" + company_data + "\\"

    token = "INTC"

    if should_calc is True:

        files = FileManager.get_files_from_temp_dir(tweet_directory)

        data = [[single_date, 0.0, 0.0, 0]
                for single_date in (TimeManager.generate_date_range(params_dict))]
        data = __to_dataframe(data)

        cnt = 0
        for filepath in tqdm(files, desc="Creating data", colour="GREEN"):
            tweets = FileManager.read_json(filepath)

            for tweet in tweets:
                tweet_creation_date = iso8601.parse_date(tweet['created_at']).date()
                text = tweet['text']

                vader_tweet_sentiment = sentiment_analyzer.get_sentiment(text)
                flair_tweet_sentiment = sentiment_analyzer.get_sentiment(text, False)

                new_row = [
                    vader_tweet_sentiment,
                    flair_tweet_sentiment,
                    1
                ]

                row = data.loc[tweet_creation_date]
                updated_row = sum_rows(row, new_row)
                data.loc[tweet_creation_date] = updated_row

        data_manager = DataManager(params)
        stocks = data_manager.get_stock_data(token)
        stocks_close = stocks.loc[:, stocks.columns.intersection(['Close'])]
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaled_stocks_close = scaler.fit_transform(stocks_close)

        data = __calculate_average_of_sentiment_values(data)
        data.drop('TweetCounter', inplace=True, axis=1)
        data['Close'] = stocks_close
        data['ScaledClose'] = scaled_stocks_close
        data = pd.read_csv(file_with_processed_data)
        Plotter.plot(data, chart_name, token)

    else:
        data = pd.read_csv(file_with_processed_data)
        data.set_index('Date', inplace=True)
        data.to_csv("processed_data_2022-11-26_23-26-44.csv")
        Plotter.plot(data, chart_directory + chart_name, token)

    print("end")
