from datetime import timedelta
import backtrader as bt
import math


class ID_NR4(bt.Strategy):
    params = (
        ('stop_atr_multiple', 2),
        ('optimise', 0), )


    def __init__(self):
        # Existing orders
        self.order = None

        # ID/NR4 indicators
        self.tr = bt.indicators.TrueRange()
        self.atr = bt.indicators.AverageTrueRange(self.data)
        self.nr4 = bt.indicators.MinN(self.tr, period=4)


    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{ dt.isoformat() } { txt }')


    def next(self):
        status = (f'===== L:{ self.datas[0].low[0] } | '
                  f'O: { self.datas[0].open[0] } | '
                  f'C: { self.datas[0].close[0] } | '
                  f'H: { self.datas[0].high[0] } ===== ')

        if self.order:
            status = status + ' Pending Order'
            if self.params.optimise == 0:
                self.log(status)
            return

        if self.position:
            status = status + ' In Trade'
            if self.params.optimise == 0:
                self.log(status)
            return
    
        if self.params.optimise == 0:
            if self.params.optimise == 0:
                self.log(status)

        # ID/NR4 signals
        self.is_nr4 = self.nr4[0] == self.tr[0]
        self.is_id = ((self.datas[0].high[0] < self.datas[0].high[-1]) and
                          (self.datas[0].low[0] > self.datas[0].low[-1]))
        self.buy_signal = self.is_nr4 and self.is_id
        self.buy_price = self.datas[0].high[0]
        self.low_stop = self.datas[0].low[0]
        self.limit_stop = self.params.stop_atr_multiple * self.atr
        self.size = round(100 / (self.buy_price - self.low_stop), 2)
    
        if self.buy_signal:
            if self.params.optimise == 0:
                self.log(f'+++++ Size { self.size } | Buy Price { self.buy_price } | Low Stop { self.low_stop } | Limit Stop { self.limit_stop } +++++')
            
            mainside = self.buy(size=self.size,
                                exectype=bt.Order.StopLimit,
                                plimit=self.buy_price,
                                valid=self.datas[0].datetime.date(0) + timedelta(days=3),
                                transmit=False)
            lowside  = self.sell(price=self.low_stop,
                                 size=mainside.size,
                                 exectype=bt.Order.Stop,
                                 transmit=False,
                                 parent=mainside)
            trailside = self.sell(size=mainside.size,
                                  exectype=bt.Order.StopTrail,
                                  trailamount=self.limit_stop,
                                  transmit=True,
                                  parent=mainside)


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            self.order = 'Submitted'
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                if self.params.optimise == 0:
                    self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                if self.params.optimise == 0:
                    self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            if self.params.optimise == 0:
                self.log('Order Canceled/Margin/Rejected')

        # Reset orders
        self.order = None


        def notify_trade(self, trade):
            '''Execute after each trade
            Calcuate Gross and Net Profit/loss'''
            if not trade.isclosed:
                return
            if self.params.optimise == 0:
                self.log(f"Operational profit, Gross: {trade.pnl:.2f}, Net: {trade.pnlcomm:.2f}")


    def stop(self):
        if self.params.optimise != 0:
            self.log(f'///// Param: { self.params.stop_atr_multiple } | Ending value: { self.broker.getvalue() } \\\\\\\\\\')

