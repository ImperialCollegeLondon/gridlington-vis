"""ESO view - Markets and Reserve.

Four plots (2x2):
- Weather
- Balancing Market
- Intra-day Market System
- Reserve/Standby Generation
"""


import dash  # type: ignore
import pandas as pd
from dash import Input, Output, callback, dcc, html  # type: ignore
from plotly import graph_objects as go  # type: ignore

from ..data import WESIM
from ..figures import (
    generate_balancing_market_fig,
    generate_intraday_market_sys_fig,
    generate_reserve_generation_fig,
    generate_weather_fig,
)

dash.register_page(__name__)

df = pd.DataFrame({"Col": [0]})

weather_fig = generate_weather_fig(WESIM)
balancing_market_fig = generate_balancing_market_fig(df)
intraday_market_sys_fig = generate_intraday_market_sys_fig(df)
reserve_generation_fig = generate_reserve_generation_fig(WESIM)

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
    ],
)


@callback(
    [
        Output("balancing_market_fig", "figure"),
        Output("intraday_market_sys_fig", "figure"),
    ],
    [Input("figure_interval", "n_intervals")],
)
def update_figures(
    n_intervals: int,
) -> tuple[go.Figure, go.Figure]:
    """Function to update the plots in this page.

    Args:
        n_intervals (int): The number of times this page has updated.
            indexes by 1 every 7 seconds.

    Returns:
        tuple[go.Figure, go.Figure]: The new figures.
    """
    from ..data import DF_OPAL

    balancing_market_fig = generate_balancing_market_fig(DF_OPAL)
    intraday_market_sys_fig = generate_intraday_market_sys_fig(DF_OPAL)
    return (
        balancing_market_fig,
        intraday_market_sys_fig,
    )
