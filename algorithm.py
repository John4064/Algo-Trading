from colorama import Fore, Style, init as ColoramaInit
import alpaca_trade_api as alpaca
from datetime import  *
import numpy as np
import logging
from scrape import *
import time
import threading
import sys
from config import *
ColoramaInit(autoreset=True)

#Logging info
#ogging.basicConfig(filename='debug.log', level=logging.DEBUG)
logging.basicConfig(filename='Misc/trades.log', level=logging.INFO)
class algo:
    def __init__(self):
        #Initialization of accounts api, account, twelvedataclients
        self.api = alpaca.REST(TESTAPI_KEY, TESTAPI_SECRET, APCA_API_BASE_URL, 'v2')
        self.account = self.api.get_account()
        #Potential Stocks to check
        self.tickers = []
        #Stocks the made it past the initial check
        self.approved = ['F', 'SPCE', 'RBLX', 'TAL', 'NVDA', 'MFC', 'IOVA', 'VFC', 'BEKE', 'YALA']
        self.blacklist = []
        self.timeToClose = None
        #self.importT()
        #self.test()
        self.run()
    def test(self):
        #RSI indicator
        #Dead Code
        """
        @:param:
        :return:
        """
        #under30 is undervalued/oversold and  over 70 is overvalued/undersold
        for stonk in self.approved:
            print(stonk)
            alp = self.api.get_barset(stonk,'1D',limit=14).df
            alp.columns = alp.columns.get_level_values(1)
            if(len(alp)>0):
                test5=sum(alp['close'])/len(alp)
                print("Average closing price {}".format(test5))
                #determine if higher or lower
                if(alp['close'][13]>alp['close'][12]):
                    print("current day is higher")
                else:
                    print("Previous day is higher")
                #rsi = 100 - (100/(1+RS))
                for x in range(len(alp['close'])-1):
                    print(alp['close'][x])
                    print(alp['close'][x]-alp['open'][x+1])
            else:
                print("Empty Dataframe FUCKING ALPACA")
        return
    def run(self):
        self.importT()
        while True:
            #Calculate time and time to closing as well as sets the positions
            self.clock = self.api.get_clock()
            closingTime = self.clock.next_close.replace(tzinfo=timezone.utc).timestamp()
            currTime = self.clock.timestamp.replace(tzinfo=timezone.utc).timestamp()
            self.timeToClose = closingTime - currTime
            positions = self.api.list_positions()
            #Checks if markets r open
            if self.clock.is_open:
                print("MARKET IS OPEN")
                if (self.timeToClose < (60 * 15)):
                    # Close all positions when 15 minutes til market close.
                    print("Market closing soon.  importing tickers.")
                    self.importT()
                    print("Sleeping until market close (15 minutes).")
                    time.sleep(60 * 15)
                    #major bug here need to just clean up this elif
                elif(self.timeToClose == (60*60)):
                    print("An Hour is Left Importing for end day trading!")
                    self.importT()
                    time.sleep(60)
                else:
                    #Checking tickers for indicator
                    #When live, on 1 minute interval we check
                    #If stocks are ready to sell
                    self.sma()
                    for position in positions:
                        print("check position")
                        profloss = float(position.unrealized_plpc) * 100
                        if (profloss > 8 or (profloss < -4)):
                            orderSide = 'sell'
                            qty = abs(int(float(position.qty)))
                            #not entirelly sure was respSO is
                            #Logging, printing, submitting orders
                            logging.info("AT {} SOLD {}".format(time.ctime(),position.symbol))
                            print("AT {} SOLD {}".format(time.ctime(),position.symbol))

                            tSubmitOrder = threading.Thread(target=self.submitOrder(qty, position.symbol, orderSide))
                            tSubmitOrder.start()
                            tSubmitOrder.join()

                    #Checkings the SMA indicator of our tickers for purchases
                    #This needs to be clean up and proper

                    time.sleep(60)
            else:
                #When off
                print("OFF LINE")
                time.sleep(60*15)
        logging.info("PROGRAM OFF")
        return
    def submitOrder(self,qty,symbol,orderSide):
        """
        :param qty: Quantity of the shares
        :param symbol: Which specific symbol
        :param orderSide: Do we purchase or sell it
        :return:
        """
        x = symbol
        t = qty
        self.api.submit_order(symbol=x, qty=t, side=orderSide, type='market',time_in_force='day')
        return
    def sma(self):
        """
        Indicator runs through all our tickers for the algorithm
        :return: void
        """
        barTimeframe = "1D"  # 1Min, 5Min, 15Min, 1H, 1D
        for x in self.tickers:
            returned_data = self.api.get_barset(x, barTimeframe, limit=100)
            closeList = []
            volumeList = []
            #Converting returned data to dataframe and flattening the columns
            bar = returned_data.df
            bar.columns = bar.columns.get_level_values(1)
            # Iterates through the barset thats in a dataframe and puts them into individual lists
            for index,row in bar.iterrows():
                #print(row['open'],row['volume'])
                closeList.append(row['close'])
                volumeList.append(row['volume'])

            #From lists to numpy arrays to use
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
                self.approved.append(x)
                try:
                    #Throws an error if there is not a position which means we buy it
                    openPosition = self.api.get_position(x)
                except:
                    #Calculates the price and size of our position
                    price,targetPositionSize = self.calculateQ(x)
                    #logs and prints all the transaction (Put in function for later)
                    print("On {} We are going to buy: {} at {} for a total amount of {}".format(time.ctime(),x,price,round(targetPositionSize)-1))
                    logging.info("On {} We are going to buy: {} at {} for a total amount of {}".format(time.ctime(), x,price,round(targetPositionSize)-1))
                    #order examples
                    #Send order
                    #NEEDS TO BE WHOLE NUMBER (Buggy with Fractional Shares
                    self.submitOrder(round(targetPositionSize) - 1, x, 'buy')
                    try:
                       print("Success Buy")
                    except:
                        print("ERROR WITH ORDER PROBABLY ON PRICE")
        return
    def moving_average(self,x, w):
        return np.convolve(x, np.ones(w), 'valid') / w
    def importT(self):
        """
        Sets the tickers list of all volatile and valid stocks from scrape
        :return:
        """
        #imprt tickers
        scrape = YahooScrape()
        scrape.findVolatile(100)
        self.tickers.extend(scrape.sortValid(1))
        print(self.tickers)
        logging.info(self.tickers)
        return
    def calculateQ(self,stock):
        """ This calculates the amount we are going to buy with current cash balance
        :param stock: Ticker of the stock
        :return:
        """
        # Opens new position if one does not exist
        # If we havent already bought this stock
        # Gets our cash balance and the last quote for the stock
        cashBalance = float(self.api.get_account().cash)
        quoteL = self.api.get_last_quote(stock)._raw
        # Then calculates the target position based on our maxpos(.25) and current price
        price = quoteL['askprice']
        if (price == 0):
            price = quoteL['bidprice']
        targetPositionSize = round(cashBalance / (price / maxPos), 2)
        return price,targetPositionSize



