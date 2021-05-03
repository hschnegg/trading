from datetime import datetime
import backtrader as bt
from strategies import *


cerebro = bt.Cerebro()


# data = bt.feeds.YahooFinanceCSVData(
#    dataname='data/fake.csv')

data = bt.feeds.YahooFinanceData(dataname='XRP-USD',
                                 fromdate=datetime(2021, 3, 18),
                                 todate=datetime(2021, 5, 3))

cerebro.adddata(data)


cerebro.addstrategy(ID_NR4)


cerebro.run()

