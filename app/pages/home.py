"""Home Page for Dash app."""

import dash  # type: ignore
from dash import html  # type: ignore

dash.register_page(__name__, path="/")

layout = html.Div(
    style={"backgroundColor": "#F9F9F9"},
    children=[
        html.H1(children="This is our Home page"),
        html.Div(
            children="""
        This is our Home page content.
    """
        ),
    ],
)
