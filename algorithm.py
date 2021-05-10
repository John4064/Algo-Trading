from colorama import Fore, Style, init as ColoramaInit
import alpaca_trade_api as alpaca
from config import *
from datetime import  *
import numpy as np
import logging
from scrape import *
import time
import threading
import twelvedata as td
ColoramaInit(autoreset=True)

#Logging info
#ogging.basicConfig(filename='debug.log', level=logging.DEBUG)
logging.basicConfig(filename='trades.log', level=logging.INFO)
class algo:
    def __init__(self):
        self.api = alpaca.REST(TESTAPI_KEY, TESTAPI_SECRET, APCA_API_BASE_URL, 'v2')
        self.account = self.api.get_account()
        self.tickers = []
        self.blacklist = []
        self.timeToClose = None
        #self.importT()
        self.td = td.TDClient(apikey=HISAPI_KEY)
        #self.test()
        self.run()
    def test(self):
        ticks = ['g','twtr','wdc','appl']
        potential = []
        ts = self.td.time_series(
            symbol=ticks[2],
            interval="1day"
        ).as_pandas()
        test = 0
        for x in ts['close']:
            test +=x
        print(test/len(ts))
        #30 day closing average
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
                    for position in positions:
                        print("check position")
                        profloss = float(position.unrealized_plpc) * 100
                        if (profloss > 8 or (profloss < -4)):
                            orderSide = 'sell'
                            qty = abs(int(float(position.qty)))
                            #not entirelly sure was respSO is
                            respSO = []
                            #Logging, printing, submitting orders
                            logging.info("SOLD {}".format(position.symbol))
                            print("SOLD {}".format(position.symbol))
                            tSubmitOrder = threading.Thread(target=self.submitOrder(qty, position.symbol, orderSide, respSO))
                            tSubmitOrder.start()
                            tSubmitOrder.join()
                    #Checkings the SMA indicator of our tickers for purchases
                    self.sma()
                    time.sleep(60)
            else:
                #When off
                print("OFF LINE")
                time.sleep(60*15)
        logging.info("PROGRAM OFF")
        return

    def submitOrder(self,qty,symbol,orderSide, respSO):
        """
        :param qty: Quantity of the shares
        :param symbol: Which specific symbol
        :param orderSide: Do we purchase or sell it
        :param respSO: Not sure
        :return:
        """
        x = symbol
        t = qty
        self.api.submit_order(symbol=x, qty=t, side=orderSide, type='market',time_in_force='day')
        return
    def importT(self):
        """
        Sets the tickers list of all volatile and valid stocks from scrape
        :return:
        """
        #imprt tickers
        scrape = YahooScrape()
        scrape.findVolatile(100)
        self.tickers= scrape.sortValid(1)
        print(self.tickers)
        logging.info(self.tickers)
        return

    def sma(self):
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
                    targetPositionSize = round(cashBalance / (price / maxPos),2)
                    print("We are going to buy: {} at {} for a total amount of {}".format(x,price,targetPositionSize))
                    logging.info("We are going to buy: {} at {} for a total amount of {}".format(x,price,targetPositionSize))
                    #order examples
                    #Send order
                    print("{} for {}".format(x,round(targetPositionSize/price) ))
                    try:
                        self.submitOrder(round(targetPositionSize/price),x,'buy',[])
                    except:
                        print("ERROR WITH ORDER PROBABLY ON PRICE")
        return

    def rsiIndicator(self):
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
            # Calculated RSI trading indicator
            rsiI= 20
            #Now that we have the stocks for the trading indicator
            #MASSIVE BUG HERE EDIT THE TRY/EXCEPT WHEN GET TO IT
            if(rsiI==20):
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
                    targetPositionSize = round(cashBalance / (price / maxPos),2)
                    print("We are going to buy: {} at {} for a total amount of {}".format(x,price,targetPositionSize))
                    logging.info("We are going to buy: {} at {} for a total amount of {}".format(x,price,targetPositionSize))
                    #order examples
                    #Send order
                    print("{} for {}".format(x,round(targetPositionSize/price) ))
                    try:
                        self.submitOrder(round(targetPositionSize/price),x,'buy',[])
                    except:
                        print("ERROR WITH ORDER PROBABLY ON PRICE")
        return
    def moving_average(self,x, w):
        return np.convolve(x, np.ones(w), 'valid') / w



