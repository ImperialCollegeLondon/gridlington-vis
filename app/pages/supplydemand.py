"""Page in dash app."""


import dash  # type: ignore
import pandas as pd
import plotly.express as px  # type: ignore
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore

from .. import datahub_api as datahub

dash.register_page(__name__)

##################
interval = 7000
##################


def generate_gen_split_fig(df: pd.DataFrame) -> px.pie:
    """Creates Plotly figure for Generation Split graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly express figure
    """
    if len(df.columns) == 1:
        gen_split_fig = px.pie()
    else:
        gen_split_df = df.iloc[-1, 13:23]

        gen_split_fig = px.pie(
            names=[
                "Battery Generation",
                "Interconnector Power",
                "Offshore Wind Generation",
                "Onshore Wind Generation",
                "Other Generation",
                "Pump Generation",
                "Pv Generation",
                "Nuclear Generation",
                "Hydro Generation",
                "Gas Generation",
            ],
            values=gen_split_df,
        ).update_layout(title_text=df.iloc[-1]["Time"])
    return gen_split_fig


def generate_total_gen_fig(df: pd.DataFrame) -> px.line:
    """Creates Plotly figure for Total Generation graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly express figure
    """
    if len(df.columns) == 1:
        total_gen_fig = px.line()
    else:
        total_gen_fig = px.line(
            df,
            x="Time",
            y=[
                "Total Generation",
                "Battery Generation",
                "Interconnector Power",
                "Offshore Wind Generation",
                "Onshore Wind Generation",
                "Other Generation",
                "Pump Generation",
                "Pv Generation",
                "Nuclear Generation",
                "Hydro Generation",
                "Gas Generation",
            ],
        ).update_layout(yaxis_title="GW")
    return total_gen_fig


def generate_total_dem_fig(df: pd.DataFrame) -> px.line:
    """Creates Plotly figure for Total Demand graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly express figure
    """
    if len(df.columns) == 1:
        total_dem_fig = px.line()
    else:
        total_dem_fig = px.line(
            df,
            x="Time",
            y=[
                "Total Demand",
            ],
        ).update_layout(yaxis_title="GW")
    return total_dem_fig


def generate_system_freq_fig(df: pd.DataFrame) -> px.line:
    """Creates Plotly figure for System Frequency graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly express figure
    """
    if len(df.columns) == 1:
        system_freq_fig = px.line()
    else:
        system_freq_fig = px.line(
            df,
            x="Time",
            y=[
                "Total Generation",
                "Total Demand",
            ],
        ).update_layout(yaxis_title="GW")
    return system_freq_fig


df = pd.DataFrame({"Col": [0]})

gen_split_fig = generate_gen_split_fig(df)
total_gen_fig = generate_total_gen_fig(df)
total_dem_fig = generate_total_dem_fig(df)
system_freq_fig = generate_system_freq_fig(df)

layout = html.Div(
    children=[
        html.Div(
            style={"display": "flex", "justify-content": "space-around"},
            children=[
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Generation Split"),
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
                        html.H1("Generation Total"),
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
                        html.H1("Demand Total"),
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
                        html.H1("System Frequency"),
                        dcc.Graph(
                            id="graph-freq",
                            figure=system_freq_fig,
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
        Output("graph-gen-split", "figure"),
        Output("graph-gen-total", "figure"),
        Output("graph-demand", "figure"),
        Output("graph-freq", "figure"),
    ],
    [Input("interval", "n_intervals")],
)
def update_data(n_intervals):  # type: ignore # noqa
    if n_intervals is None:
        raise PreventUpdate

    data = datahub.get_opal_data()

    new_df = pd.DataFrame(**data)

    gen_split_fig = generate_gen_split_fig(new_df)
    total_gen_fig = generate_total_gen_fig(new_df)
    total_dem_fig = generate_total_dem_fig(new_df)
    system_freq_fig = generate_system_freq_fig(new_df)
    return gen_split_fig, total_gen_fig, total_dem_fig, system_freq_fig
