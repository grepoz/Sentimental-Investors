""" default values """
# TODO: rethink usage of parameters and their location
# noinspection SpellCheckingInspection
import json

TICKER = 'AAPL'
START_DATE = '2022-01-01'
END_DATE = '2022-06-01'
DATA_PROVIDER = 'yahoo'
DIRECTORY_NAME = '../dataset'

with open('../../RNN/src/data_master/assets.json') as assets:  # add / delete one of ['RNN/', '../../RNN/']
    ASSETS = json.load(assets)
