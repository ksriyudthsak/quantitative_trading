# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import warnings
warnings.filterwarnings("ignore")
import os 
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import backtrader as bt
import pyfolio as pf
from backtesting.strategy.trend import SmaCrossOver, EmaCrossOver, SmaCrossUpStopLoss, EmaSmaCrossOver
from backtesting.strategy.mean_reversion import SimpleMeanReversion
from backtesting.create_portfolio import create_portfolio
from backtesting.run_analyser import TradeClosed


def execute(selected_instrument, selected_strategy,
            start_date='2010-01-01', start_date_oss='2017-01-01', end_date='2021-12-01', 
            cash=100000.0, commission=0.001, slippage=0.005
            ):
    print("*"*20, "run_optimiser", "*"*20)
    def str_to_class(classname):
        return getattr(sys.modules[__name__], classname)
    strategy = str_to_class(selected_strategy)

    print("strategy: {}".format(strategy))
    print("instrument: {}".format(selected_instrument))
    # set up engine
    cerebro = bt.Cerebro()

    # add strategy
    cerebro.optstrategy(strategy, pfast=range(9,10), pslow=range(20,30))

    # add analyser
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(TradeClosed, _name="trade_closed")

    # download data and add to backtest system
    data = bt.feeds.PandasData(dataname=yf.download(selected_instrument, start_date, end_date))
    cerebro.adddata(data, name="test")

    # set cash
    cerebro.broker.setcash(cash=cash) # 100000.0

    # set commission
    cerebro.broker.setcommission(commission=commission) # 0.001 => 0.1%

    # set slippage
    cerebro.broker.set_slippage_perc(slippage)  # 0.005 => 0.5%
    
    # print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # run backtest
    opt_runs = cerebro.run()

    startcash = cash
    # Generate results list
    final_results_list = []
    for run in opt_runs:
        for strategy in run:
            value = round(strategy.broker.get_value(),2)
            PnL = round(value - startcash,2)
            pfast = strategy.params.pfast
            pslow = strategy.params.pslow
            final_results_list.append([pfast,pslow,PnL])

    #Sort Results List
    by_period = sorted(final_results_list, key=lambda x: x[0])
    by_PnL = sorted(final_results_list, key=lambda x: x[2], reverse=True)

    #Print results
    print('Results: Ordered by period:')
    for result in by_period:
        print('pfast: {}, pslow: {}, PnL: {}'.format(result[0], result[1], result[2]))
    print('Results: Ordered by Profit:')
    for result in by_PnL:
        print('pfast: {}, pslow: {}, PnL: {}'.format(result[0], result[1], result[2]))

    # print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    df_result = pd.DataFrame(final_results_list, columns=["fast","slow","PnL"])

    return df_result
