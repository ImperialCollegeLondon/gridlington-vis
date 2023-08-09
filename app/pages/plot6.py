import dash
import numpy as np
from dash import Input, Output, callback, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

dash.register_page(__name__)


# Example data (a circle). See https://stackoverflow.com/a/63681810 for more including
# how to increase refresh rate.

##################
resolution = 30
interval = 100
colour = "#0D76BF"
##################

t = np.linspace(0, np.pi * 2, resolution)
x, y = np.cos(t), np.sin(t)
# Example app.
figure = dict(
    data=[{"x": [], "y": []}],
    layout=dict(
        xaxis=dict(range=[-1, 1]),
        yaxis=dict(range=[-1, 1]),
        colorway=[colour],
    ),
)

layout = html.Div(
    [
        html.H1("Plot 6"),
        dcc.Graph(id="graph6", figure=figure),
        dcc.Interval(id="interval", interval=interval),
    ]
)


@callback(Output("graph6", "extendData"), [Input("interval", "n_intervals")])
def update_data(n_intervals):
    if n_intervals is None:
        raise PreventUpdate
    index = n_intervals % resolution
    # tuple is (dict of new data, target trace index, number of points to keep)
    return dict(x=[[x[index]]], y=[[y[index]]]), [0], 10
