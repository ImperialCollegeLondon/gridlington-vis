"""Page in dash app."""

import random

import pandas as pd
import plotly.express as px
import requests

import dash  # type: ignore
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore

# from app.opal import opal_data


dash.register_page(__name__)

opal_data = {
    "data": {
        "index": [0.0, 1.0],
        "columns": [
            "Time",
            "Total Generation",
            "Total Demand",
            "Total Offshore Generation",
            "Intra-Day Market Value",
            "Intra-Day Market Generation",
            "Intra-Day Market Demand",
            "Intra-Day Market Storage",
            "Balancing Mechanism Generation",
            "Balancing Mechanism Storage",
            "Balancing Mechanism Demand",
            "Exp. Offshore Wind Generation",
            "Real Offshore Wind Generation",
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
            "Expected Demand",
            "Real Demand",
            "Balancing Mechanism Value",
            "Balancing Mechanism Accepted Power",
            "Expected Gridlington Demand",
            "Real Gridlington Demand",
            "Household Activity (Work)",
            "Household Activity (Study)",
            "Household Activity (Home Care)",
            "Household Activity (Personal Care)",
            "Household Activity (Shopping)",
            "Household Activity (Leisure)",
            "Household Activity (Sleep)",
            "Expected Ev Charging Power",
            "Real Ev Charging Power",
            "Ev Status (Charging)",
            "Ev Status (Travelling)",
            "Ev Status (Idle)",
        ],
        "data": [
            [
                "2035-01-22T00:00:00",
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
            ],
            [
                "2035-01-22T00:00:08.580000",
                34.9085,
                34.9055,
                16.177,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                16192.8871,
                16194.8348,
                -0.5713,
                -0.8467,
                16.2002,
                9.0618,
                0.2806,
                -2.1328,
                0.0,
                0.7931,
                0.0522,
                0.0522,
                34.8373,
                34.8343,
                0.0,
                0.0,
                30.801,
                30.801,
                28.0,
                5.0,
                63.0,
                72.0,
                0.0,
                303.0,
                7230.0,
                3.774,
                3.774,
                510.0,
                2.0,
                34.0,
            ],
        ],
    }
}

opal_post = {
    "array": [
        1,
        8.58,
        34.9085,
        34.9055,
        16.177,
        7.8868,
        15.1744,
        3.3549,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        16192.8871,
        16194.8348,
        -0.5713,
        -0.8467,
        16.2002,
        9.0618,
        0.2806,
        -2.1328,
        0,
        0.7931,
        0.0522,
        0.0522,
        34.8373,
        34.8343,
        0,
        0,
        30.801,
        30.801,
        28,
        5,
        63,
        72,
        0,
        303,
        7230,
        3.774,
        3.774,
        510,
        2,
        34,
    ]
}

##################
resolution = 30
interval = 7000
colour = "#0D76BF"
##################


def generate_gen_split_fig(df: pd.DataFrame) -> px.pie:
    """Creates Plotly figure for Generation Split graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly express figure
    """
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
    system_freq_fig = px.line(
        df,
        x="Time",
        y=[
            "Total Generation",
            "Total Demand",
        ],
    ).update_layout(yaxis_title="GW")
    return system_freq_fig


df = pd.DataFrame(**opal_data["data"])

gen_split_fig = generate_gen_split_fig(df)
total_gen_fig = generate_total_gen_fig(df)
total_dem_fig = generate_total_dem_fig(df)
system_freq_fig = generate_system_freq_fig(df)

layout = html.Div(
    [
        html.Div(
            style={"display": "flex", "justify-content": "space-around"},
            children=[
                html.Div(
                    style={"width": "45%"},
                    children=[
                        html.H1("Generation Split"),
                        dcc.Graph(id="graph-gen-split", figure=gen_split_fig),
                    ],
                ),
                html.Div(
                    style={"width": "45%"},
                    children=[
                        html.H1("Generation Total"),
                        dcc.Graph(id="graph-gen-total", figure=total_gen_fig),
                    ],
                ),
            ],
        ),
        html.Div(
            style={"display": "flex", "justify-content": "space-around"},
            children=[
                html.Div(
                    style={"width": "45%"},
                    children=[
                        html.H1("Demand Total"),
                        dcc.Graph(id="graph-demand", figure=total_dem_fig),
                    ],
                ),
                html.Div(
                    style={"width": "45%"},
                    children=[
                        html.H1("System Frequency"),
                        dcc.Graph(id="graph-freq", figure=system_freq_fig),
                    ],
                ),
            ],
        ),
        dcc.Interval(id="interval", interval=interval),
    ]
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

    for idx, x in enumerate(opal_post["array"]):
        if idx == 0:
            opal_post["array"][idx] = x + 1
        elif idx == 1:
            opal_post["array"][idx] = x + 7
        else:
            opal_post["array"][idx] = x + random.randint(2, 20)

    req = requests.post("http://127.0.0.1:8000/opal", json=opal_post)
    req = requests.get("http://127.0.0.1:8000/opal")

    new_df = pd.DataFrame(**req.json()["data"])

    gen_split_fig = generate_gen_split_fig(new_df)
    total_gen_fig = generate_total_gen_fig(new_df)
    total_dem_fig = generate_total_dem_fig(new_df)
    system_freq_fig = generate_system_freq_fig(new_df)
    return gen_split_fig, total_gen_fig, total_dem_fig, system_freq_fig
