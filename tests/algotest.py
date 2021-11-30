import unittest
from scrape import *

class Webscrape(unittest.TestCase):
    def checkCont(self):
        """
        Will make sure desired content is found on yahoo page
        """
        self.assertTrue(type(1) is int)
    def returnVal(self):
        """
        Will Test for if successfuly returning lists list when value
        """
        self.scrape = YahooScrape()
        self.scrape.findVolatile(100)
        self.assertIsInstance(self.scrape, list)

if __name__ == '__main__':
    unittest.main()
