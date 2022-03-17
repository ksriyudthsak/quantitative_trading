# -*- coding: utf-8 -*-
# tutorial: https://dash.plotly.com/urls

import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input, Output
from app_setup import dashapp
from page_views import page_main, page_backtest, page_results, page_optimisation

dashapp.layout = dhc.Div([
    dcc.Location(id='url', refresh=False),
    dhc.Div([
        dhc.Button(dcc.Link('MainPage', href='/'), id='mainpage-btn', n_clicks=0, style={'width': '15%', 'margin-left': 0, 'margin-right': '2%'}),
        dhc.Button(dcc.Link('Backtest', href='/page_backtest'), id='backtest-btn', n_clicks=0, style={'width': '15%', 'margin-left': 0, 'margin-right': '2%'}),
        dhc.Button(dcc.Link('Optimisation', href='/page_optimisation'), id='optimisation-btn', n_clicks=0, style={'width': '15%', 'margin-left': 0, 'margin-right': '2%'}),
        dhc.Button(dcc.Link('Results', href='/page_results'), id='result-btn', n_clicks=0, style={'width': '15%', 'margin-left': 0, 'margin-right': '2%'}),
    ]),
    # content will be rendered in this element
    dhc.Div(id='page-content')  
])

@dashapp.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return page_main.layout
    elif pathname == '/page_backtest':
        return page_backtest.layout
    elif pathname == '/page_optimisation':
        return page_optimisation.layout
    elif pathname == '/page_results':
        return page_results.layout
    else:
        return 'This is a main page. Please select what to do.'

if __name__ == '__main__':
    dashapp.run_server(host='0.0.0.0', port=8001, debug=True)
