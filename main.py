
import alpaca_trade_api as alpaca
from config import *
from datetime import datetime as dt
# Press the green button in the gutter to run the script.
from algorithm import *
from indicators import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
import time
import sys

def run():
    """
    To Test importing tickers
    """
    ss = YahooScrape()
    #voldf is the voltaile dataframe contains all info
    #sort valid creates valid stocks which is just a list of tickers
    try:
        ss.findVolatile(100)
        #Returns the tickers
        print(ss.vol)
        return ss.sortValid(1)
        #ss.sortValid(1)
    except:
        print("For heading in tr_elements[0] line 34 find volatile")
    #Bug with sort valid

    #print(ss.voldf['Symbol'])
    return []

class gui(QMainWindow):
    def __init__(self,parent=None):
        """Initializer."""
        super().__init__(parent)
        self.tickers = ['g', 'twtr', 'amd']
        self.setWindowTitle('QMainWindow')
        self.setCentralWidget(QLabel("I'm the Central Widget"))
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        self.setGeometry(600, 100, 680, 380)

        # 4. Show your application's GUI
        #window.show()
        # 5. Run your application's event loop (or main loop)
    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&File")
        self.menu.addAction('&Exit', self.close)


    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)


    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage(self.tickers[1],10000)
        self.setStatusBar(status)
def test():
    app = QApplication(sys.argv)
    win = gui()
    win.show()
    sys.exit(app.exec_())
    return
if __name__ == '__main__':
    tickers =['SKLZ', 'T', 'NKLA', 'FSR', 'TDC', 'HPE', 'HBAN', 'CS', 'CHPT', 'DOW', 'XM', 'NUAN', 'YSG', 'WBT']
    myApi = algo()
    #rsiIndicator()
    #test()



