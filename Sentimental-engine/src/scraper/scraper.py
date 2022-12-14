import logging
import time
from tqdm import tqdm

from scraper.param_manager import ParamManager
from scraper.request_maker import RequestMaker
from utilities.file_manager import FileManager
from utilities.filter import ImpactFilter
from utilities.time_manager import TimeManager


class Scraper:

    def __init__(self, _param_manager: ParamManager):
        self.param_manager = _param_manager
        self.request_maker = RequestMaker()
        self.scrap_counter = 0
        self.dirpath_for_temp_files = FileManager.create_temp_dirpath_from_params(self.param_manager.description_params)

    def scrap_tweets(self):

        if Scraper.are_two_steps_request_necessary(self.param_manager.description_params):
            first_date_range, second_date_range = \
                TimeManager.split_to_two_date_ranges(self.param_manager.params)
            self.param_manager.set_date_range(second_date_range)
            self.scrap()

            self.param_manager.remove_domain_and_entity_from_query_param()
            self.param_manager.set_date_range(first_date_range)

        if Scraper.should_remove_domain_and_entity_from_query_param(self.param_manager.description_params):
            self.param_manager.remove_domain_and_entity_from_query_param()

        self.scrap()

    def scrap(self):
        json_response = {}

        while True:
            try:
                json_response = self.request_maker.request_tweets(self.param_manager.params)
            except Exception:
                chunks = 15
                print("waiting 15 minutes in 1 minute chunks ")
                for _ in tqdm(range(chunks)):
                    time.sleep(60)

            filtered_tweets = self.process_json_response(json_response)

            filepath = FileManager.create_temp_filename_from_params(self.scrap_counter, self.dirpath_for_temp_files)
            FileManager.save_tweets_as_json(filtered_tweets, filepath)
            self.scrap_counter += 1

            if "meta" in json_response:
                if self.has_more_pages(json_response):
                    self.set_next_token_param(json_response)
                else:
                    print("No more pages!")

            logger = logging.getLogger('main')
            logger.debug(f"jestem w scrapie")
            return

    @staticmethod
    def process_json_response(json_response):
        if Scraper.is_empty_or_invalid(json_response):
            print("scrapped tweets have invalid structure or are empty!")
            return []
        else:
            filtered_tweets = ImpactFilter.filter_against_impact(json_response["data"])
            return filtered_tweets

    @staticmethod
    def has_more_pages(json_response): return True if "next_token" in json_response["meta"] else False

    def set_next_token_param(self, json_response):
        next_token_param = {"next_token": json_response["meta"]["next_token"]}
        self.param_manager.set_parameter(next_token_param)

    @staticmethod
    def is_empty_or_invalid(json_response) -> bool:
        if "data" not in json_response or json_response["meta"]["result_count"] == 0:
            return True

        return False

    @staticmethod
    def are_two_steps_request_necessary(description_params):
        return TimeManager.is_special_date_between_dates(description_params)

    @staticmethod
    def should_remove_domain_and_entity_from_query_param(description_params):
        return TimeManager.is_before_special_date(description_params)
