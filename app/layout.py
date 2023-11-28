"""Module for generating figure grid layout."""
from dash import html  # type: ignore


class GridBuilder:
    """_summary_."""

    def __init__(
        self,
        rows: int,
        cols: int,
        row_heights: list[str] = None,  # type: ignore
        col_widths: list[str] = None,  # type:ignore
    ):
        """_summary_.

        Args:
            rows (int): _description_
            cols (int): _description_
            row_heights (list[str], optional): _description_. Defaults to None.
            col_widths (list[str], optional): _description_. Defaults to None.
        """
        self.rows = rows
        self.cols = cols
        self.row_heights = row_heights
        self.col_widths = col_widths
        self.row_heights = row_heights
        self.col_widths = col_widths
        if not self.row_heights:
            self.row_heights = [f"{100 / rows}vh"] * rows
        if not self.col_widths:
            self.col_widths = [f"{100 / cols}%" for _ in range(cols)]
        self.grid_elements = [[None] * cols for _ in range(rows)]

    def add_element(self, element: html.Div, row: int, col: int) -> None:
        """_summary_.

        Args:
            element (html.Div): _description_
            row (int): _description_
            col (int): _description_

        Raises:
            ValueError: _description_
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid_elements[row][col] = element
        else:
            raise ValueError("Invalid row or column index.")

    def build_layout(self) -> html.Div:
        """_summary_.

        Returns:
            html.Div: _description_
        """
        grid_layout = html.Div(
            style={
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "space-around",
            },
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "justify-content": "space-around",
                        "height": self.row_heights[i],
                    },
                    children=[
                        html.Div(
                            style={"width": self.col_widths[j]},
                            children=[self.grid_elements[i][j]],
                        )
                        for j in range(self.cols)
                    ],
                )
                for i in range(self.rows)
            ],
        )

        return grid_layout
