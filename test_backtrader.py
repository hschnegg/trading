## https://analyzingalpha.com/backtrader-backtesting-trading-strategies
from datetime import datetime
import backtrader as bt


class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)


data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                 fromdate=datetime(2020, 1, 1),
                                 todate=datetime(2021,4,30))


cerebro = bt.Cerebro()

cerebro.broker.setcash(1337.0)
cerebro.broker.setcommission(commission=0.001)
cerebro.addstrategy(SmaCross)
cerebro.adddata(data)
print(f'Starting porfolio value: { cerebro.broker.getvalue() }')
cerebro.run()
print(f'Final porfolio value: { cerebro.broker.getvalue() }')
cerebro.plot(style='bar')
