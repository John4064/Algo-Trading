
import alpaca_trade_api as alpaca
from config import *
from datetime import datetime as dt
# Press the green button in the gutter to run the script.
from algorithm import *
from scrape import *
import ast



def run():
    ss = YahooScrape()
    #voldf is the voltaile dataframe contains all info
    #sort valid creates valid stocks which is just a list of tickers
    try:
        ss.findVolatile(100)
        ss.sortValid(1)
        print(ss.validStocks)
        #ss.sortValid(1)
    except:
        print("For heading in tr_elements[0] line 34 find volatile")
    #Bug with sort valid

    #print(ss.voldf['Symbol'])
    return
if __name__ == '__main__':
    #run()
    tickers =['NUAN', 'CAN', 'GGB', 'JNJ', 'NVCR', 'NVDA', 'NI', 'YNDX', 'NET', 'AHCO']
    myApi = algo()
