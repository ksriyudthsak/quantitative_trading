import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input, Output
from app_setup import dashapp

layout = dhc.Div([
    dhc.H3('Results'),
    dcc.Dropdown(
        {f'Results - {i}': f'{i}' for i in ['Crossover', 'Reversion', 'Momentum']},
        # id='page-results-dropdown'
    ),
    dhc.Div(id='page-results-display-value'),
    dcc.Link('Go to Main Page', href='/')
])

@dashapp.callback(
    Output('page-results-display-value', 'children'),
    Input('page-results-dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'