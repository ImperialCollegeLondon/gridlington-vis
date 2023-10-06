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


def get_dropdown(space: str, default: str) -> html.Div:
    """Function to generate dropdown menus."""
    div = html.Div(
        style={"width": "46%"},
        children=[
            html.H3(
                style={"text-align": "center", "margin": "0"},
                children=space,
            ),
            dcc.Dropdown(
                options,
                default,
                id=f"{space}_dropdown",
                clearable=False,
            ),
        ],
    )
    return div


def get_pc_dropdown(
    pc: str, default_1: str, default_2: str, default_3: str
) -> html.Div:
    """Function to generate dropdown menu group for PC displays."""
    div = html.Div(
        style={"width": "46%"},
        children=[
            html.Div(
                children=[
                    html.H3(
                        style={
                            "text-align": "center",
                            "margin": "0",
                        },
                        children=f"{pc}-Top",
                    ),
                    dcc.Dropdown(
                        options,
                        default_1,
                        id=f"{pc}-Top_dropdown",
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
                    get_dropdown(f"{pc}-Left", default_2),
                    get_dropdown(f"{pc}-Right", default_3),
                ],
            ),
        ],
    )
    return div


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
                        get_dropdown("Hub01", "Market"),
                        get_dropdown("Hub02", "Agent"),
                    ],
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justify-content": "space-around",
                        "padding": "6px 0",
                    },
                    children=[
                        get_pc_dropdown(
                            "PC01",
                            "NMX",
                            "Balance of Supply and Demand",
                            "Markets and Reserve",
                        ),
                        get_pc_dropdown(
                            "PC02",
                            "NMX Georgraphic Map",
                            "NMX 11kV Schematic",
                            "NMX Issues",
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
                        html.Button(
                            id="button_update",
                            style={
                                "padding": "20px",
                                "display": "grid",
                                "justify-content": "center",
                            },
                            children=[
                                DashIconify(icon="solar:upload-outline", width=100)
                            ],
                        ),
                        html.Button(
                            id="button_default",
                            style={
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
                        html.Button(
                            id="button_start",
                            style={
                                "padding": "20px",
                                "display": "grid",
                                "justify-content": "center",
                            },
                            children=[DashIconify(icon="ph:play-fill", width=100)],
                        ),
                        html.Button(
                            id="button_stop",
                            style={
                                "padding": "20px",
                                "display": "grid",
                                "justify-content": "center",
                            },
                            children=[DashIconify(icon="ri:stop-fill", width=100)],
                        ),
                        html.Button(
                            id="button_restart",
                            style={
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


@callback(Output("button_update", "className"), [Input("button_update", "n_clicks")])
def update_button_click(n_clicks):  # type: ignore # noqa
    """Placeholder function for Update Button.

    Will make an API call to set up OVE sections accoding to dropdowns.

    """
    if n_clicks is None:
        raise PreventUpdate
    print("Clicked Update Button!")
    return "clicked"


@callback(Output("button_default", "className"), [Input("button_default", "n_clicks")])
def default_button_click(n_clicks):  # type: ignore # noqa
    """Placeholder function for Update Button.

    Will make an API call to set up OVE sections accoding to default configuration.

    """
    if n_clicks is None:
        raise PreventUpdate
    print("Clicked Default Button!")
    return "clicked"


@callback(Output("button_start", "className"), [Input("button_start", "n_clicks")])
def start_button_click(n_clicks):  # type: ignore # noqa
    """Placeholder function for Start Button.

    Will make an API call to start the Gridlington simulation and Datahub.

    """
    if n_clicks is None:
        raise PreventUpdate
    print("Clicked Start Button!")
    return "clicked"


@callback(Output("button_stop", "className"), [Input("button_stop", "n_clicks")])
def stop_button_click(n_clicks):  # type: ignore # noqa
    """Placeholder function for Stop Button.

    Will make an API call to stop the Gridlington simulation and Datahub.

    """
    if n_clicks is None:
        raise PreventUpdate
    print("Clicked Stop Button!")
    return "clicked"


@callback(Output("button_restart", "className"), [Input("button_restart", "n_clicks")])
def restart_button_click(n_clicks):  # type: ignore # noqa
    """Placeholder function for Restart Button.

    Will make an API call to restart the Gridlington simulation and Datahub.

    """
    if n_clicks is None:
        raise PreventUpdate
    print("Clicked Restart Button!")
    return "clicked"
