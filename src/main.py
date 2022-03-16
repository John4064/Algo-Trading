import alpaca_trade_api as alpaca
from algorithm import *
import time
import sys
from config import *


def run():
    """
    To Test importing tickers
    """
    ss = YahooScrape()
    # voldf is the volatile dataframe contains all info
    # sort valid creates valid stocks which is just a list of tickers
    try:
        ss.findVolatile(100)
        # Returns the tickers
        print(ss.vol)
        return ss.sortValid(1)
    except:
        print("For heading in tr_elements[0] line 34 find volatile")
    return []


if __name__ == '__main__':
    tickers = ['SKLZ', 'T', 'NKLA', 'FSR', 'TDC', 'HPE', 'HBAN', 'CS', 'CHPT', 'DOW', 'XM', 'NUAN', 'YSG', 'WBT']
    myApi = algo()
