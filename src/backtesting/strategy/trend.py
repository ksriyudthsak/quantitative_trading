from __future__ import absolute_import, division, print_function, unicode_literals

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import backtrader as bt
import pyfolio as pf
import math


class SmaCrossOver(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=25   # period for the slow moving average
    )

    def __init__(self):
        fast_sma = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        slow_sma = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(fast_sma, slow_sma)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

class EmaCrossOver(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=9,  # period for the fast moving average
        pslow=20   # period for the slow moving average
    )

    def __init__(self):
        fast_ema = bt.ind.EMA(period=self.p.pfast)  # fast moving average
        slow_ema = bt.ind.EMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(fast_ema, slow_ema)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

class EmaSmaCrossOver(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=9,  # period for the fast moving average
        pslow=20   # period for the slow moving average
    )

    def __init__(self):
        fast_ema = bt.ind.EMA(period=self.p.pfast)  # fast moving average
        slow_sma = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(fast_ema, slow_sma)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

class SmaCrossUp(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self):
        fast_sma = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        slow_sma = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossup = bt.ind.CrossUp(fast_sma, slow_sma)  # crossup signal

class SmaCrossUpStopLoss(SmaCrossUp):
    # https://www.backtrader.com/blog/posts/2018-02-01-stop-trading/stop-trading/
    params = dict(
        stop_loss=0.1,  # 0.02 price is 2% less than the entry point
        trail=False,
    )

    def notify_order(self, order):
        if not order.status == order.Completed:
            return  # discard any other notification

        if not self.position:  # we left the market
            print('SELL@price: {:.2f}'.format(order.executed.price))
            return

        # We have entered the market
        print('BUY @price: {:.2f}'.format(order.executed.price))

        if not self.p.trail:
            stop_price = order.executed.price * (1.0 - self.p.stop_loss)
            self.sell(exectype=bt.Order.Stop, price=stop_price)
        else:
            self.sell(exectype=bt.Order.StopTrail, trailamount=self.p.trail)

    def next(self):
        if not self.position and self.crossup > 0:
            # not in the market and signal triggered
            self.buy()  