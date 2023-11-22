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
from dash import Input, Output, callback, dcc, html  # type: ignore

from ..figures import (
    generate_gen_split_fig,
    generate_system_freq_fig,
    generate_total_dem_fig,
    generate_total_gen_fig,
)

dash.register_page(__name__)

df = pd.DataFrame({"Col": [0]})

gen_split_fig = generate_gen_split_fig(df)
total_gen_fig = generate_total_gen_fig(df)
total_dem_fig = generate_total_dem_fig(df)
system_freq_fig = generate_system_freq_fig(df)

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
                        html.H1("Generation Split", style={"textAlign": "center"}),
                        dcc.Graph(
                            id="graph-gen-split",
                            figure=gen_split_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Generation Total", style={"textAlign": "center"}),
                        dcc.Graph(
                            id="graph-gen-total",
                            figure=total_gen_fig,
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
                        html.H1("Demand Total", style={"textAlign": "center"}),
                        dcc.Graph(
                            id="graph-demand",
                            figure=total_dem_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("System Frequency", style={"textAlign": "center"}),
                        dcc.Graph(
                            id="graph-freq",
                            figure=system_freq_fig,
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
        Output("graph-gen-split", "figure"),
        Output("graph-gen-total", "figure"),
        Output("graph-demand", "figure"),
        Output("graph-freq", "figure"),
    ],
    [Input("data_opal", "data")],
)
def update_figures(
    data_opal: list[dict[str, object]],
) -> tuple[px.pie, px.line, px.line, px.line]:
    """Function to update the plots in this page.

    Args:
        data_opal (list): Opal data

    Returns:
        tuple[px.pie, px.line, px.line, px.line]: The new figures.
    """
    df_opal = pd.DataFrame(data_opal)

    gen_split_fig = generate_gen_split_fig(df_opal)
    total_gen_fig = generate_total_gen_fig(df_opal)
    total_dem_fig = generate_total_dem_fig(df_opal)
    system_freq_fig = generate_system_freq_fig(df_opal)
    return gen_split_fig, total_gen_fig, total_dem_fig, system_freq_fig
