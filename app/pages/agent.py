"""Page in dash app."""


import dash  # type: ignore
import pandas as pd
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore

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
                        dcc.Graph(
                            id="agent_location_fig",
                            figure=agent_location_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Agent Locations on SLD"),
                        dcc.Graph(
                            id="agent_location_sld_fig",
                            figure=agent_location_sld_fig,
                            style={"height": "40vh"},
                        ),
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
                        dcc.Graph(
                            id="ev_location_fig",
                            figure=ev_location_fig,
                            style={"height": "40vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1("Electric Vehicle Location on SLD"),
                        dcc.Graph(
                            id="ev_location_sld_fig",
                            figure=ev_location_sld_fig,
                            style={"height": "40vh"},
                        ),
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
