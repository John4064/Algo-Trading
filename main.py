from twelvedata import TDClient
import pandas
# Press the green button in the gutter to run the script.
def communicate():
    td = TDClient(apikey="79e029422b1249208c83a068e5730e23")
    ts = td.time_series(symbol=" BTC/USD", interval="1min", outputsize=1)
    ts = ts.as_pandas()
    print(ts.head())
if __name__ == '__main__':
    btc = p
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
