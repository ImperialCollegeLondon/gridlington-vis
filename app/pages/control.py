"""Controller Page for Dash app."""

import dash  # type: ignore
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore
from dash_iconify import DashIconify  # type: ignore

dash.register_page(__name__)

options = [
    "NMX",
    "Balance of Supply and Demand",
    "Markets and Reserve",
    "NMX Georgraphic Map",
    "NMX 11kV Schematic",
    "NMX Issues",
    "Market",
    "Agent",
]

layout = html.Div(
    style={
        "height": "96vh",
        "display": "flex",
        "flex-direction": "column",
        "justify-content": "space-around",
    },
    children=[
        html.Div(
            style={"padding": "20px 0", "flex": "1"},
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "justify-content": "space-around",
                        "padding": "6px 0",
                    },
                    children=[
                        html.Div(
                            style={"width": "46%"},
                            children=[
                                html.H3(
                                    style={"text-align": "center", "margin": "0"},
                                    children="Hub01",
                                ),
                                dcc.Dropdown(
                                    options,
                                    "Market",
                                    id="Hub01_dropdown",
                                    clearable=False,
                                ),
                            ],
                        ),
                        html.Div(
                            style={"width": "46%"},
                            children=[
                                html.H3(
                                    style={"text-align": "center", "margin": "0"},
                                    children="Hub02",
                                ),
                                dcc.Dropdown(
                                    options,
                                    "Agent",
                                    id="Hub02_dropdown",
                                    clearable=False,
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justify-content": "space-around",
                        "padding": "6px 0",
                    },
                    children=[
                        html.Div(
                            style={"width": "46%"},
                            children=[
                                html.Div(
                                    children=[
                                        html.H3(
                                            style={
                                                "text-align": "center",
                                                "margin": "0",
                                            },
                                            children="PC01-Top",
                                        ),
                                        dcc.Dropdown(
                                            options,
                                            "NMX",
                                            id="PC01-Top_dropdown",
                                            clearable=False,
                                        ),
                                    ],
                                ),
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding": "12px 0",
                                    },
                                    children=[
                                        html.Div(
                                            style={"width": "46%"},
                                            children=[
                                                html.H3(
                                                    style={
                                                        "text-align": "center",
                                                        "margin": "0",
                                                    },
                                                    children="PC01-Left",
                                                ),
                                                dcc.Dropdown(
                                                    options,
                                                    "Balance of Supply and Demand",
                                                    id="PC01-Left_dropdown",
                                                    clearable=False,
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            style={"width": "46%"},
                                            children=[
                                                html.H3(
                                                    style={
                                                        "text-align": "center",
                                                        "margin": "0",
                                                    },
                                                    children="PC01-Right",
                                                ),
                                                dcc.Dropdown(
                                                    options,
                                                    "Markets and Reserve",
                                                    id="PC01-Right_dropdown",
                                                    clearable=False,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            style={"width": "46%"},
                            children=[
                                html.Div(
                                    children=[
                                        html.H3(
                                            style={
                                                "text-align": "center",
                                                "margin": "0",
                                            },
                                            children="PC02-Top",
                                        ),
                                        dcc.Dropdown(
                                            options,
                                            "NMX Georgraphic Map",
                                            id="PC02-Top_dropdown",
                                            clearable=False,
                                        ),
                                    ]
                                ),
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding": "12px 0",
                                    },
                                    children=[
                                        html.Div(
                                            style={"width": "46%"},
                                            children=[
                                                html.H3(
                                                    style={
                                                        "text-align": "center",
                                                        "margin": "0",
                                                    },
                                                    children="PC02-Left",
                                                ),
                                                dcc.Dropdown(
                                                    options,
                                                    "NMX 11kV Schematic",
                                                    id="PC02-Left_dropdown",
                                                    clearable=False,
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            style={"width": "46%"},
                                            children=[
                                                html.H3(
                                                    style={
                                                        "text-align": "center",
                                                        "margin": "0",
                                                    },
                                                    children="PC02-Right",
                                                ),
                                                dcc.Dropdown(
                                                    options,
                                                    "NMX Issues",
                                                    id="PC02-Right_dropdown",
                                                    clearable=False,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            style={"padding": "20px 0", "flex": "1"},
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "justify-content": "space-around",
                        "padding": "10px",
                        "width": "66%",
                        "margin": "auto",
                    },
                    children=[
                        html.Div(
                            id="button_save",
                            style={
                                "backgroundColor": "gray",
                                "border-radius": "50%",
                                "padding": "20px",
                                "display": "grid",
                                "justify-content": "center",
                            },
                            children=[
                                DashIconify(icon="solar:upload-outline", width=100)
                            ],
                        ),
                        html.Div(
                            id="button_undo",
                            style={
                                "backgroundColor": "gray",
                                "border-radius": "50%",
                                "padding": "20px",
                                "display": "grid",
                                "justify-content": "center",
                            },
                            children=[DashIconify(icon="iconoir:undo", width=100)],
                        ),
                    ],
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justify-content": "space-around",
                        "padding": "10px",
                    },
                    children=[
                        html.Div(
                            id="button_start",
                            style={
                                "backgroundColor": "gray",
                                "border-radius": "50%",
                                "padding": "20px",
                                "display": "grid",
                                "justify-content": "center",
                            },
                            children=[DashIconify(icon="ph:play-fill", width=100)],
                        ),
                        html.Div(
                            id="button_stop",
                            style={
                                "backgroundColor": "gray",
                                "border-radius": "50%",
                                "padding": "20px",
                                "display": "grid",
                                "justify-content": "center",
                            },
                            children=[DashIconify(icon="ri:stop-fill", width=100)],
                        ),
                        html.Div(
                            id="button_refresh",
                            style={
                                "backgroundColor": "gray",
                                "border-radius": "50%",
                                "padding": "20px",
                                "display": "grid",
                                "justify-content": "center",
                            },
                            children=[
                                DashIconify(icon="solar:refresh-bold", width=100)
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@callback(Output("button_save", "className"), [Input("button_save", "n_clicks")])
def save_button_click(n_clicks):  # type: ignore # noqa
    """Placeholder function for Save Button."""
    if n_clicks is None:
        raise PreventUpdate
    print("Clicked Save Button!")
    return "clicked"


@callback(Output("button_undo", "className"), [Input("button_undo", "n_clicks")])
def undo_button_click(n_clicks):  # type: ignore # noqa
    """Placeholder function for Undo Button."""
    if n_clicks is None:
        raise PreventUpdate
    print("Clicked Undo Button!")
    return "clicked"


@callback(Output("button_start", "className"), [Input("button_start", "n_clicks")])
def start_button_click(n_clicks):  # type: ignore # noqa
    """Placeholder function for Start Button.

    Will make an API call to start Gridlington simulation and Datahub.

    """
    if n_clicks is None:
        raise PreventUpdate
    print("Clicked Start Button!")
    return "clicked"


@callback(Output("button_stop", "className"), [Input("button_stop", "n_clicks")])
def stop_button_click(n_clicks):  # type: ignore # noqa
    """Placeholder function for Stop Button.

    Will make an API call to stop Gridlington simulation and Datahub.

    """
    if n_clicks is None:
        raise PreventUpdate
    print("Clicked Stop Button!")
    return "clicked"


@callback(Output("button_refresh", "className"), [Input("button_refresh", "n_clicks")])
def refresh_button_click(n_clicks):  # type: ignore # noqa
    """Placeholder function for Refresh Button.

    Will make an API call to refresh OVE spaces.

    """
    if n_clicks is None:
        raise PreventUpdate
    print("Clicked Refresh Button!")
    return "clicked"
