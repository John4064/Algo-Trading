
import alpaca_trade_api as alpaca
from config import *
from datetime import datetime as dt
# Press the green button in the gutter to run the script.
from algorithm import *
from scrape import *
#from kgui import *

def run():
    scrapestocks = YahooScrape()
    scrapestocks.findVolatile(100)
    scrapestocks.sortValid(1)
    while 0:
        hour, min, sec = updateTime()
        if (hour == 23 and min == 1 and sec == 0):
            scrapestocks.findVolatile(100)
            scrapestocks.sortValid()
            print("UPDATED")
        if (hour == 9 and min == 30 and sec == 0):
            print("TRADE")
        if (hour == 16 and min == 0 and sec == 0):
            print("TRADING OVER")
    return
if __name__ == '__main__':
    run()
