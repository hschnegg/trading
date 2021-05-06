from datetime import datetime
import backtrader as bt
from strategies import *


cerebro = bt.Cerebro()


# data = bt.feeds.YahooFinanceCSVData(
#    dataname='data/fake.csv')

data = bt.feeds.YahooFinanceData(dataname='XRP-USD',
                                 fromdate=datetime(2021, 3, 18),
                                 todate=datetime.now())

cerebro.adddata(data)


cerebro.addstrategy(ID_NR4)

start_portfolio_value = cerebro.broker.getvalue()

cerebro.run()

end_portfolio_value = cerebro.broker.getvalue()
pnl = end_portfolio_value - start_portfolio_value

print(f'Starting Portfolio Value: { start_portfolio_value }')
print(f'Final Portfolio Value: { end_portfolio_value }')
print(f'PnL: { pnl }')
