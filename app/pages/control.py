"""Controller Page for Dash app."""

import dash  # type: ignore
from dash import Input, Output, State, callback, ctx, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore
from dash_iconify import DashIconify  # type: ignore

from .. import core_api as core
from .. import log
from ..data import data_interval, empty_output

dash.register_page(__name__)


options = [key for key in core.INIT_SECTIONS.keys() if key != "Control"]


def get_default(space: str) -> str:
    """Function to get default option for dropdown.

    Args:
        space: Name of the space

    Returns:
        The default section of the space
    """
    for key, val in core.INIT_SECTIONS.items():
        if val["space"] == space:
            default = key
    return default


def get_dropdown(space: str) -> html.Div:
    """Function to generate dropdown menus.

    Args:
        space: Name of the space

    Returns:
        Div containing dropdown menu
    """
    div = html.Div(
        style={"width": "46%"},
        children=[
            html.H3(
                style={"text-align": "center", "margin": "0"},
                children=space,
            ),
            dcc.Dropdown(
                options,
                get_default(space),
                id=f"{space}_dropdown",
                clearable=False,
            ),
        ],
    )
    return div


def get_pc_dropdown(pc: str) -> html.Div:
    """Function to generate dropdown menu group for PC displays.

    Args:
        pc: Name of the PC with a Top, Left and Right space

    Returns:
        Div containing multiple dropdown menus
    """
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
                        get_default(f"{pc}-Top"),
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
                    get_dropdown(f"{pc}-Left"),
                    get_dropdown(f"{pc}-Right"),
                ],
            ),
        ],
    )
    return div


def get_button(func: str, icon: str) -> html.Button:
    """Function to generate buttons.

    Args:
        func: Name of the button function
        icon: Path of the DashIconify icon

    Returns:
        Button element with desired id
    """
    button = html.Button(
        id=f"button_{func}",
        style={
            "padding": "20px",
            "display": "grid",
            "justify-content": "center",
        },
        children=[DashIconify(icon=icon, width=100)],
    )
    return button


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
                        get_dropdown("Hub01"),
                        get_dropdown("Hub02"),
                    ],
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justify-content": "space-around",
                        "padding": "6px 0",
                    },
                    children=[
                        get_pc_dropdown("PC01"),
                        get_pc_dropdown("PC02"),
                    ],
                ),
            ],
        ),
        html.Div(
            id="message",
            style={"text-align": "center"},
            children=["No buttons pressed yet..."],
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
                        get_button("update", "mdi:tick"),
                        get_button("default", "iconoir:undo"),
                    ],
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justify-content": "space-around",
                        "padding": "10px",
                    },
                    children=[
                        get_button("start", "ph:play-fill"),
                        get_button("stop", "ri:stop-fill"),
                        get_button("restart", "solar:refresh-bold"),
                    ],
                ),
            ],
        ),
        data_interval,
        empty_output,
    ],
)


@callback(
    Output("message", "children"),
    [
        Input("button_update", "n_clicks"),
        Input("button_default", "n_clicks"),
        Input("button_start", "n_clicks"),
        Input("button_stop", "n_clicks"),
        Input("button_restart", "n_clicks"),
    ],
    [
        State("Hub01_dropdown", "value"),
        State("Hub02_dropdown", "value"),
        State("PC01-Top_dropdown", "value"),
        State("PC01-Left_dropdown", "value"),
        State("PC01-Right_dropdown", "value"),
        State("PC02-Top_dropdown", "value"),
        State("PC02-Left_dropdown", "value"),
        State("PC02-Right_dropdown", "value"),
    ],
)
def update_button_click(
    button_update: int | None,
    button_default: int | None,
    button_start: int | None,
    button_stop: int | None,
    button_restart: int | None,
    Hub01_dropdown: str,
    Hub02_dropdown: str,
    PC01_Top_dropdown: str,
    PC01_Left_dropdown: str,
    PC01_Right_dropdown: str,
    PC02_Top_dropdown: str,
    PC02_Left_dropdown: str,
    PC02_Right_dropdown: str,
) -> list[str]:
    """Placeholder function for buttons."""
    button_id = ctx.triggered_id
    if ctx.triggered_id is None:
        raise PreventUpdate

    button_id = ctx.triggered_id[7:]

    if button_id == "update":
        """Will make an API call to set up OVE sections accoding to dropdowns.

        Args: Value inputs for the 8 dropdown menus
        """
        log.debug("Clicked Update Button!")
        core.assign_sections(
            {
                "Hub01": Hub01_dropdown,
                "Hub02": Hub02_dropdown,
                "PC01-Top": PC01_Top_dropdown,
                "PC01-Left": PC01_Left_dropdown,
                "PC01-Right": PC01_Right_dropdown,
                "PC02-Top": PC02_Top_dropdown,
                "PC02-Left": PC02_Left_dropdown,
                "PC02-Right": PC02_Right_dropdown,
            }
        )
        return ["Clicked Update Button!"]

    elif button_id == "default":
        """Will make an API call to set up OVE sections accoding to
        default configuration.

        Args: INIT_SECTIONS list from core_api.py
        """
        log.debug("Clicked Default Button!")
        return ["Clicked Default Button!"]

    elif button_id == "start":
        """Will make an API call to start the Gridlington simulation and Datahub."""
        log.debug("Clicked Start Button!")
        return ["Clicked Start Button!"]

    elif button_id == "stop":
        """Will make an API call to stop the Gridlington simulation and Datahub."""
        log.debug("Clicked Stop Button!")
        return ["Clicked Stop Button!"]

    elif button_id == "restart":
        """Will make an API call to restart the Gridlington simulation and Datahub."""
        log.debug("Clicked Restart Button!")
        return ["Clicked Restart Button!"]

    else:
        return [""]
