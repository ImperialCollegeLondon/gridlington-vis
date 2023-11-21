"""ESO view – Markets and Reserve.

Four plots (2x2):
- Weather
- Balancing Market
- Intra-day Market System
- Reserve/Standby Generation
"""


import dash  # type: ignore
import pandas as pd
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore
from plotly import graph_objects as go  # type: ignore

from .. import LIVE_MODEL, log
from ..datahub_api import get_opal_data
from ..figures import (
    generate_balancing_market_fig,
    generate_intraday_market_sys_fig,
    generate_reserve_generation_fig,
    generate_weather_fig,
)

dash.register_page(__name__)

##################
interval = 7000
##################

df = pd.DataFrame({"Col": [0]})

weather_fig = generate_weather_fig(df)
balancing_market_fig = generate_balancing_market_fig(df)
intraday_market_sys_fig = generate_intraday_market_sys_fig(df)
reserve_generation_fig = generate_reserve_generation_fig(df)

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
                        html.H1("Weather", style={"textAlign": "center"}),
                        dcc.Graph(
                            id="weather_fig",
                            figure=weather_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Balancing Market", style={"textAlign": "center"}),
                        dcc.Graph(
                            id="balancing_market_fig",
                            figure=balancing_market_fig,
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
                        html.H1(
                            "Intra-day Market System", style={"textAlign": "center"}
                        ),
                        dcc.Graph(
                            id="intraday_market_sys_fig",
                            figure=intraday_market_sys_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1(
                            "Reserve/Standby Generation", style={"textAlign": "center"}
                        ),
                        dcc.Graph(
                            id="reserve_generation_fig",
                            figure=reserve_generation_fig,
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
        Output("weather_fig", "figure"),
        Output("balancing_market_fig", "figure"),
        Output("intraday_market_sys_fig", "figure"),
        Output("reserve_generation_fig", "figure"),
    ],
    [Input("interval", "n_intervals")],
)
def update_data(n_intervals: int) -> tuple[go.Figure, go.Figure, go.Figure, go.Figure]:
    """Function to update the plots in this page.

    Args:
        n_intervals (int): The number of times this page has updated.
            indexes by 1 every 7 seconds.

    Returns:
        tuple[go.Figure, go.Figure, go.Figure, go.Figure]: The new figures.
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

    weather_fig = generate_weather_fig(new_df)
    balancing_market_fig = generate_balancing_market_fig(new_df)
    intraday_market_sys_fig = generate_intraday_market_sys_fig(new_df)
    reserve_generation_fig = generate_reserve_generation_fig(new_df)
    return (
        weather_fig,
        balancing_market_fig,
        intraday_market_sys_fig,
        reserve_generation_fig,
    )
