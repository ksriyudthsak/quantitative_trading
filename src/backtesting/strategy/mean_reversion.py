from __future__ import absolute_import, division, print_function, unicode_literals

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import backtrader as bt
import pyfolio as pf
import math

class SimpleMeanReversion(bt.Strategy):
 
    '''
    This is a simple mean reversion bollinger band strategy.
 
    Entry Critria:
        - Long:
            - Price closes below the lower band
            - Stop Order entry when price crosses back above the lower band
        - Short:
            - Price closes above the upper band
            - Stop order entry when price crosses back below the upper band
    Exit Critria
        - Long/Short: Price touching the median line
    '''
 
    params = (
        ("period", 20),
        ("devfactor", 2),
        ("size", 20)
        )
 
    def __init__(self):
        self.boll = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        #self.sx = bt.indicators.CrossDown(self.data.close, self.boll.lines.top)
        #self.lx = bt.indicators.CrossUp(self.data.close, self.boll.lines.bot)
 
    def next(self):
        orders = self.broker.get_orders_open() 
        # Cancel open orders so we can track the median line
        if orders:
            for order in orders:
                self.broker.cancel(order)
 
        if not self.position:
            if self.data.close > self.boll.lines.top:
 
                self.sell(exectype=bt.Order.Stop, price=self.boll.lines.top[0], size=self.p.size)
            if self.data.close < self.boll.lines.bot:
                self.buy(exectype=bt.Order.Stop, price=self.boll.lines.bot[0], size=self.p.size)
        else:
            if self.position.size > 0:
                self.sell(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)
 
            else:
                self.buy(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)
 
    def notify_trade(self,trade):
        if trade.isclosed:
            dt = self.data.datetime.date()
 