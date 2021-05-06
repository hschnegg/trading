from datetime import timedelta
import backtrader as bt


class ID_NR4(bt.Strategy):
    '''Street SMart, p. 166'''

    params = (('stop_atr_multiple', 2), )

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
        self.log(f'===== L:{ self.datas[0].low[0] } | C: { self.datas[0].close[0] } | H: { self.datas[0].high[0] } =====')
        
        # ID/NR4 signals
        self.is_nr4 = self.nr4[0] == self.tr[0]
        self.is_id = ((self.datas[0].high[0] < self.datas[0].high[-1]) and
                          (self.datas[0].low[0] > self.datas[0].low[-1]))
        self.buy_signal = self.is_nr4 and self.is_id
        self.buy_price = self.datas[0].high[0]
        self.low_stop = self.datas[0].low[0]
        self.limit_stop = self.params.stop_atr_multiple * self.atr

        if self.order:
            return

        if not self.position:
            if self.buy_signal:
                
                self.log(f'----- Buy Price { self.buy_price } | Low Stop { self.low_stop } | Limit Stop { self.limit_stop } -----')
            
                mainside = self.buy(exectype=bt.Order.StopLimit,
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
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Reset orders
        self.order = None
