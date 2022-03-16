import config
import numpy as np
import pandas as pd
import alpaca_trade_api as alpaca
from config import *
class indicators():

    def __init__(self):
        #ind determines which indicactor it is
        """
        ind determines which indicator to use
        0 is Simple Moving Average
        1 is Rsi indicator
        """
        self.tickers = 'BA'
        self.api = alpaca.REST(TESTAPI_KEY, TESTAPI_SECRET, APCA_API_BASE_URL, 'v2')

    #actual indiaqctors
    def sma(self):
        return
    #calculations
    def moving_average(self,x, w):
        """
        Closing Prices
        :param x:Sequence of closing prices
        :param w: w is a length for a sequence of ones
        :return: The moving average of the sequence(x) in a list so we can see
        """
        return np.convolve(x, np.ones(w), 'valid') / w

    def rsiIndicator(self):
        return