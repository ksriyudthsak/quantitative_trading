# -*- coding: utf-8 -*-

from dash import Dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dashapp = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = dashapp.server
dashapp.title = 'Backtest'
