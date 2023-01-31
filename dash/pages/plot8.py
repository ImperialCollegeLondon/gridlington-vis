import dash
from dash import html, dcc, callback, Input, Output
from dash.exceptions import PreventUpdate

import numpy as np

from dash.dependencies import Input, Output

dash.register_page(__name__)


# Example data (a circle). See https://stackoverflow.com/a/63681810 for more including
# how to increase refresh rate.

##################
resolution = 30
interval = 100
colour = "#EF963B"
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
        html.H1("Plot 8"),
        dcc.Graph(id="graph", figure=figure),
        dcc.Interval(id="interval", interval=interval),
    ]
)


@callback(Output("graph", "extendData"), [Input("interval", "n_intervals")])
def update_data(n_intervals):
    if n_intervals is None:
        raise PreventUpdate
    index = n_intervals % resolution
    # tuple is (dict of new data, target trace index, number of points to keep)
    return dict(x=[[x[index]]], y=[[y[index]]]), [0], 10
