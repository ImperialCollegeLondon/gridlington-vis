"""Agent view page in dash app.

Five plots:
- Agent and EV Locations
- Agent and EV Locations on SLD
- Agent Activity Breakdown
- Electric Vehicle Charging Breakdown
- DSR commands to agents
"""

import dash  # type: ignore
import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
from dash import Input, Output, callback, dcc  # type: ignore

from .. import log
from ..figures import (
    generate_agent_activity_breakdown_fig,
    generate_dsr_commands_fig,
    generate_ev_charging_breakdown_fig,
    generate_map_fig,
    generate_sld_fig,
)
from ..layout import GridBuilder

dash.register_page(__name__)

df = pd.DataFrame({"Col": [0]})

sld_fig = generate_sld_fig(df)
map_fig = generate_map_fig(df)
agent_activity_breakdown_fig = generate_agent_activity_breakdown_fig(df)
ev_charging_breakdown_fig = generate_ev_charging_breakdown_fig(df)
dsr_commands_fig = generate_dsr_commands_fig(df)

grid = GridBuilder(rows=2, cols=3)
grid.add_element(
    dcc.Graph(
        id="map_fig",
        figure=map_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=0,
    col=1,
)
grid.add_element(
    dcc.Graph(
        id="sld_fig",
        figure=sld_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=0,
    col=0,
)
grid.add_element(
    dcc.Graph(
        id="agent_activity_breakdown_fig",
        figure=agent_activity_breakdown_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=1,
    col=0,
)
grid.add_element(
    dcc.Graph(
        id="ev_charging_breakdown_fig",
        figure=ev_charging_breakdown_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=1,
    col=1,
)
grid.add_element(
    dcc.Graph(
        id="dsr_commands_fig",
        figure=dsr_commands_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=1,
    col=2,
)
layout = grid.layout


@callback(
    [
        Output("map_fig", "figure"),
        Output("sld_fig", "figure"),
        Output("agent_activity_breakdown_fig", "figure"),
        Output("ev_charging_breakdown_fig", "figure"),
        Output("dsr_commands_fig", "figure"),
    ],
    [Input("figure_interval", "data")],
)
def update_figures(
    n_intervals: int,
) -> tuple[go.Figure, go.Figure, go.Figure, go.Figure, px.line]:
    """Function to update the plots in this page.

    Args:
        n_intervals (int): The number of times this page has updated.
            indexes by 1 every interval.

    Returns:
        tuple[go.Figure, go.Figure, go.Figure, go.Figure, px.line]:
            The new figures.
    """
    from ..data import DF_OPAL

    # TODO: ensure each figure is using the correct dataframe
    map_fig = generate_map_fig(DF_OPAL)
    sld_fig = generate_sld_fig(DF_OPAL)
    agent_activity_breakdown_fig = generate_agent_activity_breakdown_fig(DF_OPAL)
    ev_charging_breakdown_fig = generate_ev_charging_breakdown_fig(DF_OPAL)
    dsr_commands_fig = generate_dsr_commands_fig(DF_OPAL)
    log.debug("Updating figures on Agent page")
    return (
        map_fig,
        sld_fig,
        agent_activity_breakdown_fig,
        ev_charging_breakdown_fig,
        dsr_commands_fig,
    )
