import time
from pathlib import Path
from utilities.file_manager import FileManager
from utilities.filter import scrap_counter
from scraper.scraper import Scraper
from sentimental_engine.engine import SentimentalEngine
from scraper.param_manager import ParamManager
import logging

use_csv = False


def process_scrap_request(asset=None, start_time=None, end_time=None, query=None, bearer_token=None, email=None):
    logger = logging.getLogger('main')
    logger.debug(f"asset: {asset}, query: {query}, start_time: {start_time}")
    tweets_param_manager = ParamManager(asset, start_time, end_time, query, bearer_token)
    sentimental_engine = SentimentalEngine(tweets_param_manager.description_params)

    if use_csv is False:
        tweets_param_manager.append_max_results()
        tweets_scraper = Scraper(tweets_param_manager)
        start = time.time()
        tweets_scraper.scrap_tweets()
        end = time.time()
        print(f"\nexcecution time: {end - start}\n")
        print(f"scrap counter: {scrap_counter}")

    data = sentimental_engine.create_sentimental_dataframe()

    filepath = Path(f'{FileManager.create_filename_from_params(tweets_param_manager.description_params)}')
    logger.debug(f"filepath: {filepath}")
    filepath.parent.mkdir(parents=True, exist_ok=True)

    data.to_csv(filepath)

    if logger is not None:
        logger.debug("Sending email")

    return data.to_csv()
