"""Overview page in dash app.

Intended as a direct replacement for original visualisation as an interim measure:
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

from .. import log
from ..figures import (
    generate_agent_activity_breakdown_fig,
    generate_balancing_market_fig,
    generate_dsr_commands_fig,
    generate_energy_deficit_fig,
    generate_ev_charging_breakdown_fig,
    generate_intraday_market_sys_fig,
    generate_total_dem_fig,
    generate_total_gen_fig,
)
from ..layout import GridBuilder

dash.register_page(__name__)

df = pd.DataFrame({"Col": [0]})

total_gen_fig = generate_total_gen_fig(df)
total_dem_fig = generate_total_dem_fig(df)
energy_deficit_fig = generate_energy_deficit_fig(df)
balancing_market_fig = generate_balancing_market_fig(df)
intraday_market_sys_fig = generate_intraday_market_sys_fig(df)
dsr_commands_fig = generate_dsr_commands_fig(df)
agent_activity_breakdown_fig = generate_agent_activity_breakdown_fig(df)
ev_charging_breakdown_fig = generate_ev_charging_breakdown_fig(df)

grid = GridBuilder(rows=4, cols=2)
grid.add_element(
    dcc.Graph(
        id="ov-generation",
        figure=total_gen_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=0,
    col=0,
)
grid.add_element(
    dcc.Graph(
        id="ov-demand",
        figure=total_dem_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=1,
    col=0,
)
grid.add_element(
    dcc.Graph(
        id="ov-energy-deficit",
        figure=energy_deficit_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=2,
    col=0,
)
grid.add_element(
    dcc.Graph(
        id="ov-bm",
        figure=balancing_market_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=0,
    col=1,
)
grid.add_element(
    dcc.Graph(
        id="ov-id",
        figure=intraday_market_sys_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=1,
    col=1,
)
grid.add_element(
    dcc.Graph(
        id="ov-dsr",
        figure=dsr_commands_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=2,
    col=1,
)
grid.add_element(
    dcc.Graph(
        id="ov-agent-waffle",
        figure=agent_activity_breakdown_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=3,
    col=0,
)
grid.add_element(
    dcc.Graph(
        id="ov-ev-waffle",
        figure=ev_charging_breakdown_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=3,
    col=1,
)
layout = grid.layout


@callback(
    [
        Output("ov-generation", "figure"),
        Output("ov-demand", "figure"),
        Output("ov-energy-deficit", "figure"),
        Output("ov-bm", "figure"),
        Output("ov-id", "figure"),
        Output("ov-dsr", "figure"),
        Output("ov-agent-waffle", "figure"),
        Output("ov-ev-waffle", "figure"),
    ],
    [Input("figure_interval", "data")],
)
def update_figures(
    n_intervals: int,
) -> tuple[
    px.line, px.line, px.line, go.Figure, go.Figure, px.line, go.Figure, go.Figure
]:
    """Function to update the plots in this page.

    Args:
        n_intervals (int): The number of times this page has updated.
            indexes by 1 every interval.

    Returns:
        tuple[px.line,
        px.line,
        px.line,
        go.Figure,
        go.Figure,
        px.line,
        go.Figure,
        go.Figure]:
            The new figures.
    """
    from ..data import DF_OPAL

    total_gen_fig = generate_total_gen_fig(DF_OPAL)
    total_dem_fig = generate_total_dem_fig(DF_OPAL)
    energy_deficit_fig = generate_energy_deficit_fig(DF_OPAL)
    balancing_market_fig = generate_balancing_market_fig(DF_OPAL)
    intraday_market_sys_fig = generate_intraday_market_sys_fig(DF_OPAL)
    dsr_commands_fig = generate_dsr_commands_fig(DF_OPAL)
    agent_activity_breakdown_fig = generate_agent_activity_breakdown_fig(DF_OPAL)
    ev_charging_breakdown_fig = generate_ev_charging_breakdown_fig(DF_OPAL)

    log.debug("Updating figures on Overview page")
    return (
        total_gen_fig,
        total_dem_fig,
        energy_deficit_fig,
        balancing_market_fig,
        intraday_market_sys_fig,
        dsr_commands_fig,
        agent_activity_breakdown_fig,
        ev_charging_breakdown_fig,
    )
