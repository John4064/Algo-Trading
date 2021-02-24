import time
from config import *
import pandas as pd
import requests
import lxml.html as lh
import unittest
from bs4 import BeautifulSoup
import alpaca_trade_api as alpaca
class yahooTest(unittest.TestCase):
    def TsetUp(self):
        # https://finance.yahoo.com/most-active
        return
    def test_recent(self):
        #top 50 most volatile stocks
        url = "https://finance.yahoo.com/most-active?offset=0&count=100"
        page = requests.get(url)
        # Store the contents of the website under doc
        doc = lh.fromstring(page.content)
        # Parse data that are stored between <tr>..</tr> of HTML
        tr_elements = doc.xpath('//tr')
        # Check the length of the first 25 rows
        #Column list
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
            i=0
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
        self.df = pd.DataFrame(Dict)
        return self.df
    def urlBuilder(self,ticker):
        """
            Builds a url Given a stock ticker to find the quote
            """
        url = 'https://finance.yahoo.com/quote/'
        return url+ticker
    def test_financials(self):
        #PageS is page source from the desired ticker
        #We then convert it to beautiful soup so
        #we can search through for our desired tables(tbody tags)
        #then check for the data we want. Being the rows then columns
        l={}
        u=[]
        pageS = requests.get(self.urlBuilder('WWE')).text
        soup = BeautifulSoup(pageS,"html.parser")
        alldata = soup.find_all("tbody")
        try:
            table1 = alldata[0].find_all("tr")
            for x in range(len(table1)):
                try:
                    table1_td = table1[x].find_all("td")
                except:
                    table1_td =None
                l[table1_td[0].text] = table1_td[1].text
                u.append(l)
                l={}
        except:
            table1 = None
        try:
            table2 = alldata[1].find_all("tr")
            for x in range(len(table2)):
                try:
                    table2_td = table2[x].find_all("td")
                except:
                    table2_td =None
                l[table2_td[0].text] = table2_td[1].text
                u.append(l)
                l={}
        except:
            table2 = None
        return u
    def test_volCheck(self):
        #This function takes the list of active stocks
        #determines which match a 2:1 ratio of the current volume based on avg
        # self.urlBuilder(stocks['Symbol'][x])
        #Returns
        ans=[]
        stocks = self.test_recent()
        #for col in stocks.columns:
            #print(col)
        for x in range(len(stocks)):
            #print(stocks['Symbol'][x]+ " Volume "+ stocks['Volume'][x]+" Avg Vol "+stocks['Avg Vol (3 month)'][x])
            vol = str(stocks['Volume'][x])
            vol = float(vol[:-1])
            avgVol = str(stocks['Avg Vol (3 month)'][x])
            avgVol = float(avgVol[:-1])
            if (vol > avgVol * 2):
                ans.append(stocks['Symbol'][x])
                #print("{} has a valid volume to trade".format(stocks['Symbol'][x]))
        return ans
    def test_rsiIndicator(self):
        #Checks the realtive strength index
        #A indicator between 0-100
        #One factor to consider
        #https://www.investopedia.com/investing/momentum-and-relative-strength-index/
        #Rs is relative strength based on the average of x days up closes and down closes
        period = 30
        self.api = alpaca.REST(TESTAPI_KEY, TESTAPI_SECRET, APCA_API_BASE_URL, 'v2')
        tickers = self.test_volCheck()
        barset = self.api.get_barset(tickers[2], 'day', limit=period)
        main_bars = barset[tickers[2]]
        sum=0
        for x in range(len(main_bars)):
            sum = sum+main_bars[x].c
        sum=round(sum/len(main_bars),2)
        print("The avg close was {} for {}".format(sum,tickers[2]))
        self.api.close()


        stocks = self.test_recent()
        RS=5
        rsi=100-(100/(1+RS))
        #print(stocks)
        return
if __name__ == '__main__':
    unittest.main()