from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import backtrader as bt
from strategies import *
import quantstats


cerebro = bt.Cerebro()


# data = bt.feeds.YahooFinanceCSVData(
#    dataname='data/fake.csv')

data = bt.feeds.YahooFinanceData(dataname='XRP-USD',
                                 fromdate=datetime(2021, 1, 1),
                                 todate=datetime.now() + timedelta(days=1))


cerebro.adddata(data)

# Add a strategy
# cerebro.addstrategy(ID_NR4)
# With optimisation
strats = cerebro.optstrategy(
    ID_NR4,
    stop_atr_multiple=[1, 1.5, 2, 2.5, 3, 3.5, 4],
    optimise=1)


cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')


start_portfolio_value = cerebro.broker.getvalue()


results = cerebro.run()
#cerebro.plot(style='bar')


end_portfolio_value = cerebro.broker.getvalue()
pnl = end_portfolio_value - start_portfolio_value


print(f'Starting Portfolio Value: { start_portfolio_value }')
print(f'Final Portfolio Value: { end_portfolio_value }')
print(f'PnL: { pnl }')


cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')


strat = results[0]
portfolio_stats = strat.analyzers.getbyname('PyFolio')
returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
returns.index = returns.index.tz_convert(None)


quantstats.reports.html(returns, output='stats.html', title='Test1')
