"""ESO view - Markets and Reserve.

Four plots (2x2):
- Weather
- Balancing Market
- Intra-day Market System
- Reserve/Standby Generation
"""


import dash  # type: ignore
import pandas as pd
import plotly.express as px  # type: ignore
from dash import Input, Output, callback, dcc, html  # type: ignore
from plotly import graph_objects as go  # type: ignore

from ..figures import (
    generate_balancing_market_fig,
    generate_intraday_market_sys_fig,
    generate_reserve_generation_fig,
    generate_weather_fig,
)

dash.register_page(__name__)

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
    ],
)


@callback(
    [
        Output("weather_fig", "figure"),
        Output("balancing_market_fig", "figure"),
        Output("intraday_market_sys_fig", "figure"),
        Output("reserve_generation_fig", "figure"),
    ],
    [Input("data_opal", "data")],
)
def update_figures(
    data_opal: list[dict[str, object]],
) -> tuple[go.Figure, go.Figure, go.Figure, px.line]:
    """Function to update the plots in this page.

    Args:
        data_opal (list): Opal data

    Returns:
        tuple[go.Figure, go.Figure, go.Figure, px.line]: The new figures.
    """
    df_opal = pd.DataFrame(data_opal)

    weather_fig = generate_weather_fig(df_opal)
    balancing_market_fig = generate_balancing_market_fig(df_opal)
    intraday_market_sys_fig = generate_intraday_market_sys_fig(df_opal)
    reserve_generation_fig = generate_reserve_generation_fig(df_opal)
    return (
        weather_fig,
        balancing_market_fig,
        intraday_market_sys_fig,
        reserve_generation_fig,
    )
