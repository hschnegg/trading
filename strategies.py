from datetime import timedelta
import backtrader as bt
import math


class ID_NR4(bt.Strategy):
    params = (
        ('optimise', 0),
        ('stop_atr_multiple', 2.5),)


    def __init__(self):
        # Existing orders
        self.order = dict()

        # ID/NR4 indicators
        self.inds = dict()
        for i, d in enumerate(self.datas):
            self.order[d] = None
            self.inds[d] = dict()
            self.inds[d]['tr'] = bt.indicators.TrueRange()
            self.inds[d]['atr'] = bt.indicators.AverageTrueRange(d)
            self.inds[d]['nr4'] = bt.indicators.MinN(self.inds[d]['tr'], period=4)


    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        print(f'{ dt.isoformat() } { txt }')

    def next(self):
        self.signs = dict()
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            self.signs[d] = dict()
            
            status = (f'===== { dn } | '
                      f'L: { d.low[0] } | '
                      f'O: { d.open[0] } | '
                      f'C: { d.close[0] } | '
                      f'H: { d.high[0] } ===== ')

            if self.order[d]:
                status = status + ' Pending Order'
                if self.params.optimise == 0:
                    self.log(status, dt)
                return
                
            if self.position:
                status = status + ' In Trade'
                if self.params.optimise == 0:
                    self.log(status, dt)
                return
    
            if self.params.optimise == 0:
                self.log(status, dt)

            # ID/NR4 signals
            self.signs[d]['is_nr4'] = self.inds[d]['nr4'][0] == self.inds[d]['tr'][0]
            self.signs[d]['is_id'] = ((d.high[0] < d.high[-1]) and
                                      (d.low[0] > d.low[-1]))
            self.signs[d]['buy_signal'] = self.signs[d]['is_nr4'] and self.signs[d]['is_id']
            self.signs[d]['buy_price'] = d.high[0]
            self.signs[d]['low_stop'] = d.low[0]
            self.signs[d]['limit_stop'] = self.params.stop_atr_multiple * self.inds[d]['atr']
            self.signs[d]['size'] = round(100 / (self.signs[d]['buy_price'] - self.signs[d]['low_stop']), 2)
    
            if self.signs[d]['buy_signal']:
                if self.params.optimise == 0:
                    self.log(f'+++++ { dn } | Size { self.signs[d]["size"] } | Buy Price { self.signs[d]["buy_price"] } | Low Stop { self.signs[d]["low_stop"] } | Limit Stop { self.signs[d]["limit_stop"] } +++++', dt)
            
                mainside = self.buy(data=d,
                                    size=self.signs[d]['size'],
                                    exectype=bt.Order.StopLimit,
                                    plimit=self.signs[d]['buy_price'],
                                    valid=d.datetime.date(0) + timedelta(days=3),
                                    transmit=False)
                lowside  = self.sell(data=d,
                                     price=self.signs[d]['low_stop'],
                                     size=mainside.size,
                                     exectype=bt.Order.Stop,
                                     transmit=False,
                                     parent=mainside)
                trailside = self.sell(data=d,
                                      size=mainside.size,
                                      exectype=bt.Order.StopTrail,
                                      trailamount=self.signs[d]['limit_stop'],
                                      transmit=True,
                                      parent=mainside)


    def notify_order(self, order):
        d = order.data
        if order.status in [order.Submitted, order.Accepted]:
            self.order[d] = 'Submitted'
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                if self.params.optimise == 0:
                    self.log(f'{ d._name } - BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                if self.params.optimise == 0:
                    self.log(f'{ d._name } - SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            if self.params.optimise == 0:
                self.log(f'{ d._name } - Order Canceled/Margin/Rejected')

        # Reset orders
        self.order[d] = None


        def notify_trade(self, trade):
            '''Execute after each trade
            Calcuate Gross and Net Profit/loss'''
            if not trade.isclosed:
                return
            if self.params.optimise == 0:
                self.log(f'Operational profit, Gross: { trade.pnl:.2f }, Net: { trade.pnlcomm:.2f }')


    def stop(self):
        if self.params.optimise != 0:
            self.log(f'///// Param: { self.params.stop_atr_multiple } | Ending value: { self.broker.getvalue() } \\\\\\\\\\')

