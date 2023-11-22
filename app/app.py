"""Sets up the server for the Dash app."""
import dash  # type: ignore
from dash import Dash, dcc, html  # type: ignore

from . import log

##################
interval = 7000
##################

app = Dash(__package__, use_pages=True, update_title=None)

app.layout = html.Div(
    style={
        "backgroundColor": "#F9F9F9",
        "height": "100%",
    },
    children=[
        dash.page_container,
        dcc.Interval(id="figure_interval", interval=interval),
    ],
)

server = app.server
log.info("Gridlington Visualisation System is running...")


if __name__ == "__main__":
    app.run_server(debug=True)
