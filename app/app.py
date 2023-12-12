"""Sets up the server for the Dash app."""
import dash  # type: ignore
from dash import Dash, Input, Output, callback, dcc, html  # type: ignore

from . import log

app = Dash(__package__, use_pages=True, update_title=None)

app.layout = html.Div(
    style={
        "backgroundColor": "#F9F9F9",
        "height": "100%",
    },
    children=[
        dash.page_container,
        dcc.Interval(id="figure_interval"),
    ],
)

server = app.server
log.info("Gridlington Visualisation System is running...")


@callback(
    [Output("figure_interval", "disabled"), Output("figure_interval", "interval")],
    [Input("figure_interval", "n_intervals")],
)
def update_interval(
    n_intervals: int,
) -> tuple[bool, int]:
    """_summary_.

    Args:
        n_intervals (int): _description_

    Returns:
        tuple[bool, int]: _description_
    """
    from .data import data_ended
    from .pages.control import interval

    return (data_ended, interval)


if __name__ == "__main__":
    app.run_server(debug=True)
