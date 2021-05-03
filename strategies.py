import backtrader as bt


class ID_NR4(bt.Strategy):

    params = (('stop_atr_multiple', 1), )

    def __init__(self):
        self.tr = bt.indicators.TrueRange()
        self.atr = bt.indicators.AverageTrueRange(self.data)
        self.nr4 = bt.indicators.MinN(self.tr, period=4)
        

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{ dt.isoformat() } { txt }')


    def next(self):
        self.is_nr4 = self.nr4[0] == self.tr[0]
        self.is_id = ((self.datas[0].high[0] < self.datas[0].high[-1]) and
                      (self.datas[0].low[0] > self.datas[0].low[-1]))
        self.buy_signal = self.is_nr4 and self.is_id
        self.buy_price = self.datas[0].high[0]
        self.buy_stop = self.params.stop_atr_multiple * self.atr

        # self.log(f' { self.is_id }')
        
        self.log(f'High: { self.datas[0].high[0] } Buy Price: { self.buy_price if self.buy_signal else None } Buy Stop: { self.buy_stop if self.buy_signal else None } ')
