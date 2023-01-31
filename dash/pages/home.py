import dash
from dash import html, dcc

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
