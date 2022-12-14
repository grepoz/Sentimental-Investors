from utilities.time_manager import TimeManager


class Asset:
    def __init__(self, stock, token):
        self.stock = stock
        self.token = token


class ParamManager:

    def __init__(self, _asset=None, _start_time=None, _end_time=None, _query=None, _bearer_token=None):
        """ default params """

        self.asset = Asset('bitcoin', 'BTC') if _asset is None else _asset
        self.start_time = TimeManager.create_rcf_3339_timestamp(2022, 5, 1) if _start_time is None \
            else TimeManager.parse_str_to_rcf(_start_time)
        self.end_time = TimeManager.create_rcf_3339_timestamp(2022, 6, 6) if _end_time is None \
            else TimeManager.parse_str_to_rcf(_end_time)
        self.end_time = TimeManager.adjust_end_date(self.end_time)

        if _query is None or _query == "":
            self.PHRASE = "(" + self.asset.stock + " OR " + self.asset.token + ")"
        else:  # what if user
            self.PHRASE = _query

        self.domain_and_entity = ""  # ' (context:131.1007360414114435072 OR context:174.1007360414114435072)'
        self.QUERY = ParamManager.compose_query(self.PHRASE, self.domain_and_entity)

        """
            explanation:
            -> is:verified - only verified users
            -> bitcoin - word/phrase which has to be in tweet
            -> lang:en - language of post
            -> -is:nullcast - 'Removes Tweets created for promotion only on ads.twitter.com'
            -> (context:131.1007360414114435072 OR context:174.1007360414114435072) - domain & entity, source: 
            https://raw.githubusercontent.com/twitterdev/twitter-context-annotations/main/files/evergreen-context-entities-20220601.csv

            --> additionally (just to check performance): has:cashtags
        """

        # TODO abstract params ie. dates
        self.params = {
            'query': self.QUERY,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'tweet.fields': 'created_at,public_metrics'
        }

        self.description_params = {
            'asset': self.asset,
            'phrase': self.PHRASE,
            'start_time': TimeManager.get_short_date(self.start_time),
            'end_time': TimeManager.get_short_date(self.end_time)
        }

        if TimeManager.are_dates_valid(self.description_params) is False:
            raise Exception("invalid dates!")

        """
            if there will be not enough info, we can filter tweets not by explicit query i.e. 'bitcoin', 
            but by manually filtering by context annotations: 
            https://developer.twitter.com/en/docs/twitter-api/annotations/overview
        """

    def set_parameter(self, parameter):
        key = list(parameter.keys())[0]
        self.params[key] = parameter[key]

    def append_parameter(self, parameter):
        self.set_parameter(parameter)

    def append_parameters_from_dict(self, dict_with_params):
        for item in dict_with_params.items():
            self.append_parameter(item)

    def print_params(self):
        for item in self.params.items():
            print(item)

    def get_params(self):
        return self.params

    def append_max_results(self):
        self.append_parameter({'max_results': '500'})

    def append_start_time(self, start_time):
        self.append_parameter({'start_time': start_time})

    def set_date_range(self, date_range):
        for date in date_range:
            self.set_parameter(date)

    def remove_domain_and_entity_from_query_param(self):
        query = ParamManager.compose_query(self.PHRASE, '')
        self.set_parameter({'query': query})

    @staticmethod
    def compose_query(phrase, domain_and_entity):
        return f'is:verified {phrase} lang:en -is:nullcast{domain_and_entity}'
