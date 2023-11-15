"""Page in dash app."""


import dash  # type: ignore
import pandas as pd
import plotly.express as px  # type: ignore
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore

from .. import LIVE_MODEL, log
from ..datahub_api import get_opal_data
from ..figures import (
    generate_gen_split_fig,
    generate_system_freq_fig,
    generate_total_dem_fig,
    generate_total_gen_fig,
)

dash.register_page(__name__)

##################
interval = 7000
##################

df = pd.DataFrame({"Col": [0]})

gen_split_fig = generate_gen_split_fig(df)
total_gen_fig = generate_total_gen_fig(df)
total_dem_fig = generate_total_dem_fig(df)
system_freq_fig = generate_system_freq_fig(df)

layout = html.Div(
    style={
        "display": "flex",
        "flex-direction": "column",
        "justify-content": "space-around",
    },
    children=[
        html.Div(
            style={"display": "flex", "justify-content": "space-around"},
            children=[
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Generation Split"),
                        dcc.Graph(
                            id="graph-gen-split",
                            figure=gen_split_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Generation Total"),
                        dcc.Graph(
                            id="graph-gen-total",
                            figure=total_gen_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            style={"display": "flex", "justify-content": "space-around"},
            children=[
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Demand Total"),
                        dcc.Graph(
                            id="graph-demand",
                            figure=total_dem_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("System Frequency"),
                        dcc.Graph(
                            id="graph-freq",
                            figure=system_freq_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
            ],
        ),
        dcc.Interval(id="interval", interval=interval),
    ],
)


@callback(
    [
        Output("graph-gen-split", "figure"),
        Output("graph-gen-total", "figure"),
        Output("graph-demand", "figure"),
        Output("graph-freq", "figure"),
    ],
    [Input("interval", "n_intervals")],
)
def update_data(n_intervals: int) -> tuple[px.pie, px.line, px.line, px.line]:
    """Function to update the plots in this page.

    Args:
        n_intervals (int): The number of times this page has updated.
            indexes by 1 every 7 seconds.

    Returns:
        tuple[px.pie, px.line, px.line, px.line]: The new figures.
    """
    if n_intervals is None:
        raise PreventUpdate

    if LIVE_MODEL:
        log.debug("Updating plots from live model")
        data = get_opal_data()
        new_df = pd.DataFrame(**data)  # type: ignore[call-overload]
    else:
        from ..pre_set_data import OPAL_DATA

        log.debug("Updating plots with pre-set data")
        new_df = OPAL_DATA.loc[:n_intervals]

    gen_split_fig = generate_gen_split_fig(new_df)
    total_gen_fig = generate_total_gen_fig(new_df)
    total_dem_fig = generate_total_dem_fig(new_df)
    system_freq_fig = generate_system_freq_fig(new_df)
    return gen_split_fig, total_gen_fig, total_dem_fig, system_freq_fig
