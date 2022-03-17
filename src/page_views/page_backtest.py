import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import matplotlib.pyplot as plt
import base64
from app_setup import dashapp
from backtesting import run_backtest

layout = dhc.Div([
    dhc.H3('BACKTEST'), 
    dhc.Div(
        [
        dhc.Div(
            [
            dhc.Label('Strategy'),
            dcc.Dropdown(
                id = 'strategy',
                options = [{'label': i, 'value': i} for i in ['SmaCrossover', 'SimpleMeanReversion', 'Momentum']],
                value = 'SmaCrossover',
                style={
                    'width': '100%','float': 'left','margin': 'auto'
                    }
            ),],
            className='two columns'
        ),    
        dhc.Div([
            dhc.Label('Instrument'),
            dcc.Input(
                id = 'instrument', 
                type = "text", 
                # placeholder = 5,
                value = '9449.T',
                debounce=True,
            ),],
            className='two columns'
        ),
        dhc.Div([
            dhc.Label('Start_date'),
            dcc.Input(
                id = 'start_date', 
                type = "text", 
                value = '2010-01-01',
                debounce=True,
            ),],
            className='two columns'
        ), 
        dhc.Div([
            dhc.Label('Start_date_OOS'),
            dcc.Input(
                id = 'start_date_oos', 
                type = "text", 
                value = '2018-01-01',
                debounce=True,
            ),],
            className='two columns'
        ),        
        dhc.Div([
            dhc.Label('End_date'),
            dcc.Input(
                id = 'end_date', 
                type = "text", 
                value = '2021-12-01',
                debounce=True,
            ),],
            className='two columns'
        ),        
        ], 
        className='row'
    ),
    dhc.Div([
        dhc.Div([
            dhc.Label('Cash'),
            dcc.Input(
                id = 'cash', 
                type = "number", 
                value = 100000.0,
                debounce=True,
            ),],
            className='two columns'
        ),        
        dhc.Div([
            dhc.Label('Commission'),
            dcc.Input(
                id = 'commission', 
                type = "number", 
                value = 0.001,
                debounce=True,
            ),],
            className='two columns'
        ),   
        dhc.Div([
            dhc.Label('Slippage'),
            dcc.Input(
                id = 'slippage', 
                type = "number", 
                value = 0.005,
                debounce=True,
            ),],
            className='two columns'
        ),   
        ], 
        className='row'
    ),
    dhc.Div(
        [
            dcc.Graph(
                id='graph1',
                figure={
                },
            ),
        ],
        className='row'
    ),
    dhc.Div(
        [
            dhc.Label('portfolio'),
            dash_table.DataTable(
                id='table1', 
                style_table={
                    # 'height': 400,
                    'overflowY': 'scroll',
                    'width': 1000
                }
            ),
        ],
    ),    
    dhc.Div(
        [
            dhc.Label('portfolio_figure'),
            dhc.Img(id='image1', style={'width': '75%'}),
        ],
        className='row'
    ),    
    dcc.Link('Back to main pages', href='/'),
]),

@dashapp.callback(
    [
        Output('graph1', 'figure'),
        Output('table1', 'data'),
        Output('table1', 'columns'),
        Output('image1', 'src')
    ], [
        Input('instrument', 'value'),
        Input('strategy', 'value'),
        Input('start_date', 'value'),
        Input('start_date_oos', 'value'),
        Input('end_date', 'value'),
        Input('cash', 'value'),
        Input('commission', 'value'),
        Input('slippage', 'value'),
    ])
def update_figure(instrument, strategy, start_date, start_date_oos, end_date, cash, commission, slipage):
    print("start backtest")
    print(instrument, strategy, start_date, end_date, cash, commission, slipage)

    # run backtest
    strat, portfo, fig_portfo = run_backtest.execute(instrument, strategy, start_date, start_date_oos, end_date, cash, commission, slipage)

    # process data
    pyfoliozer = strat.analyzers.getbyname('pyfolio')
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    df_position = positions.reset_index()   
    df_position = df_position.rename(columns={'test': 'value'})

    # analyse data
    trade_dict = strat.analyzers.getbyname("trade_closed").get_analysis()
    columns_df = [
            "DateClosed",
            "Ticker",
            "PnL",
            "PnLComm",
            "Commission",
            "DaysOpen",
            "Status",
        ]
    df_analyse = pd.DataFrame(trade_dict)
    df_analyse = df_analyse.T
    df_analyse.columns = columns_df    

    df_rawdata = pyfoliozer.datas[0]._dataname.reset_index()
    return_ordereddict = pyfoliozer._returns.rets
    df_return = pd.DataFrame.from_dict(return_ordereddict, orient="index").reset_index()
    df_return = df_return.rename(columns={"index":"date", 0:"returns"})
    transactions_ordereddictlist = pyfoliozer._transactions.rets
    df_transactions = pd.DataFrame(transactions_ordereddictlist, columns=transactions_ordereddictlist.keys())
    df_transactions = df_transactions.explode(list(df_transactions.columns)).T.reset_index()
    df_transactions.columns = df_transactions.iloc[0]
    df_transactions = df_transactions[1:]

    # get indicator
    df_indicator = df_rawdata.Date.to_frame()
    line_label = []

    # inds = strat.getindicators()
    # ind = inds[0]
    # st_dtime = strat.lines.datetime.plot()
    # line_data = ind.lines
    # line_label = ind.lines._getlines()
    # for i, l in enumerate(line_label):
    #     df_indicator[l] = line_data.lines[i].array.tolist()

    label_len = len(strat.getindicators_lines())
    for i in range(label_len):   
        label_name = "{}{}{}".format(strat.getindicators_lines()[i]._getlines()[0],
                            strat.getindicators_lines()[i].params._getvalues())
        df_indicator[label_name] = strat.getindicators_lines()[i].array.tolist()
        line_label.append(label_name)

    # plot backtest
    fig = go.Figure()
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        # subplot_titles=('Cash', 'PnL', 'Chart'),
                        vertical_spacing=0.01,
                        row_heights=[0.2, 0.2, 0.6],
                        specs=[[{'secondary_y': True}] * 1] * 3
                        )
    fig.add_trace(go.Bar(x=df_rawdata.Date, y=df_rawdata.Volume, 
                    name='volume', marker_color="black"
                    ), row=3, col=1, secondary_y=False)
    
    for i in range(len(line_label)):
        fig.add_trace(go.Scatter(x=df_indicator.Date, y=df_indicator[line_label[i]], 
                    name=line_label[i]
                    ), row=3, col=1, secondary_y=True)
                    
    fig.add_trace(go.Candlestick(x=df_rawdata.Date,
                                open=df_rawdata.Open,
                                high=df_rawdata.High,
                                low=df_rawdata.Low,
                                close=df_rawdata.Close,
                                name='ohlc'), row=3,col=1, secondary_y=True)    

    fig.add_trace(go.Scatter(x=df_transactions.date, y=df_transactions.price, 
                    name='trade', mode="markers", marker_color=df_transactions.amount
                    ),  row=3, col=1, secondary_y=True)

    # fig.add_trace(go.Scatter(x=df_transactions.date, y=df_transactions.price, 
    #                 name='trade', mode="markers", marker_color=df_transactions.amount
    #                 ),  row=2, col=1, secondary_y=False)
    # fig.add_trace(go.Scatter(x=df_return.date, y=df_return.returns, 
    #                 name='return', marker_color="blue"
    #                 ), row=1, col=1, secondary_y=False)


    fig.add_trace(go.Scatter(x=df_analyse.DateClosed, y=df_analyse.PnL, 
                    name='PnL', mode="markers", marker_color=df_analyse.Status
                    ),  row=2, col=1, secondary_y=True)
    fig.add_trace(go.Scatter(x=df_analyse.DateClosed, y=df_analyse.PnLComm, 
                    name='PnLComm', mode="markers", marker_color=df_analyse.Status
                    ),  row=2, col=1, secondary_y=True)                    
    fig.add_trace(go.Bar(x=df_analyse.DateClosed, y=df_analyse.Commission, 
                    name='Commission', marker_color="black"
                    ),  row=2, col=1, secondary_y=False)

    fig.add_trace(go.Scatter(x=df_position.Datetime, y=df_position.cash, 
                    name='cash', marker_color="blue"
                    ), row=1, col=1, secondary_y=False)
    # fig.add_trace(go.Scatter(x=df_position.Datetime, y=df_position.value, 
    #                 name='value', marker_color="red"
    #                 ), row=1, col=1, secondary_y=False)

    fig.update_layout(
        title='backtest',
        height=800,
        hovermode="x",
        # xaxis_rangeslider_visible=False
        # showlegend=False,
        # transition_duration=500,
    )         
    fig.update_yaxes(fixedrange=False)
    # Update yaxis properties
    fig.update_yaxes(title_text="Cash", row=1, col=1)
    fig.update_yaxes(title_text="PnL", row=2, col=1)
    fig.update_yaxes(title_text="Chart", row=3, col=1)

    # show portfolio table
    columns = [{'name': col, 'id': col} for col in portfo.columns]
    data = portfo.to_dict(orient='records')

    # show portfolio figure
    port_png = 'src/output/fig_portfo_{}_{}.png'.format(instrument, strategy)
    port_fig = base64.b64encode(open(port_png, 'rb').read()).decode('ascii')    
    port_fig = 'data:image/png;base64,{}'.format(port_fig)

    return fig, data, columns, port_fig
