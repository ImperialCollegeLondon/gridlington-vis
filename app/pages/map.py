"""Map view page in dash app.
This is a cut down copy of the agent page
One plots:
- Agent and EV Locations
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

map_fig = generate_map_fig(df)

grid = GridBuilder(rows=1, cols=1)
grid.add_element(
    dcc.Graph(
        id="big_map_fig",
        figure=map_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=0,
    col=0,
)
layout = grid.layout


@callback(
    [
        Output("big_map_fig", "figure"),
    ],
    [Input("figure_interval", "data")],
)
def update_figures(
    n_intervals: int,
) -> tuple[go.Figure]:
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
    log.debug("Updating figures on Map page")
    return (
        map_fig,
    )
