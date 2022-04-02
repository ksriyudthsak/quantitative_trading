import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input, Output
from app_setup import dashapp
from backtesting import run_optimiser

layout = dhc.Div([
    dhc.H3('Optimisation'),
    dcc.Dropdown(
        {f'Optimisation - {i}': f'{i}' for i in ['GridSearch', 'GeneticsAlgorithm']},
        # id='page-optimisation-dropdown'
    ),
    dhc.Div(id='page-optimisation-display-value'),
    dcc.Link('Go to Main Page', href='/')
])

@dashapp.callback(
    Output('page-optimisation-display-value', 'children'),
    Input('page-optimisation-dropdown', 'value'))
def display_value(instrument, strategy, start_date, start_date_oos, end_date, cash, commission, slipage):

    # run optimisation
    df_result = run_optimiser.execute(instrument, strategy, start_date, start_date_oos, end_date, cash, commission, slipage)

    columns = [{'name': col, 'id': col} for col in df_result.columns]
    data = df_result.to_dict(orient='records')
    return data, columns