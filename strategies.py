import backtrader as bt


class ID_NR4(bt.Strategy):
    '''Street SMart, p. 166'''

    params = (('stop_atr_multiple', 1), )

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
        self.log(f'===== L:{ self.datas[0].low[0] } | H: { self.datas[0].high[0] } =====')
        # print(self.order)
        # print(self.position)
        
        # ID/NR4 signals
        self.is_nr4 = self.nr4[0] == self.tr[0]
        self.is_id = ((self.datas[0].high[0] < self.datas[0].high[-1]) and
                          (self.datas[0].low[0] > self.datas[0].low[-1]))
        self.buy_signal = self.is_nr4 and self.is_id
        self.buy_price = self.datas[0].high[0]
        self.buy_stop = self.params.stop_atr_multiple * self.atr
        # self.stop_percent = self.buy_stop / self.buy_price

        if self.order:
            return

        if not self.position:
            if self.buy_signal:
                self.log(f'BUY CREATE { self.buy_price }')
                self.order = self.buy(exectype=bt.Order.StopLimit,
                                      plimit=self.buy_price)
                                       
        else:
            pass
            # self.log(f'CLOSE CREATE { self.datas[0].close[0] }')
            # self.order = self.sell(exectype=bt.Order.StopTrail,
            #                        trailpercent=self.buy_stop)
            

        # self.log(f'High: { self.datas[0].high[0] } Buy Price: { self.buy_price if self.buy_signal else None } Buy Stop: { self.buy_stop if self.buy_signal else None } ')


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
