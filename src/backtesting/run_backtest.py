# -*- coding: utf-8 -*-
# tutorial: https://www.backtrader.com/docu/strategy/

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
from backtesting.strategy.trend import *
from backtesting.strategy.mean_reversion import *
from backtesting.create_portfolio import create_portfolio
from backtesting.run_analyser import TradeClosed


def execute(selected_instrument, selected_strategy,
            start_date='2010-01-01', start_date_oss='2017-01-01', end_date='2021-12-01', 
            cash=100000.0, commission=0.001, slippage=0.005
            ):
    print("*"*20, "run_backtest", "*"*20)
    def str_to_class(classname):
        return getattr(sys.modules[__name__], classname)
    strategy = str_to_class(selected_strategy)

    print("strategy: {}".format(strategy))
    print("instrument: {}".format(selected_instrument))
    # set up engine
    cerebro = bt.Cerebro()

    # add strategy
    cerebro.addstrategy(strategy)

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
    results = cerebro.run()

    # analyse portfolio
    strat = results[0]
    pyfoliozer = strat.analyzers.getbyname('pyfolio')
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()

    # print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # show portfolio
    fig_portfo = pf.create_returns_tear_sheet(
    returns,
    positions=positions,
    transactions=transactions,
    # gross_lev=gross_lev,
    live_start_date=start_date_oss,  # This date is for starting out-of-sample
    # round_trips=True,
    return_fig=True
    )
    fig_name = 'src/output/fig_portfo_{}_{}.png'.format(selected_instrument, selected_strategy)
    plt.savefig(fig_name, format="png", 
               bbox_inches='tight', 
               transparent=True,
               pad_inches=0)

    portfo = create_portfolio(returns=returns,
        positions=positions,
        transactions=transactions,
        gross_lev=gross_lev,
        live_start_date='2021-01-01',
        round_trips=True
        )

    return strat, portfo, fig_portfo
