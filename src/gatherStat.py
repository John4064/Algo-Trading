from config import *
from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd

if __name__ == '__main__':
    api = REST(TESTAPI_KEY, TESTAPI_SECRET, APCA_API_BASE_URL, 'v2')


    def process_bar(bar):
        # process bar
        print(bar)


    bar_iter = api.get_bars_iter("UNH", TimeFrame.Hour, "2021-06-08", "2021-06-08", adjustment='raw')
    for bar in bar_iter:
        process_bar(bar)
