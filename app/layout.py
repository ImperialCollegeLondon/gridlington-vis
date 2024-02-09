"""Module for generating figure grid layout."""

from dash import html  # type: ignore


class GridBuilder:
    """Class for building a grid layout of graphs."""

    def __init__(
        self,
        rows: int,
        cols: int,
        row_heights: list[str] | None = None,
        col_widths: list[str] | None = None,
    ):
        """Initialise grid with specified rows and columns.

        Args:
            rows (int): Number of rows
            cols (int): Number of columns
            row_heights (list[str], optional): List of row heights (vh format).
                Defaults to None.
            col_widths (list[str], optional): List of column widths (vw format).
                Defaults to None.
        """
        if row_heights is None:
            row_heights = [f"{100 / rows}vh"] * rows
        if col_widths is None:
            col_widths = [f"{100 / cols}vw"] * cols

        self.rows = rows
        self.cols = cols
        self.row_heights = row_heights
        self.col_widths = col_widths
        self.grid_elements = [[None] * cols for _ in range(rows)]

    def add_element(self, element: html.Div, row: int, col: int) -> None:
        """Add an element to the grid at a specified position.

        Args:
            element (html.Div): Single div to add to the grid
            row (int): Row index
            col (int): Column index

        Raises:
            ValueError: Raised if row/column index is not in grid bounds
        """
        if 0 > row >= self.rows and 0 > col >= self.cols:
            raise ValueError("Invalid row or column index.")
        self.grid_elements[row][col] = element

    @property
    def layout(self) -> html.Div:
        """Builds a grid layout with the elements added so far.

        Returns:
            html.Div: The full grid layout as a div
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
                            style={
                                "width": self.col_widths[j],
                                "height": self.row_heights[i],
                            },
                            children=[
                                self.grid_elements[i][j],
                            ],
                        )
                        for j in range(self.cols)
                    ],
                )
                for i in range(self.rows)
            ],
        )

        return grid_layout
