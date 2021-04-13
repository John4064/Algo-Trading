
import alpaca_trade_api as alpaca
from config import *
from datetime import datetime as dt
# Press the green button in the gutter to run the script.
from algorithm import *
from scrape import *
import ast

def tester():
    """
    Dead Code Returns all tickers and their open
    So unbelievably slow
    """
    ss = YahooScrape()
    tickers = tester()
    for x in tickers:
        if ('.' not in x) and ('-' not in x):
            test = ss.findStat(x)
            print(x)
            print(test[1])
    ticks = open("tickers.txt", "r")
    tickers=[]
    line = ticks.readline()
    try:
        line = ticks.readline()
        while line != '':
            ticker,name = line.split(',')
            tickers.append(ticker)
            line = ticks.readline()
    finally:
        ticks.close()
    return tickers
def run():
    ss = YahooScrape()
    #voldf is the voltaile dataframe contains all info
    #sort valid creates valid stocks which is just a list of tickers
    try:
        ss.findVolatile(100)
        print(ss.vol)
        #ss.sortValid(1)

    except:
        print("For heading in tr_elements[0] line 34 find volatile")
    #Bug with sort valid

    #print(ss.voldf['Symbol'])
    return
if __name__ == '__main__':
    run()
