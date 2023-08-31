"""Page in dash app."""

import dash  # type: ignore
import numpy as np
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore
import pandas as pd
import plotly.express as px

# from app.opal import opal_data

dash.register_page(__name__)

opal_data = {
    "data": {
        "index": [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0
        ],
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
            "Ev Status (Idle)"
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
                0.0
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
                34.0
            ],
            [
                "2035-01-22T00:00:16.110000",
                34.7576,
                34.7548,
                16.2635,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                16279.2764,
                16281.797,
                -0.5729,
                -1.0155,
                16.2868,
                8.9761,
                0.2806,
                -2.1394,
                0.0,
                0.7946,
                0.052,
                0.052,
                34.687,
                34.6842,
                0.0,
                0.0,
                30.7926,
                30.7926,
                23.0,
                5.0,
                80.0,
                173.0,
                0.0,
                311.0,
                7170.0,
                3.7148,
                3.7148,
                502.0,
                2.0,
                42.0
            ],
            [
                "2035-01-22T00:00:23.660000",
                34.6068,
                34.6036,
                16.3504,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                16367.0406,
                16368.53,
                -0.5745,
                -1.1827,
                16.3735,
                8.8902,
                0.2807,
                -2.146,
                0.0,
                0.7961,
                0.0519,
                0.0519,
                34.5363,
                34.5335,
                0.0,
                0.0,
                30.7094,
                30.7094,
                20.0,
                5.0,
                72.0,
                107.0,
                0.0,
                291.0,
                7164.0,
                3.663,
                3.663,
                495.0,
                2.0,
                49.0
            ],
            [
                "2035-01-22T00:00:31.100000",
                34.4579,
                34.4543,
                16.4357,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                16451.253,
                16452.6278,
                -0.576,
                -1.3463,
                16.4578,
                8.8063,
                0.2807,
                -2.1524,
                0.0,
                0.7975,
                0.0517,
                0.0517,
                34.3888,
                34.3862,
                0.0,
                0.0,
                30.7065,
                30.7065,
                30.0,
                5.0,
                59.0,
                124.0,
                0.0,
                316.0,
                7161.0,
                3.6408,
                3.6408,
                492.0,
                3.0,
                51.0
            ],
            [
                "2035-01-22T00:00:38.560000",
                34.3088,
                34.3056,
                16.5206,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                16536.7257,
                16538.3297,
                -0.5776,
                -1.5122,
                16.543,
                8.7217,
                0.2807,
                -2.1589,
                0.0,
                0.799,
                0.0515,
                0.0515,
                34.2416,
                34.239,
                0.0,
                0.0,
                30.6399,
                30.6399,
                30.0,
                5.0,
                59.0,
                124.0,
                0.0,
                316.0,
                7161.0,
                3.5742,
                3.5742,
                483.0,
                3.0,
                60.0
            ]
        ]
    }
}

##################
resolution = 30
interval = 100
colour = "#0D76BF"
##################

df = pd.DataFrame(**opal_data["data"])

gen_split_df = df.iloc[-1, 13:23]

print(gen_split_df)

t = np.linspace(0, np.pi * 2, resolution)
x, y = np.cos(t), np.sin(t)
# Example app.
gen_split_fig = px.pie(names=[
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
values=gen_split_df)

total_gen_fig = px.line(df, x="Time", y=[
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

total_dem_fig = px.line(df, x="Time", y=[
    "Total Demand",
]).update_layout(yaxis_title="GW")

system_freq_fig = px.line(df, x="Time", y=[
    "Total Generation",
    "Total Demand",
]).update_layout(yaxis_title="GW")

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
                    ]
                ),
                html.Div(
                    style={"width": "45%"},
                    children=[
                        html.H1("Generation Total"),
                        dcc.Graph(id="graph-gen-total", figure=total_gen_fig),
                    ]
                ),
            ]
        ),
        html.Div(
            style={"display": "flex", "justify-content": "space-around"},
            children=[
                html.Div(
                    style={"width": "45%"},
                    children=[
                        html.H1("Demand Total"),
                        dcc.Graph(id="graph-demand", figure=total_dem_fig),
                    ]
                ),
                html.Div(
                    style={"width": "45%"},
                    children=[
                        html.H1("System Frequency"),
                        dcc.Graph(id="graph-freq", figure=system_freq_fig),
                    ]
                ),
            ]
        ),
    ]
)

# dcc.Interval(id="interval", interval=interval)


@callback(Output("graph2", "extendData"), [Input("interval", "n_intervals")])
def update_data(n_intervals):  # type: ignore # noqa
    if n_intervals is None:
        raise PreventUpdate
    index = n_intervals % resolution
    # tuple is (dict of new data, target trace index, number of points to keep)
    return dict(x=[[x[index]]], y=[[y[index]]]), [0], 10
