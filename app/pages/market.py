"""Page in dash app."""


import dash  # type: ignore
import pandas as pd
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore

from .. import datahub_api as datahub
from ..figures import (
    generate_balancing_market_fig,
    generate_dsr_bids_fig,
    generate_dsr_commands_fig,
    generate_energy_deficit_fig,
    generate_intraday_market_bids_fig,
    generate_intraday_market_sys_fig,
)

dash.register_page(__name__)

##################
interval = 7000
##################

df = pd.DataFrame({"Col": [0]})

intraday_market_sys_fig = generate_intraday_market_sys_fig(df)
balancing_market_fig = generate_balancing_market_fig(df)
energy_deficit_fig = generate_energy_deficit_fig(df)
intraday_market_bids_fig = generate_intraday_market_bids_fig(df)
dsr_bids_fig = generate_dsr_bids_fig(df)
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
                    style={"width": "48%"},
                    children=[
                        html.H1("Intra-day Market System"),
                        dcc.Graph(
                            id="graph-intraday-market-sys",
                            figure=intraday_market_sys_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Balancing Market"),
                        dcc.Graph(
                            id="graph-balancing-market",
                            figure=balancing_market_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Energy Deficit"),
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
                    style={"width": "48%"},
                    children=[
                        html.H1("Intraday Market Bids and Offers"),
                        dcc.Graph(
                            id="table-intraday-market-bids",
                            figure=intraday_market_bids_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("DSR Bids and Offers"),
                        dcc.Graph(
                            id="table-dsr-bids",
                            figure=dsr_bids_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("DSR Commands to Agents"),
                        dcc.Graph(
                            id="graph-dsr-commands",
                            figure=dsr_commands_fig,
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
        Output("graph-intraday-market-sys", "figure"),
        Output("graph-balancing-market", "figure"),
        Output("graph-energy-deficit", "figure"),
        Output("table-intraday-market-bids", "figure"),
        Output("table-dsr-bids", "figure"),
        Output("graph-dsr-commands", "figure"),
    ],
    [Input("interval", "n_intervals")],
)
def update_data(n_intervals):  # type: ignore # noqa
    if n_intervals is None:
        raise PreventUpdate

    data_opal = datahub.get_opal_data()
    new_df_opal = pd.DataFrame(**data_opal)

    data_dsr = datahub.get_dsr_data()
    new_df_dsr = pd.DataFrame(**data_dsr)

    intraday_market_sys_fig = generate_intraday_market_sys_fig(new_df_opal)
    balancing_market_fig = generate_balancing_market_fig(new_df_opal)
    energy_deficit_fig = generate_energy_deficit_fig(new_df_opal)
    intraday_market_bids_fig = generate_intraday_market_bids_fig(new_df_opal)
    dsr_bids_fig = generate_dsr_bids_fig(new_df_dsr)
    dsr_commands_fig = generate_dsr_commands_fig(new_df_dsr)
    return (
        intraday_market_sys_fig,
        balancing_market_fig,
        energy_deficit_fig,
        intraday_market_bids_fig,
        dsr_bids_fig,
        dsr_commands_fig,
    )
