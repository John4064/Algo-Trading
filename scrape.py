import alpaca_trade_api as alpaca
import lxml.html as lh
import pandas as pd
import requests
import sys
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
                # Append the data to the empty list of the i'th column
                col[i][1].append(data)
                # Increment i for the next column
                i += 1
        #gets the volatile stock tickers
        self.vol =col[0][1]
        return
    def findStat(self,ticker):
        """
        Finds Price, Volume, and basic stats about the stock
        """
        url = self.urlBuilder(ticker,0)
        page = requests.get(url).text
        l = {}
        u = []
        # Page is the page source code that we are searching
        # Using beautiful soup we sort through with a html parser.
        # Search for body tags which our data is key on in yahoo finance
        soup = BeautifulSoup(page, "html.parser")
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
        return u
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
        #Useless method atm
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
        #Then Checks the price for >5
        ans = []
        stocks = self.vol
        #Iterates through the volatile stocks
        for x in range(len(stocks)):
            #gets the finanacial stats for every one, then volume, avgvolume, the open price
            stats =self.findStat(stocks[x])
            try:
                vol = int(stats[6]['Volume'].replace(',', ''))
                avgVol=int(stats[7]['Avg. Volume'].replace(',', ''))
                price = float(stats[1]['Open'])
                if (price > 4.9):
                    # CHECKS that the volume is over double avg volume
                    if (vol > avgVol * 2):
                        # financials index 19 is the float
                        ans.append(stocks[x])
                self.validStocks = ans
            except:
                print("Skipping Import Text Error")
            #checks the price to get rid of any penny stocks immediatly.

        return ans

