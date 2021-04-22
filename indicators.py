import config
import numpy as np
import pandas as pd
import alpaca-trade-api as alpaca

class indicators():

    def __init__(self,ind):
        #ind determines which indicactor it is
        """
        ind determines which indicator to use
        0 is Simple Moving Average
        1 is Rsi indicator
        """
        self.indic = ind
        self.tickers = 'BA'

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