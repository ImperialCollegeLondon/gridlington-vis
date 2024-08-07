"""Functions for generating plotly figures."""

from functools import wraps
from typing import Callable, Union

import numpy as np
import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
from plotly.colors import DEFAULT_PLOTLY_COLORS  # type: ignore
from plotly.subplots import make_subplots  # type: ignore

from .svg import (
    generate_map_location_svg,
    generate_sld_location_svg,
    get_agent_map_coordinates,
    get_agent_sld_coordinates,
    get_ev_map_coordinates,
    get_ev_sld_coordinates,
    svg_map,
    svg_sld,
)

time_range = ["2035-01-22 04:00", "2035-01-22 11:00"]


def figure(title: str, title_size: float = 30) -> Callable:  # type: ignore[type-arg]
    """Decorator for common formatting of all figures.

    Args:
        title (str): Title
        title_size (float, optional): Title size. Defaults to 30.

    Returns:
        Callable: Decorated function
    """

    def decorator(func: Callable) -> Callable:  # type: ignore[type-arg]
        @wraps(func)
        def wrapper(df: pd.DataFrame) -> Union[px.pie, px.line, go.Figure]:
            fig = func(df)
            fig.update_layout(
                title_text=title,
                title={"font": {"size": title_size}},
                title_x=0.5,
            )
            return fig

        return wrapper

    return decorator


def axes(
    ylabel: str,
    yrange: list[str | float],
    xlabel: str = "Time",
    xrange: list[str | float] = time_range,  # type:ignore
    xdomain: list[float] = [0, 1],
    ydomain: list[float] = [0, 1],
    xlabel_size: float = 15,
    ylabel_size: float = 15,
    xticklabel_size: float = 15,
    yticklabel_size: float = 15,
) -> Callable:  # type: ignore[type-arg]
    """Decorator to set axis labels and ranges.

    Args:
        ylabel (str): Y axis label
        yrange (list[str  |  float]): Y axis range
        xlabel (str, optional): X axis label. Defaults to "Time".
        xrange (list[str  |  float], optional): X-axis range.
            Defaults to time_range.
        xdomain (list[float], optional): Region of figure width occupied by
            the x-axis. Defaults to [0, 1].
        ydomain (list[float], optional): Region of figure height occupied by
            the y-axis. Defaults to [0, 1].
        xlabel_size (float, optional): X axis label size. Defaults to 15.
        ylabel_size (float, optional): Y axis label size. Defaults to 15.
        xticklabel_size (float, optional): X axis tick label size.
            Defaults to 15.
        yticklabel_size (float, optional): Y axis tick label size.
            Defaults to 15.

    Returns:
        Callable: Decorated function
    """

    def decorator(func: Callable) -> Callable:  # type: ignore[type-arg]
        @wraps(func)
        def wrapper(df: pd.DataFrame) -> Union[px.pie, px.line, go.Figure]:
            fig = func(df)

            # X axis
            fig.layout.xaxis.title = xlabel
            fig.layout.xaxis.titlefont.size = xlabel_size
            fig.layout.xaxis.tickfont.size = xticklabel_size
            fig.layout.xaxis.range = xrange
            if xlabel == "Time":
                fig.update_xaxes(type="date")

            # Y axis
            fig.layout.yaxis.title = ylabel
            fig.layout.yaxis.titlefont.size = ylabel_size
            fig.layout.yaxis.tickfont.size = yticklabel_size
            fig.layout.yaxis.range = yrange

            # Layout
            fig.update_layout(xaxis=dict(domain=xdomain), yaxis=dict(domain=ydomain))
            return fig

        return wrapper

    return decorator


def timestamp(
    x: float = 0, y: float = 1, fontsize: float = 15, color: str = "black"
) -> Callable:  # type: ignore[type-arg]
    """Decorator to add timestamp to figure.

    Coordinate scheme: x=0, y=1 corresponds to top left

    Args:
        x (float, optional): x coordinate of the timestamp. Defaults to 0.
        y (float, optional): y coordinate of the timestamp. Defaults to 1.
        fontsize (float, optional): font size
        color (str, optional): text color

    Returns:
        Callable: Decorated function
    """

    def decorator(func: Callable) -> Callable:  # type: ignore[type-arg]
        @wraps(func)
        def wrapper(df: pd.DataFrame) -> Union[px.pie, px.line, go.Figure]:
            fig = func(df)

            if not len(df.columns) == 1:
                fig.add_annotation(
                    text=df.iloc[-1]["Time"],
                    x=x,
                    y=y,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=fontsize, color=color),
                )

            return fig

        return wrapper

    return decorator


def legend(
    show_legend: bool = True,
    legend_font_size: int = 15,
    legend_title: str | None = None,
    legend_title_font_size: int = 20,
    x: float = 1,
    y: float = 1,
) -> Callable:  # type: ignore[type-arg]
    """Decorator to set legend properties.

    Args:
        show_legend (bool, optional): Show/hide the legend.
            Defaults to True.
        legend_font_size (int, optional): Font size of the legend items.
            Defaults to 15.
        legend_title (str, optional): Legend title. Defaults to None,
            which means no title.
        legend_title_font_size (int, optional): Font size of the title.
            Defaults to 20.
        x (float, optional): x position of the legend. Defaults to 1
            (rightmost).
        y (float, optional): y position of the legend. Defaults to 1
            (topmost).

    Returns:
        Callable: Decorated function
    """

    def decorator(func: Callable) -> Callable:  # type: ignore[type-arg]
        @wraps(func)
        def wrapper(df: pd.DataFrame) -> Union[px.pie, go.Figure]:
            fig = func(df)

            # Legend
            fig.update_layout(
                showlegend=show_legend,
                legend=dict(
                    font=dict(size=legend_font_size),
                    title=dict(
                        text=legend_title, font=dict(size=legend_title_font_size)
                    ),
                    x=x,
                    y=y,
                ),
            )

            return fig

        return wrapper

    return decorator


def combine_left_right_subplots(fig_left: go.Figure, fig_right: go.Figure) -> go.Figure:
    """Assembles two go.Figure objects into left-right subplots.

    Must specify xdomain for the two subplots using the axes decorator to
        avoid overlap

    Args:
        fig_left (go.Figure): Left figure
        fig_right (go.Figure): Right figure

    Returns:
        go.Figure: Combined figure
    """
    fig = make_subplots(rows=1, cols=2)

    # Transfer data from original figures
    for trace in fig_left.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in fig_right.data:
        fig.add_trace(trace, row=1, col=2)

    # Transfer layout properties from original figures
    fig.layout.xaxis.update(fig_left.layout.xaxis)
    fig.layout.yaxis.update(fig_left.layout.yaxis)
    fig.layout.xaxis2.update(fig_right.layout.xaxis)
    fig.layout.yaxis2.update(fig_right.layout.yaxis)

    return fig


power_sources = [
    "Battery Generation",
    "Interconnector Power",
    "Offshore Wind Generation",
    "Onshore Wind Generation",
    "Other Generation",
    "Pump Generation",
    "Pv Generation",
    "Nuclear Generation",
    "Hydro Generation",
    "Gas Generation",
]

power_sources_names = [
    "Battery",
    "Interconnectors",
    "Offshore Wind",
    "Onshore Wind",
    "Other",
    "Pumped Hydro",
    "Solar PV",
    "Nuclear",
    "Hydro",
    "Gas",
]

power_sources_colors = {
    s: c for s, c in zip(power_sources, DEFAULT_PLOTLY_COLORS[: len(power_sources)])
}


@figure("Generation Split")
@legend()
@timestamp(y=0, x=1)
def generate_gen_split_fig(df: pd.DataFrame) -> px.pie:
    """Creates Plotly figure for Generation Split graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly express figure
    """
    if len(df.columns) == 1:
        fig = go.Figure(go.Pie())
    else:
        # Data
        values = df.iloc[-1].loc[power_sources]
        values_negative, names_negative = zip(
            *[(val, name) for val, name in zip(values, power_sources) if val < 0]
        )
        values_positive, names_positive = zip(
            *[(val, name) for val, name in zip(values, power_sources) if val >= 0]
        )
        sum_negative = -sum(values_negative)
        sum_positive = sum(values_positive)
        diameter_left = 1  # fixed diameter for left pie
        diameter_right = diameter_left * (sum_negative / sum_positive) ** 0.5

        # Left pie
        pie_left = go.Pie(
            labels=names_positive,
            values=values_positive,
            domain={
                "x": [0, 0.5],
                "y": [0.5 - diameter_left / 2, 0.5 + diameter_left / 2],
            },
            marker=dict(colors=[power_sources_colors[n] for n in names_positive]),
            legendgroup="1",
            sort=False,
            direction="clockwise",
        )

        # Right pie
        pie_right = go.Pie(
            labels=names_negative,
            values=[-v for v in values_negative],
            domain={
                "x": [0.5, 1],
                "y": [0.5 - diameter_right / 2, 0.5 + diameter_right / 2],
            },
            marker=dict(colors=[power_sources_colors[n] for n in names_negative]),
            legendgroup="2",
            sort=False,
            direction="clockwise",
        )

        # Figure
        fig = go.Figure(data=[pie_left, pie_right])
        fig.update_traces(
            textposition="inside",
            texttemplate="%{value:.1f} GW",
        )
        fig.update_layout(
            uniformtext_minsize=15,
            uniformtext_mode="hide",
            legend_tracegroupgap=50,
        )

        # Titles
        title_kwargs = {
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "font": dict(size=24),
        }
        fig.add_annotation(
            text="Power Generation",
            x=0.18,
            y=1,
            **title_kwargs,
        )
        fig.add_annotation(
            text="Storage/Interconnector Use",
            x=0.86,
            y=1,
            **title_kwargs,
        )

    return fig


@figure("Generation Total")
@legend()
@axes(ylabel="Power Generation (GW)", yrange=[-5, 70])
def generate_total_gen_fig(df: pd.DataFrame) -> px.line:
    """Creates Plotly figure for Total Generation graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly express figure
    """
    if len(df.columns) == 1:
        total_gen_fig = px.line()
    else:
        total_gen_fig = px.line(
            df,
            x="Time",
            y=["Total Generation"] + power_sources,
            color_discrete_map={**power_sources_colors, "Total Generation": "black"},
        )

    return total_gen_fig


@figure("Demand Total")
@legend(show_legend=False)
@axes(ylabel="Total Demand (GW)", yrange=[30, 60])
def generate_total_dem_fig(df: pd.DataFrame) -> px.line:
    """Creates Plotly figure for Total Demand graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly express figure
    """
    if len(df.columns) == 1:
        total_dem_fig = px.line()
    else:
        total_dem_fig = px.line(
            df,
            x="Time",
            y=[
                "Total Demand",
            ],
        )
    return total_dem_fig


@figure("System Frequency")
@legend()
@axes(ylabel="Hz", yrange=[30, 70])
def generate_system_freq_fig(df: pd.DataFrame) -> px.line:
    """Creates Plotly figure for System Frequency graph.

    TODO: This is using placeholder data. Update when data is available
    https://github.com/ImperialCollegeLondon/gridlington-vis/issues/73

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly express figure
    """
    if len(df.columns) == 1:
        system_freq_fig = px.line()
    else:
        system_freq_fig = px.line(
            df,
            x="Time",
            y=[
                "Total Generation",
                "Total Demand",
            ],
        )

    return system_freq_fig


@axes(ylabel="Power (MW)", yrange=[-100, 100], xdomain=[0, 0.43])
def generate_intraday_market_sys_fig_left(df: pd.DataFrame) -> go.Figure:
    """Generate left panel of Intraday Market System figure.

    Args:
        df (pd.DataFrame): Opal Dataframe

    Returns:
        go.Figure: Plotly figure
    """
    if len(df.columns) == 1:
        intraday_market_sys_fig_left = go.Figure(go.Scatter())
    else:
        columns = [
            "Intra-Day Market Generation",
            "Intra-Day Market Storage",
            "Intra-Day Market Demand",
        ]
        col_names = [
            "Gen.",
            "Sto.",
            "DSR",
        ]
        intraday_market_sys_fig_left = go.Figure(
            [
                go.Scatter(
                    x=df["Time"],
                    y=df[columns[c]],
                    mode="lines",
                    name=col_names[c],
                    showlegend=True,
                )
                for c in [0, 1, 2]
            ]
        )
    return intraday_market_sys_fig_left


@axes(ylabel="Value (£/MW)", yrange=[-50000, 50000], xdomain=[0.57, 1])
def generate_intraday_market_sys_fig_right(df: pd.DataFrame) -> px.line:
    """Generate right panel of Intraday Market System figure.

    Args:
        df (pd.DataFrame): Opal dataframe

    Returns:
        px.line: Plotly figure
    """
    if len(df.columns) == 1:
        intraday_market_sys_fig_right = go.Figure(go.Scatter())
    else:
        intraday_market_sys_fig_right = go.Figure(
            go.Scatter(
                x=df["Time"],
                y=df["Intra-Day Market Value"],
                mode="lines",
                showlegend=False,
            )
        )
    return intraday_market_sys_fig_right


@figure("Intra-day Market System")
@legend(x=0, y=1)
def generate_intraday_market_sys_fig(df: pd.DataFrame) -> go.Figure:
    """Creates Intra-day Market System figure.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly graph_objects figure
    """
    intraday_market_sys_fig_left = generate_intraday_market_sys_fig_left(df)
    intraday_market_sys_fig_right = generate_intraday_market_sys_fig_right(df)
    intraday_market_sys_fig = combine_left_right_subplots(
        intraday_market_sys_fig_left, intraday_market_sys_fig_right
    )
    return intraday_market_sys_fig


@axes(ylabel="Power (MW)", yrange=[-250, 250], xdomain=[0, 0.43])
def generate_balancing_market_fig_left(df: pd.DataFrame) -> go.Figure:
    """Generate left panel for Balancing Market figure.

    Args:
        df (pd.DataFrame): Opal dataframe

    Returns:
        go.Figure: Plotly figure
    """
    if len(df.columns) == 1:
        balancing_market_fig_left = go.Figure(go.Scatter())
    else:
        columns = [
            "Balancing Mechanism Generation",
            "Balancing Mechanism Storage",
            "Balancing Mechanism Demand",
        ]
        col_names = [
            "Gen.",
            "Sto.",
            "DSR",
        ]
        balancing_market_fig_left = go.Figure(
            [
                go.Scatter(
                    x=df["Time"],
                    y=df[columns[c]],
                    mode="lines",
                    name=col_names[c],
                    showlegend=True,
                )
                for c in [0, 1, 2]
            ]
        )
    return balancing_market_fig_left


@axes(ylabel="Value (£/MW)", yrange=[-50000, 50000], xdomain=[0.57, 1])
def generate_balancing_market_fig_right(df: pd.DataFrame) -> go.Figure:
    """Generate right panel for Balancing Market figure.

    Args:
        df (pd.DataFrame): Opal dataframe

    Returns:
        go.Figure: Plotly figure
    """
    if len(df.columns) == 1:
        balancing_market_fig_right = go.Figure(go.Scatter())
    else:
        balancing_market_fig_right = go.Figure(
            go.Scatter(
                x=df["Time"],
                y=df["Balancing Mechanism Value"],
                mode="lines",
                showlegend=False,
            )
        )
    return balancing_market_fig_right


@figure("Balancing Market")
@legend(x=0, y=1)
def generate_balancing_market_fig(df: pd.DataFrame) -> go.Figure:
    """Creates Plotly figure for Balancing Market graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly graph_objects figure
    """
    balancing_market_fig_left = generate_balancing_market_fig_left(df)
    balancing_market_fig_right = generate_balancing_market_fig_right(df)
    balancing_market_fig = combine_left_right_subplots(
        balancing_market_fig_left, balancing_market_fig_right
    )
    return balancing_market_fig


@figure("Energy Deficit")
@axes(ylabel="Energy Deficit (MW)", yrange=[-600, 600])
def generate_energy_deficit_fig(df: pd.DataFrame) -> px.line:
    """Creates Plotly figure for Energy Deficit graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly express figure
    """
    if len(df.columns) == 1:
        energy_deficit_fig = px.line()
    else:
        energy_deficit_fig = px.line(
            df,
            x="Time",
            y=df["Exp. Offshore Wind Generation"] - df["Real Offshore Wind Generation"],
        )

    return energy_deficit_fig


@figure("Intraday Market Bids and Offers")
def generate_intraday_market_bids_fig(df: pd.DataFrame) -> go.Figure:
    """Creates plotly Figure object for Intraday Market Bids and Offers table.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly graph_objects figure
    """
    if len(df.columns) == 1:
        intraday_market_bids_fig = go.Figure()

    else:
        columns = ["Power", "Cost"]  # TODO: Units?
        data = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]  # TODO: Replace with real data
        intraday_market_bids_fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=columns, align="left", height=30, font=dict(size=20)
                    ),
                    cells=dict(
                        values=data, align="left", height=30, font=dict(size=20)
                    ),
                )
            ]
        )

    return intraday_market_bids_fig


@axes(ylabel="kW", yrange=[-1, 1], xdomain=[0, 0.43])
def generate_dsr_fig_left(df: pd.DataFrame) -> go.Figure:
    """Generate left panel of Demand Side Response figure.

    TODO: this will need to be fixed when the data is available
    Will either be in DSR or Opal

    See https://github.com/ImperialCollegeLondon/gridlington-vis/issues/34#issuecomment-1768200705

    Args:
        df (pd.DataFrame): DSR data DataFrame

    Returns:
        go.Figure: Plotly figure
    """
    if len(df.columns) == 1:
        dsr_fig_left = go.Figure(go.Scatter())
    else:
        columns = [
            "Cost",  # TODO: This will need to be changed when data is available
            "Cost",
        ]
        dsr_fig_left = go.Figure(
            [
                go.Scatter(
                    x=df["Time"],
                    y=df[c],
                    mode="lines",
                    name=c,
                    showlegend=True,
                )
                for c in columns
            ]
        )
    return dsr_fig_left


@axes(ylabel="Cost (£/MW)", yrange=[-1, 1], xdomain=[0.57, 1])
def generate_dsr_fig_right(df: pd.DataFrame) -> go.Figure:
    """Generate right panel of Demand Side Response figure.

    TODO: this will need to be checked when the DSR data is available

    Args:
        df (pd.DataFrame): DSR data DataFrame

    Returns:
        go.Figure: Plotly figure
    """
    if len(df.columns) == 1:
        dsr_fig_right = go.Figure(go.Scatter())
    else:
        dsr_fig_right = go.Figure(
            go.Scatter(
                x=df["Time"],
                y=df["Cost"],
                mode="lines",
                showlegend=False,
            )
        )
    return dsr_fig_right


@figure("Demand Side Response")
@legend(x=0, y=1)
def generate_dsr_fig(df: pd.DataFrame) -> go.Figure:
    """Creates plotly figure for Demand Side Response graph.

    TODO: double check this when all the data is available

    Args:
        df: DSR data DataFrame (TODO: may take opal as well)

    Returns:
        Plotly graph objects figure
    """
    dsr_fig_left = generate_dsr_fig_left(df)
    dsr_fig_right = generate_dsr_fig_right(df)
    dsr_fig = combine_left_right_subplots(dsr_fig_left, dsr_fig_right)
    return dsr_fig


@figure("DSR Commands to Agents")
@axes(ylabel="MW", yrange=[-8, 8])
def generate_dsr_commands_fig(df: pd.DataFrame) -> px.line:
    """Creates Plotly figure for DSR Commands to Agents graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly express figure
    """
    if len(df.columns) == 1:
        dsr_commands_fig = px.line()
    else:
        figure_data = df[
            [
                "Time",
            ]
        ].copy()
        figure_data["Name"] = (  # TODO: Give this column an appropriate name
            df["Real Gridlington Demand"] - df["Expected Gridlington Demand"]
        ) + (df["Real Ev Charging Power"] - df["Expected Ev Charging Power"])
        figure_data["Name2"] = (  # TODO: Give this column an appropriate name
            df["Real Ev Charging Power"] - df["Expected Ev Charging Power"]
        )
        dsr_commands_fig = px.line(
            figure_data,
            x="Time",
            y=[
                "Name",
                "Name2",
            ],
        )

    dsr_commands_fig.update_layout(
        legend_title=None,
        legend=dict(font=dict(size=15)),
    )
    return dsr_commands_fig


def sainte_lague_algorithm(votes: list[int], seats: int) -> list[int]:
    """Saint-Lague algorithm for proportional representation in voting.

    https://en.wikipedia.org/wiki/Sainte-Lagu%C3%AB_method

    In general, this can be used to allocate a limited set of resources
        (seats) to a large population of agents (votes)
    Used below to allocate squares in waffle plots

    Args:
        votes (list[int]): List of votes
        seats (int): Total number of seats

    Returns:
        list: Number of seats allocated to each party
    """
    allocated_seats = [0] * len(votes)

    for _ in range(seats):
        quotients = [v / (2 * a + 1) for v, a in zip(votes, allocated_seats)]
        max_index = quotients.index(max(quotients))
        allocated_seats[max_index] += 1

    return allocated_seats


def create_waffle_chart(
    categories: list[str],
    counts: list[int],
    label: str,
    colors: list[str] | None = None,
    squares: int | None = None,
    rows: int | None = None,
    gap: float = 0.0,
) -> go.Figure:
    """Create waffle chart.

    Args:
        categories (list[str]): List of categories
        counts (list[int]): List of counts
        label (str): Text label used in the scale annotation
        colors (list[str], optional): List of colors. If None, will use plotly
            default color map. Defaults to None.
        squares (int, optional): Total number of squares in the waffle plot.
            If set, will allocate counts to this many squares based on a
            proportional representation algorithm. If None, will default to
            sum(counts) (i.e. no proportional representation). Defaults to None.
        rows (int, optional): Number of rows in the chart. Number of columns
            is set automatically. If None, will produce a square chart.
            Defaults to None.
        gap (str, optional): Gap between squares (pixel units). Defaults to 0.0.

    Raises:
        ValueError: Raised if categories, counts and colors are not equal length
        TypeError: Raised if counts are not integers

    Returns:
        go.Figure: Waffle chart
    """
    # Set default colors
    if not colors:
        colors = [DEFAULT_PLOTLY_COLORS[i] for i in range(len(categories))]

    # Check fields, counts, colors are all same length
    if not len(categories) == len(counts) == len(colors):
        raise ValueError(
            "categories, counts and colors (if specified) must be "
            "lists of equal length"
        )

    # Check counts is all integers
    if not all(isinstance(item, int) for item in counts):
        raise TypeError("Counts must be integers")

    # Proportional representation
    counts_pr = sainte_lague_algorithm(counts, squares) if squares else counts

    # Shape
    total = sum(counts_pr)
    if not rows:
        rows = max(int(total**0.5), 1)  # Default to square chart
    columns = int(np.ceil(total / rows))

    # Create numpy array
    z_flat = np.ones([columns * rows])
    z_flat[:total] = [
        i / len(categories) for i, c in enumerate(counts_pr) for _ in range(c)
    ]
    z = z_flat.reshape((rows, columns))

    # Create color scale
    colorscale = [[i / len(categories), c] for i, c in enumerate(colors)]
    colorscale.append([1, "rgb(255, 255, 255)"])

    # Create legend labels
    labels = [f"{category} ({count})" for category, count in zip(categories, counts)]

    # Legend
    legend_traces = [
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            name=label,
            marker=dict(size=7, color=col, symbol="square"),
        )
        for label, col in zip(labels, colors)
    ]

    # Waffle plot
    waffle = go.Figure(
        legend_traces
        + [
            go.Heatmap(
                z=z,
                xgap=gap,
                ygap=gap,
                colorscale=colorscale,
                showscale=False,
                zmin=0,
                zmax=1,
            )
        ]
    )

    # Scale
    if squares:
        text = f"Scale:<br>1 square ≈ {round(sum(counts) / squares)} {label}s"
    else:
        text = f"Scale:<br>1 square = 1 {label}"
    waffle.add_annotation(
        text=text,
        x=1.02,
        y=0,
        xref="paper",
        yref="paper",
        align="left",
        xanchor="left",
        showarrow=False,
        font=dict(size=15, color="black"),
    )

    waffle.update_layout(
        yaxis=dict(scaleanchor="x"),
        plot_bgcolor="rgba(0,0,0,0)",
    )
    waffle.update_xaxes(visible=False)
    waffle.update_yaxes(visible=False, autorange="reversed")
    return waffle


@figure("Agent Activity Breakdown")
@legend()
@timestamp(y=1.05)
def generate_agent_activity_breakdown_fig(df: pd.DataFrame) -> go.Figure:
    """Creates waffle chart for agent activity breakdown figure.

    TODO: total number of agents is changing at each timestep

    Args:
        df: Opal dataframe

    Returns:
        Waffle chart
    """
    if len(df.columns) == 1:
        agent_activity_breakdown_fig = go.Figure()
    else:
        household_activities = [
            c for c in df.columns.values.tolist() if "Household Activity" in c
        ]
        categories = [h.split("(")[1].split(")")[0] for h in household_activities]
        counts = [int(df[h].iloc[-1]) for h in household_activities]
        agent_activity_breakdown_fig = create_waffle_chart(
            categories=categories,
            counts=counts,
            label="agent",
            squares=546,  # for consistency with EV chart (below)
            gap=1,
            rows=21,  # -> 26 columns
        )
    agent_activity_breakdown_fig.update_layout(
        legend_title_text="Household Activity",
    )
    return agent_activity_breakdown_fig


@figure("Electric Vehicle Charging Breakdown")
@legend()
@timestamp(y=1.05)
def generate_ev_charging_breakdown_fig(df: pd.DataFrame) -> go.Figure:
    """Creates waffle chart for EV charging breakdown figure.

    Args:
        df: Opal dataframe

    Returns:
        Waffle chart
    """
    if len(df.columns) == 1:
        ev_charging_breakdown_fig = go.Figure()
    else:
        ev_states = [c for c in df.columns.values.tolist() if "Ev Status" in c]
        categories = [h.split("(")[1].split(")")[0] for h in ev_states]
        counts = [int(df[h].iloc[-1]) for h in ev_states]  # sum(counts) = 546
        ev_charging_breakdown_fig = create_waffle_chart(
            categories=categories,
            counts=counts,
            label="EV",
            gap=1,
            rows=21,  # -> 26 columns
        )
    ev_charging_breakdown_fig.update_layout(
        legend_title_text="EV Status",
    )
    return ev_charging_breakdown_fig


@figure("Weather")
def generate_weather_fig(wesim_data: dict[str, pd.DataFrame]) -> go.Figure:
    """Creates plotly figure for Weather table.

    Sun and wind levels are allocated to bins with associated icons.
    Bin thresholds (sun_bins, wind_bins) can be modified as appropriate.

    Args:
        wesim_data: Wesim data (dictionary of dataframes)

    Returns:
        Plotly figure
    """
    hours = [4, 5, 6, 7, 8, 9, 10, 11]

    sun_bins = [0, 0.05, 0.1]
    sun_labels = [
        "\U00002601\U0000FE0F",
        "\U0001F324\U0000FE0F",
        "\U00002600\U0000FE0F",
    ]
    wind_bins = [0, 0.05, 0.1]
    wind_labels = [
        "\U0001F4A8",
        "\U0001F4A8\U0001F4A8",
        "\U0001F4A8\U0001F4A8\U0001F4A8",
    ]

    if len(wesim_data) == 1:
        weather_fig = go.Figure()

    else:
        wesim_regions = wesim_data["Regions"]
        wesim_capacity = wesim_data["Capacity"]
        wesim_regions_total = wesim_regions[wesim_regions["Code"] == "Total"]
        wesim_capacity_total = wesim_capacity[wesim_capacity["Code"] == "Total"]
        solar_capacity = wesim_capacity_total["Solar PV"].to_list()[0]
        wind_capacity = wesim_capacity_total["Onshore wind"].to_list()[0]

        table_df = wesim_regions_total[
            ["Hour", "Time", "Solar PV", "Onshore wind"]
        ].copy()
        table_df = table_df[table_df["Hour"].isin(hours)]

        def label_output(
            output: float, capacity: float, bins: list[float], labels: list[str]
        ) -> str:
            output_norm = output / capacity
            output_labelled = labels[np.digitize(output_norm, bins) - 1]
            return output_labelled

        table_solar_labels = [
            label_output(o, solar_capacity, sun_bins, sun_labels)
            for o in table_df["Solar PV"].to_list()
        ]
        table_wind_labels = [
            label_output(o, wind_capacity, wind_bins, wind_labels)
            for o in table_df["Onshore wind"].to_list()
        ]

        columns = table_df["Time"]
        data = list(zip(table_solar_labels, table_wind_labels))

        weather_fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=columns, align="center", height=30, font=dict(size=20)
                    ),
                    cells=dict(
                        values=data, align="center", height=50, font=dict(size=30)
                    ),
                )
            ]
        )

    return weather_fig


@figure("Reserve/Standby Generation")
@axes(ylabel="Reserve/Standby Generation (MW)", yrange=[25000, 35000])
def generate_reserve_generation_fig(wesim_data: dict[str, pd.DataFrame]) -> go.Figure:
    """Creates Plotly figure for Reserve/Standby Generation graph.

    Args:
        wesim_data: Wesim data (dictionary of dataframes)

    Returns:
        Plotly express line graph
    """
    if len(wesim_data) == 1:
        reserve_generation_fig = px.line()
    else:
        wesim_regions = wesim_data["Regions"]
        wesim_capacity = wesim_data["Capacity"]

        solar_capacity = wesim_capacity[wesim_capacity["Code"] == "Total"][
            "Solar PV"
        ].squeeze()
        wesim_regions_total = wesim_regions[(wesim_regions["Code"] == "Total")].copy()
        wesim_regions_total.loc[:, "Solar Reserve"] = wesim_regions_total.apply(
            lambda x: solar_capacity - x["Solar PV"], axis=1
        )

        reserve_generation_fig = px.line(
            wesim_regions_total,
            x="Time",
            y="Solar Reserve",
        )
    return reserve_generation_fig


@figure("Agent and EV Locations")
def generate_map_fig(df: pd.DataFrame) -> go.Figure:
    """Creates map figure.

    Args:
        df (pd.DataFrame): Opal dataframe

    Returns:
        go.Figure: Plotly figure object
    """
    agent_x, agent_y = get_agent_map_coordinates(df)
    agent_svg = generate_map_location_svg(agent_x, agent_y, colour="#6A0DAD")
    ev_x, ev_y = get_ev_map_coordinates(df)
    ev_svg = generate_map_location_svg(ev_x, ev_y, colour="#fcba03")

    map_fig = go.Figure()
    args = {"x": 0, "y": 1, "xref": "paper", "yref": "paper", "sizex": 1, "sizey": 1}
    map_fig.add_layout_image(source=svg_map.url, **args)
    map_fig.add_layout_image(source=agent_svg.url, **args)
    map_fig.add_layout_image(source=ev_svg.url, **args)
    map_fig.update_layout(yaxis=dict(scaleanchor="x"), plot_bgcolor="rgba(0,0,0,0)")
    map_fig.update_xaxes(visible=False)
    map_fig.update_yaxes(visible=False)
    return map_fig


@figure("Agent and EV Locations on SLD")
def generate_sld_fig(df: pd.DataFrame) -> go.Figure:
    """Creates SLD figure.

    Args:
        df (pd.DataFrame): Opal dataframe

    Returns:
        go.Figure: Plotly figure object
    """
    agent_location_data = get_agent_sld_coordinates(df)
    agent_svg = generate_sld_location_svg(
        agent_location_data, angle_mid=180, colour="#6A0DAD"
    )
    ev_location_data = get_ev_sld_coordinates(df)
    ev_svg = generate_sld_location_svg(ev_location_data, angle_mid=0, colour="#fcba03")

    sld_fig = go.Figure()
    args = {"x": 0, "y": 1, "xref": "paper", "yref": "paper", "sizex": 1, "sizey": 1}
    sld_fig.add_layout_image(source=svg_sld.url, **args)
    sld_fig.add_layout_image(source=agent_svg.url, **args)
    sld_fig.add_layout_image(source=ev_svg.url, **args)
    sld_fig.update_layout(yaxis=dict(scaleanchor="x"), plot_bgcolor="rgba(0,0,0,0)")
    sld_fig.update_xaxes(visible=False)
    sld_fig.update_yaxes(visible=False)
    return sld_fig
