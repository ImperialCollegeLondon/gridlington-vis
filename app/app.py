"""Sets up the server for the Dash app."""
import dash  # type: ignore
from dash import Dash, dcc, html  # type: ignore

app = Dash(__package__, use_pages=True, update_title=None)

app.layout = html.Div(
    style={"backgroundColor": "#F9F9F9"},
    children=[
        html.H1("Multi-page app with Dash Pages"),
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"]
                    )
                )
                for page in dash.page_registry.values()
            ]
        ),
        dash.page_container,
        html.H2("Footer", style={"float": "right", "backgroundColor": "#F9F9F9"}),
    ],
)

server = app.server


if __name__ == "__main__":
    app.run_server(debug=True)
