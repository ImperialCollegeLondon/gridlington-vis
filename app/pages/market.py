"""Market view page in dash app.

Four plots (2x2):
- Energy deficit
- Intraday market bids and offers
- Demand side response
- DSR commands to agents.
"""


import dash  # type: ignore
import pandas as pd
import plotly.express as px  # type: ignore
from dash import Input, Output, callback, dcc  # type: ignore
from plotly import graph_objects as go  # type: ignore

from ..figures import (
    generate_dsr_commands_fig,
    generate_dsr_fig,
    generate_energy_deficit_fig,
    generate_intraday_market_bids_fig,
)
from ..layout import GridBuilder

dash.register_page(__name__)

df = pd.DataFrame({"Col": [0]})

energy_deficit_fig = generate_energy_deficit_fig(df)
intraday_market_bids_fig = generate_intraday_market_bids_fig(df)
dsr_fig = generate_dsr_fig(df)
dsr_commands_fig = generate_dsr_commands_fig(df)


grid = GridBuilder(rows=2, cols=2)
grid.add_element(
    dcc.Graph(
        id="graph-energy-deficit",
        figure=energy_deficit_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=0,
    col=0,
)
grid.add_element(
    dcc.Graph(
        id="table-intraday-market-bids",
        figure=intraday_market_bids_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=0,
    col=1,
)
grid.add_element(
    dcc.Graph(
        id="graph-dsr",
        figure=dsr_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=1,
    col=0,
)
grid.add_element(
    dcc.Graph(
        id="graph-dsr-commands",
        figure=dsr_commands_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=1,
    col=1,
)
layout = grid.layout


@callback(
    [
        Output("graph-energy-deficit", "figure"),
        Output("table-intraday-market-bids", "figure"),
        Output("graph-dsr", "figure"),
        Output("graph-dsr-commands", "figure"),
    ],
    [Input("figure_interval", "n_intervals")],
)
def update_figures(
    n_intervals: int,
) -> tuple[px.line, go.Figure, go.Figure, px.line]:
    """Function to update the plots in this page.

    Args:
        n_intervals (int): The number of times this page has updated.
            indexes by 1 every 7 seconds.

    Returns:
        tuple[px.line, go.Figure, go.Figure, px.line]:
            The new figures.
    """
    from ..data import DF_OPAL

    energy_deficit_fig = generate_energy_deficit_fig(DF_OPAL)
    intraday_market_bids_fig = generate_intraday_market_bids_fig(DF_OPAL)
    dsr_fig = generate_dsr_fig(df)  # TODO: replace with df_dsr when available
    dsr_commands_fig = generate_dsr_commands_fig(DF_OPAL)
    return (
        energy_deficit_fig,
        intraday_market_bids_fig,
        dsr_fig,
        dsr_commands_fig,
    )
