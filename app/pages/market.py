"""Market view page in dash app.

Six plots (2x3):
- Intra-day market system
- Balancing market
- Energy deficit
- Intraday market bids and offers
- Demand side response
- DSR commands to agents.
"""


import dash  # type: ignore
import pandas as pd
import plotly.express as px  # type: ignore
from dash import Input, Output, callback, dcc, html  # type: ignore
from plotly import graph_objects as go  # type: ignore

from ..figures import (
    generate_balancing_market_fig,
    generate_dsr_commands_fig,
    generate_dsr_fig,
    generate_energy_deficit_fig,
    generate_intraday_market_bids_fig,
    generate_intraday_market_sys_fig,
)

dash.register_page(__name__)

df = pd.DataFrame({"Col": [0]})

intraday_market_sys_fig = generate_intraday_market_sys_fig(df)
balancing_market_fig = generate_balancing_market_fig(df)
energy_deficit_fig = generate_energy_deficit_fig(df)
intraday_market_bids_fig = generate_intraday_market_bids_fig(df)
dsr_fig = generate_dsr_fig(df)
dsr_commands_fig = generate_dsr_commands_fig(df)

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
                    style={"width": "32%"},
                    children=[
                        html.H1(
                            "Intra-day Market System", style={"textAlign": "center"}
                        ),
                        dcc.Graph(
                            id="graph-intraday-market-sys",
                            figure=intraday_market_sys_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "32%"},
                    children=[
                        html.H1("Balancing Market", style={"textAlign": "center"}),
                        dcc.Graph(
                            id="graph-balancing-market",
                            figure=balancing_market_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "32%"},
                    children=[
                        html.H1("Energy Deficit", style={"textAlign": "center"}),
                        dcc.Graph(
                            id="graph-energy-deficit",
                            figure=energy_deficit_fig,
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
                    style={"width": "32%"},
                    children=[
                        html.H1(
                            "Intraday Market Bids and Offers",
                            style={"textAlign": "center"},
                        ),
                        dcc.Graph(
                            id="table-intraday-market-bids",
                            figure=intraday_market_bids_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "32%"},
                    children=[
                        html.H1("Demand Side Response", style={"textAlign": "center"}),
                        dcc.Graph(
                            id="graph-dsr",
                            figure=dsr_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "32%"},
                    children=[
                        html.H1(
                            "DSR Commands to Agents", style={"textAlign": "center"}
                        ),
                        dcc.Graph(
                            id="graph-dsr-commands",
                            figure=dsr_commands_fig,
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
        Output("graph-intraday-market-sys", "figure"),
        Output("graph-balancing-market", "figure"),
        Output("graph-energy-deficit", "figure"),
        Output("table-intraday-market-bids", "figure"),
        Output("graph-dsr", "figure"),
        Output("graph-dsr-commands", "figure"),
    ],
    [Input("data_opal", "data")],
)
def update_figures(
    data_opal: list[dict[str, object]],
) -> tuple[go.Figure, go.Figure, px.line, go.Figure, go.Figure, px.line]:
    """Function to update the plots in this page.

    Args:
        data_opal (list): Opal data

    Returns:
        tuple[go.Figure, go.Figure, px.line, go.Figure, go.Figure, px.line]:
            The new figures.
    """
    df_opal = pd.DataFrame(data_opal)

    intraday_market_sys_fig = generate_intraday_market_sys_fig(df_opal)
    balancing_market_fig = generate_balancing_market_fig(df_opal)
    energy_deficit_fig = generate_energy_deficit_fig(df_opal)
    intraday_market_bids_fig = generate_intraday_market_bids_fig(df_opal)
    dsr_fig = generate_dsr_fig(df)  # TODO: replace with df_dsr when available
    dsr_commands_fig = generate_dsr_commands_fig(df_opal)
    return (
        intraday_market_sys_fig,
        balancing_market_fig,
        energy_deficit_fig,
        intraday_market_bids_fig,
        dsr_fig,
        dsr_commands_fig,
    )
