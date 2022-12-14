import requests

from secret import BEARER_TOKEN
from utilities.url_creator import UrlMaker


class RequestMaker:

    def __init__(self):
        self.string_request_url_maker = UrlMaker()

    @staticmethod
    def __bearer_oauth(r):
        """
        Method required by bearer token authentication.
        """
        bearer_token = BEARER_TOKEN  # os.environ.get("BEARER_TOKEN")
        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def request_tweets(self, request_params):
        request_url = self.string_request_url_maker.create_search_tweets_request_url()
        try:
            return self._connect_to_endpoint(request_url, request_params)
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    def _connect_to_endpoint(self, request_url, request_params):
        response = requests.get(request_url, auth=self.__bearer_oauth, params=request_params)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()
