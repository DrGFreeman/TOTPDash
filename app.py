from datetime import datetime

from dash import Dash
from dash.dependencies import Input
from dash.dependencies import Output
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html

from pyotp import TOTP

default_secret = 'JHCO GO7V CER3 EJ4L'
update_interval = 2

layout = html.Div(
    id='container',
    children=[
        html.H1('000 000', id='totp_token'),
        daq.GraduatedBar(
            id='remaining_bar',
            max=28,
            step=2,
            value=28,
            size=200
        ),
        html.Hr(),
        html.Label("TOTP Secret"),
        dcc.Input(
            id='totp_secret',
            type='text',
            placeholder='Enter TOTP Secret...',
            value=default_secret
        ),
        dcc.Interval(
            id='interval',
            interval=update_interval * 1000,
            n_intervals=0,
        )
    ]
)

app = Dash(__name__)

app.title = 'TOTP'

app.layout = layout


@app.callback([Output('totp_token', 'children'),
               Output('remaining_bar', 'value')],
              [Input('interval', 'n_intervals'),
               Input('totp_secret', 'value')])
def update_totp_token(_, secret):
    try:
        if secret is None or secret == '':
            raise ValueError

        token = TOTP(secret.replace(' ', '')).now()

        remaining = 30 - update_interval - datetime.now().second % 30

        return f"{token[:3]} {token[3:]}", remaining

    except Exception:
        return 'Invalid Secret', 0


if __name__ == '__main__':
    app.run_server()
