"""Page in dash app."""


import base64
import os

import dash  # type: ignore
import pandas as pd
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore

from .. import datahub_api as datahub
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


class SVG:
    """Class for loading SVGs and formating for display."""

    def __init__(self, file_path: str) -> None:
        """Loads SVG file and formats for display using html.Img.

        Example usage:
        svg = SVG(path)
        html.Img(src=svg.url)

        Args:
            file_path (str): Path to svg file
        """
        raw = open(file_path, "rt", encoding="utf-8").read()
        encoded = base64.b64encode(bytes(raw, "utf-8"))
        self.url = f"data:image/svg+xml;base64,{encoded.decode()}"

        # Image dimensions
        self.width, self.height = [
            int(raw.split(x, 1)[1].split(" ", 1)[0][2:-3]) for x in ["width", "height"]
        ]
        self.aspect_ratio = self.width / self.height


svg_map = SVG(os.path.dirname(os.path.abspath(__file__)) + "/../map.svg")
svg_sld = SVG(os.path.dirname(os.path.abspath(__file__)) + "/../sld.svg")

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
                    style={"width": "32%"},
                    children=[
                        html.H1("Agent Locations", style={"textAlign": "center"}),
                        html.Div(
                            style={"position": "relative"},
                            children=[
                                html.Img(src=svg_map.url, width="90%"),
                                dcc.Graph(
                                    id="agent_location_fig",
                                    figure=agent_location_fig,
                                    style={
                                        "position": "absolute",
                                        "top": 0,
                                        "left": 0,
                                        "width": "90%",
                                        "aspect-ratio": str(svg_map.aspect_ratio),
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "32%"},
                    children=[
                        html.H1(
                            "Agent Locations on SLD", style={"textAlign": "center"}
                        ),
                        html.Div(
                            style={"position": "relative"},
                            children=[
                                html.Img(src=svg_sld.url, width="90%"),
                                dcc.Graph(
                                    id="agent_location_sld_fig",
                                    figure=agent_location_sld_fig,
                                    style={
                                        "position": "absolute",
                                        "top": 0,
                                        "left": 0,
                                        "width": "90%",
                                        "aspect-ratio": str(svg_sld.aspect_ratio),
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "32%"},
                    children=[
                        html.H1(
                            "Agent Activity Breakdown", style={"textAlign": "center"}
                        ),
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
                    style={"width": "32%"},
                    children=[
                        html.H1(
                            "Electric Vehicle Location", style={"textAlign": "center"}
                        ),
                        html.Div(
                            style={"position": "relative"},
                            children=[
                                html.Img(src=svg_map.url, width="90%"),
                                dcc.Graph(
                                    id="ev_location_fig",
                                    figure=ev_location_fig,
                                    style={
                                        "position": "absolute",
                                        "top": 0,
                                        "left": 0,
                                        "width": "90%",
                                        "aspect-ratio": str(svg_map.aspect_ratio),
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "32%"},
                    children=[
                        html.H1(
                            "Electric Vehicle Location on SLD",
                            style={"textAlign": "center"},
                        ),
                        html.Div(
                            style={"position": "relative"},
                            children=[
                                html.Img(src=svg_sld.url, width="90%"),
                                dcc.Graph(
                                    id="ev_location_sld_fig",
                                    figure=ev_location_sld_fig,
                                    style={
                                        "position": "absolute",
                                        "top": 0,
                                        "left": 0,
                                        "width": "90%",
                                        "aspect-ratio": str(svg_sld.aspect_ratio),
                                    },
                                ),
                            ],
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
                    style={"width": "48%"},  # TODO: how wide?
                    children=[
                        html.H1(
                            "DSR Commands to Agents", style={"textAlign": "center"}
                        ),
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

    data_opal = datahub.get_opal_data()
    new_df_opal = pd.DataFrame(**data_opal)

    # TODO: uncomment when datahub.get_dsr_data() is fixed
    # data_dsr = datahub.get_dsr_data()
    # new_df_dsr = pd.DataFrame(**data_dsr)

    # TODO: ensure each figure is using the correct dataframe
    agent_location_fig = generate_agent_location_fig(new_df_opal)
    agent_location_sld_fig = generate_agent_location_sld_fig(new_df_opal)
    agent_activity_breakdown_fig = generate_agent_activity_breakdown_fig(new_df_opal)
    ev_location_fig = generate_ev_location_fig(new_df_opal)
    ev_location_sld_fig = generate_ev_location_sld_fig(new_df_opal)
    ev_charging_breakdown_fig = generate_ev_charging_breakdown_fig(new_df_opal)
    dsr_commands_fig = generate_dsr_commands_fig(new_df_opal)
    return (
        agent_location_fig,
        agent_location_sld_fig,
        agent_activity_breakdown_fig,
        ev_location_fig,
        ev_location_sld_fig,
        ev_charging_breakdown_fig,
        dsr_commands_fig,
    )
