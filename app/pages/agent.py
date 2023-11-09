"""Page in dash app."""


import dash  # type: ignore
import pandas as pd
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore
import base64
import os

from ..figures import (
    generate_agent_activity_breakdown_fig,
    generate_agent_location_fig,
    generate_agent_location_sld_fig,
    generate_dsr_commands_fig,
    generate_ev_charging_breakdown_fig,
    generate_ev_location_fig,
    generate_ev_location_sld_fig,
)

dash.register_page(__name__)

##################
interval = 7000
##################

df = pd.DataFrame({"Col": [0]})

agent_location_fig = generate_agent_location_fig(df)
agent_location_sld_fig = generate_agent_location_sld_fig(df)
agent_activity_breakdown_fig = generate_agent_activity_breakdown_fig(df)
ev_location_fig = generate_ev_location_fig(df)
ev_location_sld_fig = generate_ev_location_sld_fig(df)
ev_charging_breakdown_fig = generate_ev_charging_breakdown_fig(df)
dsr_commands_fig = generate_dsr_commands_fig(df)

# Load SVGs
p = os.path.dirname(os.path.abspath(__file__))
map_encoded = base64.b64encode(open(p + '/../map.svg', 'rb').read()) 
map_svg = 'data:image/svg+xml;base64,{}'.format(map_encoded.decode()) 
sld_encoded = base64.b64encode(open(p + '/../sld.svg', 'rb').read()) 
sld_svg = 'data:image/svg+xml;base64,{}'.format(sld_encoded.decode()) 


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
                        html.H1("Agent Locations"),
                        html.Img(src=map_svg, width=400, height=400),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Agent Locations on SLD"),
                        html.Img(src=sld_svg, width=400, height=400),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Agent Activity Breakdown"),
                        dcc.Graph(
                            id="agent_activity_breakdown_fig",
                            figure=agent_activity_breakdown_fig,
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
                        html.H1("Electric Vehicle Location"),
                        html.Img(src=map_svg, width=400, height=400),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Electric Vehicle Location on SLD"),
                        html.Img(src=sld_svg, width=400, height=400),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Electric Vehicle Charging Breakdown"),
                        dcc.Graph(
                            id="ev_charging_breakdown_fig",
                            figure=ev_charging_breakdown_fig,
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
                        html.H1("DSR Commands to Agents"),
                        dcc.Graph(
                            id="dsr_commands_fig",
                            figure=dsr_commands_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                )
            ],
        ),
        dcc.Interval(id="interval", interval=interval),
    ],
)


@callback(
    [
        Output("agent_location_fig", "figure"),
        Output("agent_location_sld_fig", "figure"),
        Output("agent_activity_breakdown_fig", "figure"),
        Output("ev_location_fig", "figure"),
        Output("ev_location_sld_fig", "figure"),
        Output("ev_charging_breakdown_fig", "figure"),
        Output("dsr_commands_fig", "figure"),
    ],
    [Input("interval", "n_intervals")],
)
def update_data(n_intervals):  # type: ignore # noqa
    if n_intervals is None:
        raise PreventUpdate

    # data_opal = datahub.get_opal_data()
    # new_df_opal = pd.DataFrame(**data_opal)

    # data_dsr = datahub.get_dsr_data()
    # new_df_dsr = pd.DataFrame(**data_dsr)

    agent_location_fig = generate_agent_location_fig(df)
    agent_location_sld_fig = generate_agent_location_sld_fig(df)
    agent_activity_breakdown_fig = generate_agent_activity_breakdown_fig(df)
    ev_location_fig = generate_ev_location_fig(df)
    ev_location_sld_fig = generate_ev_location_sld_fig(df)
    ev_charging_breakdown_fig = generate_ev_charging_breakdown_fig(df)
    dsr_commands_fig = generate_dsr_commands_fig(df)
    return (
        agent_location_fig,
        agent_location_sld_fig,
        agent_activity_breakdown_fig,
        ev_location_fig,
        ev_location_sld_fig,
        ev_charging_breakdown_fig,
        dsr_commands_fig,
    )
