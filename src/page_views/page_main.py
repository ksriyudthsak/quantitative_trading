import dash_core_components as dcc
import dash_html_components as dhc
import base64

image_filename = 'src/input/pochama.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')    
opening_fig = 'data:image/png;base64,{}'.format(encoded_image)

layout = dhc.Div([
    dhc.H3('Pochama will help you performing backtesting. Let\'s do it!!!'),
    dhc.Div(
        [
            dhc.Img(src=opening_fig, style={'width': '33%'}),
            # dhc.Label('pocha pocha'),
        ],
        # className='row'
    ),    

    dcc.Link('START BACKTESTING', href='/page_backtest'),
])
