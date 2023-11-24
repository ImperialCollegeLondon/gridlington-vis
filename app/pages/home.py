"""Home Page for Dash app."""
from pathlib import Path

import dash  # type: ignore
from dash import dcc, html  # type: ignore

dash.register_page(__name__, path="/")

layout = html.Div(
    style={"backgroundColor": "#F9F9F9"},
    children=[
        html.H1(children="This is our Home page"),
        html.Div(
            children=[
                "This is our Home page content.",
                html.Div(
                    [
                        html.Div(
                            dcc.Link(
                                page.with_suffix("").name,
                                href=f"/{page.with_suffix('').name}",
                            )
                        )
                        for page in Path(__file__).parent.glob("*.py")
                    ]
                ),
            ]
        ),
    ],
)
