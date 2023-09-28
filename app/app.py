"""Sets up the server for the Dash app."""
import dash  # type: ignore
from dash import Dash, html  # type: ignore

app = Dash(__package__, use_pages=True, update_title=None)

app.layout = html.Div(
    style={"backgroundColor": "#F9F9F9"},
    children=[
        dash.page_container,
    ],
)

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
