"""SupplyDemand page in dash app.

Four plots (2x2):
- Generation Split
- Generation Total
- Demand Total
- System Frequency
"""


import dash  # type: ignore
import pandas as pd
import plotly.express as px  # type: ignore
from dash import Input, Output, callback, dcc  # type: ignore

from ..figures import (
    generate_gen_split_fig,
    generate_system_freq_fig,
    generate_total_dem_fig,
    generate_total_gen_fig,
)
from ..layout import GridBuilder

dash.register_page(__name__)

df = pd.DataFrame({"Col": [0]})

gen_split_fig = generate_gen_split_fig(df)
total_gen_fig = generate_total_gen_fig(df)
total_dem_fig = generate_total_dem_fig(df)
system_freq_fig = generate_system_freq_fig(df)

grid = GridBuilder(rows=2, cols=2)
grid.add_element(
    dcc.Graph(
        id="graph-gen-split",
        figure=gen_split_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=0,
    col=0,
)
grid.add_element(
    dcc.Graph(
        id="graph-gen-total",
        figure=total_gen_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=0,
    col=1,
)
grid.add_element(
    dcc.Graph(
        id="graph-demand",
        figure=total_dem_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=1,
    col=0,
)
grid.add_element(
    dcc.Graph(
        id="graph-freq",
        figure=system_freq_fig,
        style={"height": "100%", "width": "100%"},
    ),
    row=1,
    col=1,
)
layout = grid.layout


@callback(
    [
        Output("graph-gen-split", "figure"),
        Output("graph-gen-total", "figure"),
        Output("graph-demand", "figure"),
        Output("graph-freq", "figure"),
    ],
    [Input("figure_interval", "n_intervals")],
)
def update_figures(
    n_intervals: int,
) -> tuple[px.pie, px.line, px.line, px.line]:
    """Function to update the plots in this page.

    Args:
        n_intervals (int): The number of times this page has updated.
            indexes by 1 every 7 seconds.

    Returns:
        tuple[px.pie, px.line, px.line, px.line]: The new figures.
    """
    from ..data import DF_OPAL

    gen_split_fig = generate_gen_split_fig(DF_OPAL)
    total_gen_fig = generate_total_gen_fig(DF_OPAL)
    total_dem_fig = generate_total_dem_fig(DF_OPAL)
    system_freq_fig = generate_system_freq_fig(DF_OPAL)
    return gen_split_fig, total_gen_fig, total_dem_fig, system_freq_fig
