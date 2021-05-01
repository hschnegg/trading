from datetime import datetime
import backtrader as bt


class hs_test(bt.SignalStrategy):

    ## https://algotrading101.com/learn/backtrader-for-backtesting/
    params = (('test_para', 20), )
    
    def __init__(self):
        self.tr = bt.indicators.TrueRange()
        self.atr = bt.indicators.AverageTrueRange(self.data)

    def next(self):
        print(f'Date Time: { self.data.datetime.date() } \        
                Parameter: { self.params.test_para } \
                Open: { self.data.open[0] } \
                High: { self.data.high[0] } \
                Low: { self.data.low[0] } \
                Close: { self.data.close[0] } \
                Volume: { self.data.volume[0] } \
                tr: { self.tr[0] } \
                atr: { self.atr[0] }')



data = bt.feeds.YahooFinanceData(dataname='XRP-USD',
                                 fromdate=datetime(2021, 1, 1),
                                 todate=datetime(2021,4,29))


cerebro = bt.Cerebro()



cerebro.addstrategy(hs_test)
cerebro.adddata(data)
# print(f'Starting porfolio value: { cerebro.broker.getvalue() }')
cerebro.run()
# print(f'Final porfolio value: { cerebro.broker.getvalue() }')
