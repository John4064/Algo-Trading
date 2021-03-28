
import alpaca_trade_api as alpaca
from config import *
from datetime import datetime as dt
# Press the green button in the gutter to run the script.
from algorithm import *
from scrape import *
import ast

def run():
    ss = YahooScrape()
    ss.findVolatile(25)
    #print(ss.voldf['Symbol'])
    return
if __name__ == '__main__':
    run()
