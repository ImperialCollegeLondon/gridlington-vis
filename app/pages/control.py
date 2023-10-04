"""Controller Page for Dash app."""

import dash  # type: ignore
from dash import dcc, html  # type: ignore
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
