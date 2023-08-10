"""Page in dash app."""

import dash  # type: ignore
import numpy as np
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore

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
        html.H1("Plot 5"),
        dcc.Graph(id="graph5", figure=figure),
        dcc.Interval(id="interval", interval=interval),
    ]
)


@callback(Output("graph5", "extendData"), [Input("interval", "n_intervals")])
def update_data(n_intervals):  # type: ignore # noqa
    if n_intervals is None:
        raise PreventUpdate
    index = n_intervals % resolution
    # tuple is (dict of new data, target trace index, number of points to keep)
    return dict(x=[[x[index]]], y=[[y[index]]]), [0], 10
