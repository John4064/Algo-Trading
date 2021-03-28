import alpaca_trade_api as alpaca
import lxml.html as lh
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from config import *

#Test

class YahooScrape():
    def __init__(self):
        # Finds the top X Volatile stocks
        # Contraint 10,25,50,100
        self.api = alpaca.REST(TESTAPI_KEY, TESTAPI_SECRET, APCA_API_BASE_URL, 'v2')
        # self.rsiIndicator()
        clock = self.api.get_clock()
        #if(clock.is_open == False):
            #print(clock.timestamp.hour)
        return
    def findVolatile(self, amount):
        # top 10,25,50,100 most volatile stocks
        url = "https://finance.yahoo.com/most-active?offset=0&count={}".format(amount)
        page = requests.get(url)
        # Store the contents of the website under doc
        doc = lh.fromstring(page.content)
        # Parse data that are stored between <tr>..</tr> of HTML
        tr_elements = doc.xpath('//tr')
        # Check the length of the first 25 rows
        # Column list
        col = []
        # For each row, store each first element (header) and an empty list
        for header in tr_elements[0]:
            name = header.text_content()
            col.append((name, []))

        for j in range(1, len(tr_elements)):
            # T is our j'th row
            T = tr_elements[j]
            # If row is not of size 10, the //tr data is not from our table
            if len(T) != 10:
                break
            i = 0
            # Iterate through each element of the row
            for t in T.iterchildren():
                data = t.text_content()
                # Check if row is empty
                if i > 0:
                    # Convert any numerical value to integers
                    try:
                        data = int(data)
                    except:
                        pass
                # Append the data to the empty list of the i'th column
                col[i][1].append(data)
                # Increment i for the next column
                i += 1
        Dict = {title: column for (title, column) in col}
        # Volatile df
        self.voldf = pd.DataFrame(Dict)
        #return pd.DataFrame(Dict)
        return

    def urlBuilder(self, ticker, option):
        """
            Builds a url Given a stock ticker to find the quote
            """
        url = 'https://finance.yahoo.com/quote/{}'.format(ticker)
        url1 = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(ticker, ticker)
        if option == 1:
            return url1
        else:
            return url

    def findFinancials(self, ticker, option):
        # PageS is page source from the desired ticker
        # We then convert it to beautiful soup so
        # we can search through for our desired tables(tbody tags)
        # then check for the data we want. Being the rows then columns
        l = {}
        u = []
        # Check the urlbuilder for more information about where we get this.
        # This option means we are looking for the key statistics of the stock
        if option == 1:
            pageS = requests.get(self.urlBuilder(ticker, 1)).text
        else:
            # This just gets us the base summary for the ticker
            pageS = requests.get(self.urlBuilder(ticker, 0)).text
        # PageS is the page source code that we are searching
        # Using beautiful soup we sort through with a html parser.
        # Search for body tags which our data is key on in yahoo finance
        soup = BeautifulSoup(pageS, "html.parser")
        alldata = soup.find_all("tbody")
        try:
            table1 = alldata[0].find_all("tr")
            for x in range(len(table1)):
                try:
                    table1_td = table1[x].find_all("td")
                except:
                    table1_td = None
                l[table1_td[0].text] = table1_td[1].text
                u.append(l)
                l = {}
        except:
            table1 = None
        try:
            table2 = alldata[1].find_all("tr")
            for x in range(len(table2)):
                try:
                    table2_td = table2[x].find_all("td")
                except:
                    table2_td = None
                l[table2_td[0].text] = table2_td[1].text
                u.append(l)
                l = {}
        except:
            table2 = None
        if option == 1:
            try:
                table3 = alldata[2].find_all("tr")
                for x in range(len(table2)):
                    try:
                        table3_td = table3[x].find_all("td")
                    except:
                        table3_td = None
                    l[table3_td[0].text] = table3_td[1].text
                    u.append(l)
                    l = {}
            except:
                table3 = None
        # Returns a list containing a dictionary
        return u

    def sortValid(self,option):
        # This function takes the list of active stocks
        # determines which match a 2:1 ratio of the current volume based on avg
        # self.urlBuilder(stocks['Symbol'][x])
        # Returns
        # ans = pd.DataFrame()
        ans = []
        stocks = self.voldf
        # for col in stocks.columns:
        # print(col)
        for x in range(len(stocks)):
            #x is index
            vol = str(stocks['Volume'][x])
            vol = float(vol[:-1])
            avgVol = str(stocks['Avg Vol (3 month)'][x])
            avgVol = float(avgVol[:-1])
            price = str(stocks['Price (Intraday)'][x])
            price = float(price[:-1])
            # CHECKS that the volume is double avg volume, as well that its above 5 dollars a share
            if (vol > avgVol * 2 and (price > 4.9)):
                # print("{} has a valid volume to trade".format(stocks['Symbol'][x]))
                # WE now need to check if Float is under 100m
                financials = self.findFinancials(stocks['Symbol'][x], 1)
                # financials index 19 is the float
                tradingFlo = financials[19]['Float ']
                try:
                    if (tradingFlo[-1] == 'M'):
                        tradingFlo = float(financials[19]['Float '][:-1])
                        if (tradingFlo < 100):
                            ans.append(stocks['Symbol'][x])
                except:
                    print("ERROR WITH THE FLOAT VALUE")
        self.validStocks = ans
        return

    def rsiIndicator(self):
        # Checks the realtive strength index
        # A indicator between 0-100
        # One factor to consider
        # https://www.investopedia.com/investing/momentum-and-relative-strength-index/
        # Rs is relative strength based on the average of x days up closes and down closes
        period = 30
        tickers = self.validStocks
        barset = self.api.get_barset(tickers[4], 'day', limit=period)
        main_bars = barset[tickers[4]]
        sum = 0
        for x in range(len(main_bars)):
            sum = sum + main_bars[x].c
        if sum != 0:
            sum = round(sum / len(main_bars), 2)
        else:
            print("INVALID IND")

        print("The avg close was {} for {}".format(sum, tickers[4]))
        self.api.close()

        stocks = self.voldf
        RS = 5
        rsi = 100 - (100 / (1 + RS))
        return

def updateTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    hour = int(current_time[0] + current_time[1])
    min = int(current_time[3] + current_time[4])
    sec = int(current_time[6] + current_time[7])
    return hour,min,sec

