from colorama import Fore, Style, init as ColoramaInit
import alpaca_trade_api as alpaca
from config import *
from datetime import  *
import numpy as np
import logging
from scrape import *
import time
import threading
ColoramaInit(autoreset=True)

#Logging info
#ogging.basicConfig(filename='debug.log', level=logging.DEBUG)
logging.basicConfig(filename='trades.log', level=logging.INFO)
class algo:
    def __init__(self):
        self.api = alpaca.REST(TESTAPI_KEY, TESTAPI_SECRET, APCA_API_BASE_URL, 'v2')
        self.account = self.api.get_account()
        self.tickers = ['BAC', 'PPD', 'QS', 'NRZ', 'NUAN', 'GSK', 'KIM', 'DELL']
        #for x in self.tickers:
            #self.movingData(x,30)
            #self.volumeCheck(x,30)

        #self.sma()
        self.blacklist = []
        self.timeToClose = None
        #self.run()
    def run(self):
        while True:
            self.clock = self.api.get_clock()
            closingTime = self.clock.next_close.replace(tzinfo=timezone.utc).timestamp()
            currTime = self.clock.timestamp.replace(tzinfo=timezone.utc).timestamp()
            self.timeToClose = closingTime - currTime
            if (self.timeToClose < (60 * 15)):
                # Close all positions when 15 minutes til market close.
                print("Market closing soon.  Closing positions.")

                positions = self.alpaca.list_positions()
                for position in positions:
                    #CHANGE THIS TO PROFIT VS LOSS
                    if (position.side == 'long'):
                        orderSide = 'sell'
                    else:
                        orderSide = 'buy'
                    qty = abs(int(float(position.qty)))
                    respSO = []
                    tSubmitOrder = threading.Thread(target=self.submitOrder(qty, position.symbol, orderSide, respSO))
                    tSubmitOrder.start()
                    tSubmitOrder.join()

                # Run script again after market close for next trading day.
                print("Sleeping until market close (15 minutes).")
                time.sleep(60 * 15)
            else:
                # Rebalance the portfolio.
                print(5)
                #tRebalance = threading.Thread(target=self.rebalance)
                #tRebalance.start()
                #tRebalance.join()
                time.sleep(60)







        logging.info("PROGRAM OFF")
        return
    def importT(self):
        #imprt tickers
        scrape = YahooScrape()
        scrape.findVolatile(100)
        self.tickers= scrape.sortValid(1)
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

    def sma(self):
        barTimeframe = "1D"  # 1Min, 5Min, 15Min, 1H, 1D
        for x in self.tickers:
            returned_data = self.api.get_barset(x, barTimeframe, limit=100)
            timeList = []
            openList = []
            highList = []
            lowList = []
            closeList = []
            volumeList = []
            #Converting returned data to dataframe and flattening the columns
            bar = returned_data.df
            bar.columns = bar.columns.get_level_values(1)
            # Iterates through the barset thats in a dataframe and puts them into individual lists
            for index,row in bar.iterrows():
                #print(row['open'],row['volume'])
                #timeList.append(strptime(bar.time, '%Y-%m-%dT%H:%M:%SZ'))
                openList.append(row['open'])
                highList.append(row['high'])
                lowList.append(row['low'])
                closeList.append(row['close'])
                volumeList.append(row['volume'])

            #From lists to numpy arrays to use
            timeList = np.array(timeList)
            openList = np.array(openList, dtype=np.float64)
            highList = np.array(highList, dtype=np.float64)
            lowList = np.array(lowList, dtype=np.float64)
            closeList = np.array(closeList, dtype=np.float64)
            volumeList = np.array(volumeList, dtype=np.float64)
            # Calculated SMA trading indicator
            SMA20 = self.moving_average(closeList,20)

            SMA50 = self.moving_average(closeList,50)
            final20 = sum(SMA20)/len(SMA20)
            final50 = sum(SMA50)/len(SMA50)
            #Now that we have the stocks for the trading indicator
            #MASSIVE BUG HERE EDIT THE TRY/EXCEPT WHEN GET TO IT
            if(final20>final50):
                try:
                    #Throws an error if there is not a position
                    openPosition = self.api.get_position(x)
                except:
                    # Opens new position if one does not exist
                    #If we havent already bought this stock
                    #Gets our cash balance and the last quote for the stock
                    cashBalance = float(self.api.get_account().cash)
                    test = self.api.get_last_quote(x)._raw
                    #Then calculates the target position based on our maxpos(.25) and current price
                    price =test['askprice']
                    if(price  == 0):
                        price =test['bidprice']
                    else:
                        targetPositionSize = round(cashBalance / (price / maxPos),2)
                    print("We are going to buy: {} at {} for a total amount of {}".format(x,price,targetPositionSize))
                    logging.info("We are going to buy: {} at {} for a total amount of {}".format(x,price,targetPositionSize))
                    #order examples
                    #self.api.submit_order(symbol=x, qty=round(targetPositionSize/price), side='buy', type='market',time_in_force='day')
        return
    def moving_average(self,x, w):
        return np.convolve(x, np.ones(w), 'valid') / w


    def movingData(self,ticker,days):
        # Get daily price data for AAPL over the last x 'days' trading days.
        #limit is day,minutes
        barset = self.api.get_barset(ticker, 'day', limit=days )
        main_bars = barset[ticker]
        #Over the week see from monday->friday the change
        week_open = main_bars[0].o
        week_close = main_bars[-1].c
        percent_change = (week_close - week_open) / week_open * 100
        print('{} moved {}% over the last 5 day'.format(ticker,round(percent_change,2)))
        return
    def active(self):
        #aapl = self.api.get_barset('AAPL', '15Min',limit=1000).df
        #print(aapl.loc['2021-02-16 18:45:00-05:00'])
        orders = self.api.list_orders(status="")
        active_assets = self.api.list_positions()
        print(active_assets)
        return



