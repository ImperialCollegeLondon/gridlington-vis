"""Agent view page in dash app.

Seven plots:
- Agent Locations
- Agent Locations on SLD
- Agent Activity Breakdown
- Electric Vehicle Location
- Electric Vehicle Location on SLD
- Electric Vehicle Charging Breakdown
- DSR commands to agents.
"""

import dash  # type: ignore
import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
from dash import Input, Output, callback, dcc, html  # type: ignore

from ..figures import (
    generate_agent_activity_breakdown_fig,
    generate_dsr_commands_fig,
    generate_ev_charging_breakdown_fig,
)
from ..svg import (
    generate_agent_location_map_img,
    generate_agent_location_sld_img,
    generate_ev_location_map_img,
    generate_ev_location_sld_img,
    svg_map,
    svg_sld,
)

dash.register_page(__name__)

df = pd.DataFrame({"Col": [0]})

agent_location_map_img = generate_agent_location_map_img(df)
agent_location_sld_img = generate_agent_location_sld_img(df)
agent_activity_breakdown_fig = generate_agent_activity_breakdown_fig(df)
ev_location_map_img = generate_ev_location_map_img(df)
ev_location_sld_img = generate_ev_location_sld_img(df)
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
                        html.H1("Agent Locations", style={"textAlign": "center"}),
                        html.Div(
                            style={
                                "position": "relative",
                                "margin": "auto",
                                "width": "60%",
                            },
                            children=[
                                html.Img(src=svg_map.url, width="100%"),
                                html.Img(
                                    id="agent_location_map_img",
                                    src=agent_location_map_img,
                                    width="100%",
                                    style={
                                        "position": "absolute",
                                        "top": 0,
                                        "left": 0,
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1(
                            "Electric Vehicle Location", style={"textAlign": "center"}
                        ),
                        html.Div(
                            style={
                                "position": "relative",
                                "margin": "auto",
                                "width": "60%",
                            },
                            children=[
                                html.Img(src=svg_map.url, width="100%"),
                                html.Img(
                                    id="ev_location_map_img",
                                    src=ev_location_map_img,
                                    width="100%",
                                    style={
                                        "position": "absolute",
                                        "top": 0,
                                        "left": 0,
                                    },
                                ),
                            ],
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
                        html.H1(
                            "Agent Locations on SLD", style={"textAlign": "center"}
                        ),
                        html.Div(
                            style={
                                "position": "relative",
                                "margin": "auto",
                                "width": "60%",
                            },
                            children=[
                                html.Img(src=svg_sld.url, width="100%"),
                                html.Img(
                                    id="agent_location_sld_img",
                                    src=agent_location_sld_img,
                                    width="100%",
                                    style={
                                        "position": "absolute",
                                        "top": 0,
                                        "left": 0,
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%"},
                    children=[
                        html.H1(
                            "Electric Vehicle Location on SLD",
                            style={"textAlign": "center"},
                        ),
                        html.Div(
                            style={
                                "position": "relative",
                                "margin": "auto",
                                "width": "60%",
                            },
                            children=[
                                html.Img(src=svg_sld.url, width="100%"),
                                html.Img(
                                    id="ev_location_sld_img",
                                    src=ev_location_sld_img,
                                    width="100%",
                                    style={
                                        "position": "absolute",
                                        "top": 0,
                                        "left": 0,
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            style={"display": "flex", "justify-content": "space-around"},
            children=[
                html.Div(
                    style={"width": "32%"},
                    children=[
                        html.H1(
                            "Agent Activity Breakdown", style={"textAlign": "center"}
                        ),
                        dcc.Graph(
                            id="agent_activity_breakdown_fig",
                            figure=agent_activity_breakdown_fig,
                            style={"height": "30vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "32%"},
                    children=[
                        html.H1(
                            "Electric Vehicle Charging Breakdown",
                            style={"textAlign": "center"},
                        ),
                        dcc.Graph(
                            id="ev_charging_breakdown_fig",
                            figure=ev_charging_breakdown_fig,
                            style={"height": "30vh"},
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "32%"},
                    children=[
                        html.H1(
                            "DSR Commands to Agents", style={"textAlign": "center"}
                        ),
                        dcc.Graph(
                            id="dsr_commands_fig",
                            figure=dsr_commands_fig,
                            style={"height": "30vh"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@callback(
    [
        Output("agent_location_map_img", "src"),
        Output("agent_location_sld_img", "src"),
        Output("agent_activity_breakdown_fig", "figure"),
        Output("ev_location_map_img", "src"),
        Output("ev_location_sld_img", "src"),
        Output("ev_charging_breakdown_fig", "figure"),
        Output("dsr_commands_fig", "figure"),
    ],
    [Input("figure_interval", "n_intervals")],
)
def update_figures(
    n_intervals: int,
) -> tuple[str, str, go.Figure, str, str, go.Figure, px.line]:
    """Function to update the plots in this page.

    Args:
        n_intervals (int): The number of times this page has updated.
            indexes by 1 every 7 seconds.

    Returns:
        tuple[str, str, px.pie, str, str, px.pie, px.line]:
            The new figures.
    """
    from ..data import DF_OPAL

    # TODO: ensure each figure is using the correct dataframe
    agent_location_fig = generate_agent_location_map_img(DF_OPAL)
    agent_location_sld_img = generate_agent_location_sld_img(DF_OPAL)
    agent_activity_breakdown_fig = generate_agent_activity_breakdown_fig(DF_OPAL)
    ev_location_fig = generate_ev_location_map_img(DF_OPAL)
    ev_location_sld_img = generate_ev_location_sld_img(DF_OPAL)
    ev_charging_breakdown_fig = generate_ev_charging_breakdown_fig(DF_OPAL)
    dsr_commands_fig = generate_dsr_commands_fig(DF_OPAL)
    return (
        agent_location_fig,
        agent_location_sld_img,
        agent_activity_breakdown_fig,
        ev_location_fig,
        ev_location_sld_img,
        ev_charging_breakdown_fig,
        dsr_commands_fig,
    )
