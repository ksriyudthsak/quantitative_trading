from __future__ import absolute_import, division, print_function, unicode_literals

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import backtrader as bt
import pyfolio as pf
import math


class Momentum(bt.Strategy):
    params = dict()
 
    def __init__(self):

 
    def next(self):
