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

    Returns:
        Callable: Decorated function
    """

    def decorator(func: Callable) -> Callable:  # type: ignore[type-arg]
        @wraps(func)
        def wrapper(df: pd.DataFrame) -> Union[px.pie, px.line, go.Figure]:
            fig = func(df)
            fig.layout.xaxis.title = xlabel
            fig.layout.xaxis.range = xrange
            if xlabel == "Time":
                fig.update_xaxes(type="date")
            fig.layout.yaxis.title = ylabel
            fig.layout.yaxis.range = yrange
            fig.update_layout(xaxis=dict(domain=xdomain), yaxis=dict(domain=ydomain))
            return fig

        return wrapper

    return decorator


def timestamp(
    x: float = 0, y: float = 1, fontsize: float = 14, color: str = "black"
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
power_sources_colors = {
    s: c for s, c in zip(power_sources, DEFAULT_PLOTLY_COLORS[: len(power_sources)])
}


@figure("Generation Split")
@timestamp()
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
        sum_positive = sum([v for v in values if v > 0])
        height_right = (sum_negative / sum_positive) ** 0.5

        # Left pie
        pie_left = go.Pie(
            labels=names_positive,
            values=values_positive,
            domain={"x": [0, 0.5], "y": [0, 1]},
            marker=dict(colors=[power_sources_colors[n] for n in names_positive]),
        )

        # Right pie
        pie_right = go.Pie(
            labels=names_negative,
            values=[-v for v in values_negative],
            domain={
                "x": [0.5, 1],
                "y": [0.5 - height_right / 2, 0.5 + height_right / 2],
            },
            marker=dict(colors=[power_sources_colors[n] for n in names_negative]),
        )

        # Figure
        fig = go.Figure(data=[pie_left, pie_right])
        fig.update_traces(
            textposition="inside",
            texttemplate="%{value:.1f}",
        )
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")

    return fig


@figure("Generation Total")
@axes(ylabel="GW", yrange=[-5, 70])
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
@axes(ylabel="GW", yrange=[-5, 70])
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
@axes(ylabel="Hz", yrange=[40, 70])
def generate_system_freq_fig(df: pd.DataFrame) -> px.line:
    """Creates Plotly figure for System Frequency graph.

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


@figure("Intra-day Market System")
def generate_intraday_market_sys_fig(df: pd.DataFrame) -> go.Figure:
    """Creates Plotly figure for Intra-day Market System graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly graph_objects figure
    """
    intraday_market_sys_fig = make_subplots(specs=[[{"secondary_y": True}]])

    if not len(df.columns) == 1:
        left_axis_columns = [
            "Intra-Day Market Generation",
            "Intra-Day Market Storage",
            "Intra-Day Market Demand",
        ]
        intraday_market_sys_fig_left = px.line(
            df,
            x="Time",
            y=left_axis_columns,
        ).for_each_trace(lambda t: t.update(name=t.name + " (MW)"))

        right_axis_columns = [
            "Intra-Day Market Value",
        ]
        intraday_market_sys_fig_right = (
            px.line(
                df,
                x="Time",
                y=right_axis_columns,
            )
            .update_traces(yaxis="y2")
            .for_each_trace(lambda t: t.update(name=t.name + " (£/MW)"))
        )

        intraday_market_sys_fig.add_traces(
            intraday_market_sys_fig_left.data + intraday_market_sys_fig_right.data
        )

    intraday_market_sys_fig.layout.xaxis.title = "Time"
    intraday_market_sys_fig.layout.xaxis.range = time_range
    intraday_market_sys_fig.update_xaxes(type="date")
    intraday_market_sys_fig.layout.yaxis.title = "MW"
    intraday_market_sys_fig.layout.yaxis2.title = "£/MW"
    intraday_market_sys_fig.layout.yaxis.range = [-100, 100]
    intraday_market_sys_fig.layout.yaxis2.range = [-10000, 10000]
    intraday_market_sys_fig.for_each_trace(
        lambda t: t.update(line=dict(color=t.marker.color))
    )

    return intraday_market_sys_fig


@figure("Balancing Market")
def generate_balancing_market_fig(df: pd.DataFrame) -> go.Figure:
    """Creates Plotly figure for Balancing Market graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly graph_objects figure
    """
    balancing_market_fig = make_subplots(specs=[[{"secondary_y": True}]])

    if not len(df.columns) == 1:
        left_axis_columns = [
            "Balancing Mechanism Generation",
            "Balancing Mechanism Storage",
            "Balancing Mechanism Demand",
        ]
        balancing_market_fig_left = px.line(
            df,
            x="Time",
            y=left_axis_columns,
        ).for_each_trace(lambda t: t.update(name=t.name + " (MW)"))

        right_axis_columns = [
            "Balancing Mechanism Value",
        ]
        balancing_market_fig_right = (
            px.line(
                df,
                x="Time",
                y=right_axis_columns,
            )
            .update_traces(yaxis="y2")
            .for_each_trace(lambda t: t.update(name=t.name + " (£/MW)"))
        )

        balancing_market_fig.add_traces(
            balancing_market_fig_left.data + balancing_market_fig_right.data
        )

    balancing_market_fig.layout.xaxis.title = "Time"
    balancing_market_fig.layout.xaxis.range = time_range
    balancing_market_fig.update_xaxes(type="date")
    balancing_market_fig.layout.yaxis.title = "MW"
    balancing_market_fig.layout.yaxis2.title = "£/MW"
    balancing_market_fig.layout.yaxis.range = [-250, 250]
    balancing_market_fig.layout.yaxis2.range = [-50000, 50000]
    balancing_market_fig.for_each_trace(
        lambda t: t.update(line=dict(color=t.marker.color))
    )

    return balancing_market_fig


@figure("Energy Deficit")
@axes(ylabel="MW", yrange=[-600, 600])
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
                    header=dict(values=columns, align="left"),
                    cells=dict(values=data, align="left"),
                )
            ]
        )

    return intraday_market_bids_fig


@figure("Demand Side Response")
def generate_dsr_fig(df: pd.DataFrame) -> go.Figure:
    """Creates plotly figure for Demand Side Response graph.

    Args:
        df: DSR data DataFrame. TODO: Will this be DSR, Opal or both?

    Returns:
        Plotly graph objects figure
    """
    dsr_fig = make_subplots(specs=[[{"secondary_y": True}]])

    if not len(df.columns) == 1:
        left_axis_columns = [
            "Cost",  # TODO: This will need to be changed when data is available
            "Cost",  # TODO: As above
        ]
        dsr_fig_left = px.line(
            df,
            x="Time",
            y=left_axis_columns,
        ).for_each_trace(lambda t: t.update(name=t.name + " (kW)"))

        right_axis_columns = [
            "Cost",
        ]
        dsr_fig_right = (
            px.line(
                df,
                x="Time",
                y=right_axis_columns,
            )
            .update_traces(yaxis="y2")
            .for_each_trace(lambda t: t.update(name=t.name + " (£/MW)"))
        )

        dsr_fig.add_traces(dsr_fig_left.data + dsr_fig_right.data)

    dsr_fig.layout.xaxis.title = "Time"
    dsr_fig.layout.xaxis.range = time_range
    dsr_fig.update_xaxes(type="date")
    dsr_fig.layout.yaxis.title = "kW"
    dsr_fig.layout.yaxis2.title = "£/MW"
    dsr_fig.layout.yaxis.range = [-1, 1]  # TODO: Check range
    dsr_fig.layout.yaxis2.range = [-1, 1]
    dsr_fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
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
        font=dict(size=12, color="black"),
    )

    waffle.update_layout(yaxis=dict(scaleanchor="x"), plot_bgcolor="rgba(0,0,0,0)")
    waffle.update_xaxes(visible=False)
    waffle.update_yaxes(visible=False, autorange="reversed")

    return waffle


@figure("Agent Activity Breakdown")
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
                    header=dict(values=columns, align="center"),
                    cells=dict(
                        values=data, align="center", height=50, font=dict(size=30)
                    ),
                )
            ]
        )

    return weather_fig


@figure("Reserve/Standby Generation")
@axes(ylabel="MW", yrange=[25000, 35000])
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
