"""TODO."""

import dash  # type: ignore
import pandas as pd
import plotly.express as px  # type: ignore
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore

from .. import LIVE_MODEL, log
from ..datahub_api import get_opal_data  # , get_dsr_data
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

##################
interval = 7000
##################

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
                    style={"width": "32%"},
                    children=[
                        html.H1("Agent Locations", style={"textAlign": "center"}),
                        html.Div(
                            style={"position": "relative"},
                            children=[
                                html.Img(src=svg_map.url, width="90%"),
                                html.Img(
                                    id="agent_location_map_img",
                                    src=agent_location_map_img,
                                    width="90%",
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
                    style={"width": "32%"},
                    children=[
                        html.H1(
                            "Agent Locations on SLD", style={"textAlign": "center"}
                        ),
                        html.Div(
                            style={"position": "relative"},
                            children=[
                                html.Img(src=svg_sld.url, width="90%"),
                                html.Img(
                                    id="agent_location_sld_img",
                                    src=agent_location_sld_img,
                                    width="90%",
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
                                html.Img(
                                    id="ev_location_map_img",
                                    src=ev_location_map_img,
                                    width="90%",
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
                                html.Img(
                                    id="ev_location_sld_img",
                                    src=ev_location_sld_img,
                                    width="90%",
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
        Output("agent_location_map_img", "src"),
        Output("agent_location_sld_img", "src"),
        Output("agent_activity_breakdown_fig", "figure"),
        Output("ev_location_map_img", "src"),
        Output("ev_location_sld_img", "src"),
        Output("ev_charging_breakdown_fig", "figure"),
        Output("dsr_commands_fig", "figure"),
    ],
    [Input("interval", "n_intervals")],
)
def update_data(n_intervals: int) -> tuple[str, str, px.pie, str, str, px.pie, px.line]:
    """Function to update the plots in this page.

    Args:
        n_intervals (int): The number of times this page has updated.
            indexes by 1 every 7 seconds.

    Returns:
        tuple[str, str, px.pie, str, str, px.pie, px.line]:
            The new figures.
    """
    if n_intervals is None:
        raise PreventUpdate

    if LIVE_MODEL:
        log.debug("Updating plots from live model")
        data_opal = get_opal_data()
        new_df_opal = pd.DataFrame(**data_opal)  # type: ignore[call-overload]
        # data_dsr = get_dsr_data() TODO
        # new_df_dsr = pd.DataFrame(**data_dsr)
    else:
        from ..pre_set_data import OPAL_DATA

        log.debug("Updating plots with pre-set data")
        new_df_opal = OPAL_DATA.loc[:n_intervals]
        # new_df_dsr = ... TODO

    # TODO: ensure each figure is using the correct dataframe
    agent_location_fig = generate_agent_location_map_img(new_df_opal)
    agent_location_sld_img = generate_agent_location_sld_img(new_df_opal)
    agent_activity_breakdown_fig = generate_agent_activity_breakdown_fig(new_df_opal)
    ev_location_fig = generate_ev_location_map_img(new_df_opal)
    ev_location_sld_img = generate_ev_location_sld_img(new_df_opal)
    ev_charging_breakdown_fig = generate_ev_charging_breakdown_fig(new_df_opal)
    dsr_commands_fig = generate_dsr_commands_fig(new_df_opal)
    return (
        agent_location_fig,
        agent_location_sld_img,
        agent_activity_breakdown_fig,
        ev_location_fig,
        ev_location_sld_img,
        ev_charging_breakdown_fig,
        dsr_commands_fig,
    )
