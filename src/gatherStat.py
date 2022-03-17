from config import *
import alpaca_trade_api as alpaca
import pandas as pd

if __name__ == '__main__':
    api = alpaca.REST(TESTAPI_KEY, TESTAPI_SECRET, APCA_API_BASE_URL, 'v2')

    api.get_bars("AAPL", TimeFrame.Hour, "2021-06-08", "2021-06-08", adjustment='raw').df

