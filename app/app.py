"""Sets up the server for the Dash app."""
import dash  # type: ignore
from dash import Dash, Input, Output, State, callback, dcc, html  # type: ignore

from . import log

app = Dash(__package__, use_pages=True, update_title=None)

app.layout = html.Div(
    style={
        "backgroundColor": "#F9F9F9",
        "height": "100%",
    },
    children=[
        dash.page_container,
        dcc.Store(id="figure_interval", data=0),
        dcc.Interval(id="sync_interval", interval=100),
    ],
)

server = app.server
log.info("Gridlington Visualisation System is running...")


@callback(
    [Output("figure_interval", "data")],
    [Input("sync_interval", "n_intervals")],
    [State("figure_interval", "data")],
)
def update_figure_interval(
    n_intervals_sync: int,
    n_intervals_figures: int,
) -> tuple[int]:
    """Callback to synchronise figure_interval with data_interval.

    This pulls in N_INTERVALS_DATA (number of times the data has updated) from
        the data module and increments figure_interval accordingly.

    Args:
        n_intervals_sync (int): Number of times this callback has run
        n_intervals_figures (int): Number of times the figures have updated

    Returns:
        N_INTERVALS_DATA (int): Number of times the data has updated
    """
    from .data import N_INTERVALS_DATA

    return (
        dash.no_update
        if n_intervals_figures == N_INTERVALS_DATA
        else (N_INTERVALS_DATA,)
    )


if __name__ == "__main__":
    app.run_server(debug=True)
