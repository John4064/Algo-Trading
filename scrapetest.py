import unittest
from scrape import *

class Webscrape(unittest.TestCase):
    def test_init(self):
        """
        Generic test to check if yahoo scrape object can be created
        """
        self.scrape = YahooScrape()
        self.assertEqual(self.scrape.code, 1)
    def test_urlbuild(self):
        """
        Verifying the string builder for our links are valid format!
        Does not check if website content/link exists
        """
        self.scrape = YahooScrape()
        #Random Generic Tickers to test on
        tickers =['SKLZ', 'T', 'NKLA', 'FSR', 'TDC', 'HPE', 'HBAN', 'CS', 'CHPT', 'DOW', 'XM', 'NUAN', 'YSG', 'WBT']
        #List of check validitiy of url built
        success =[]
        for x in range(len(tickers)):
            url = self.scrape.urlBuilder(tickers[x],0)
            #Checks if the url has valid elements needed
            if(tickers[x] in url and 'https://finance.yahoo.com/quote/' in url):
                #Appends random value to dignify success
                success.append(1)
        self.assertEqual(len(tickers),len(success))
    def test_cont(self):
        """
        Will make sure desired content is found on yahoo page
        (Tesla is the test company)
        """
        self.scrape = YahooScrape()
        stats =self.scrape.findStat('T')
        try:
            #Our desired values are found and correct format via typecasting
            vol = int(stats[6]['Volume'].replace(',', ''))
            avgVol=int(stats[7]['Avg. Volume'].replace(',', ''))
            price = float(stats[1]['Open'])
            #SUCCESS
            self.assertEqual(1,1)
        except:
            #Error Occured in content on site
            self.assertEqual(0,1)

    def test_process(self):
        """
        Will Test if our entire web scrape process is functional
        Creates our yahoo scrape object then find top 100 volatile stocks. Then sort on our criteria
        Takes long!
        """
        self.scrape = YahooScrape()
        self.scrape.findVolatile(100)
        self.tickers = []
        self.tickers.extend(self.scrape.sortValid(1))
        self.assertIsInstance(self.tickers, list)
if __name__ == '__main__':
    unittest.main()
