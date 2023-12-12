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
def update_figure_interval(
    n_intervals: int,
) -> tuple[bool, int]:
    """Callback to synchronise the figure interval with the data interval.

    Args:
        n_intervals (int): Number of times the figures have updated

    Returns:
        data_ended (bool): Whether the data has ended
        interval (int): The interval between updates
    """
    from .data import data_ended
    from .pages.control import interval

    return data_ended, interval


if __name__ == "__main__":
    app.run_server(debug=True)
