import pandas as pd
import quandl
import requests


class QuandlSocket:

    """
        Socket for cached historical market data requests
    """

    def __init__(self):
        quandl.ApiConfig.api_key = 'G-_bYxUyUv3v_jCxGMZi'
