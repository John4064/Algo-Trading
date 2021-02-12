#from twelvedata import TDClient,websocket
import pandas
from colorama import Fore, Style, init as ColoramaInit
import alpaca_trade_api as alpaca
from datetime import datetime as dt
# Press the green button in the gutter to run the script.
from config import *

ColoramaInit(autoreset=True)
class algo:
    def __init__(self):
        self.api = alpaca.REST(TESTAPI_KEY, TESTAPI_SECRET, APCA_API_BASE_URL, 'v2')
        self.account = self.api.get_account()
        self.tickers = ['YGMZ', 'KOSS', 'LACQ', 'GATO', 'ASM', 'NEXA', 'GME', 'FIZZ', 'CATB', 'SPCE', 'SPG', 'ABC']
    def marketHours(self):
        clock = self.api.get_clock()
        print('The market is {}'.format('open.' if clock.is_open else 'closed.'))

        # Check when the market was open on Dec. 1, 2018
        date = '2018-12-01'
        calendar = self.api.get_calendar(start=date, end=date)[0]
        print('The market opened at {} and closed at {} on {}.'.format(
            calendar.open,
            calendar.close,
            date
        ))
    def weekData(self,ticker):
        # Get daily price data for AAPL over the last 5 trading days.
        #limit is day,minutes
        barset = self.api.get_barset(ticker, 'day', limit=5 )
        main_bars = barset[ticker]
        #Over the week see from monday->friday the change
        week_open = main_bars[0].o
        week_close = main_bars[-1].c
        percent_change = (week_close - week_open) / week_open * 100
        print('{} moved {}% over the last 5 day'.format(ticker,percent_change))
        return
    def marketStream(self):

        return
    def run(self):
        orders = self.api.list_orders(status="")
        # Check if the market is open now.
        #self.weekData('TSLA')
        self.positions = self.api.list_positions()
        for x in range(len(self.positions)):
            print(type(self.positions[x]))
        return



if __name__ == '__main__':
    ls = algo()
    ls.run()



#epoch ns to date time
#market data comes in date time
