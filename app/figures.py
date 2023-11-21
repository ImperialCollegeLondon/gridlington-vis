"""Functions for generating plotly figures."""
import numpy as np
import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
from plotly.colors import DEFAULT_PLOTLY_COLORS  # type: ignore
from plotly.subplots import make_subplots  # type: ignore

time_range = ["2035-01-22 00:00:00", "2035-01-22 00:07:01.140"]


def generate_gen_split_fig(df: pd.DataFrame) -> px.pie:
    """Creates Plotly figure for Generation Split graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly express figure
    """
    if len(df.columns) == 1:
        gen_split_fig = px.pie()
    else:
        gen_split_df = df.iloc[-1, 13:23]

        gen_split_fig = px.pie(
            names=[
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
            ],
            values=gen_split_df,
        ).update_layout(title_text=df.iloc[-1]["Time"])
    return gen_split_fig


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
            y=[
                "Total Generation",
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
            ],
            range_x=time_range,
            range_y=[-5, 70],
        ).update_layout(yaxis_title="GW")
    return total_gen_fig


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
            range_x=time_range,
            range_y=[-5, 70],
        ).update_layout(yaxis_title="GW")
    return total_dem_fig


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
            range_x=time_range,
            range_y=[-5, 70],
        ).update_layout(yaxis_title="GW")
    return system_freq_fig


def generate_intraday_market_sys_fig(df: pd.DataFrame) -> go.Figure:
    """Creates Plotly figure for Intra-day Market System graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly graph_objects figure
    """
    intraday_market_sys_fig = make_subplots(specs=[[{"secondary_y": True}]])

    if len(df.columns) == 1:
        return intraday_market_sys_fig

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
    intraday_market_sys_fig.layout.yaxis.title = "MW"
    intraday_market_sys_fig.layout.yaxis2.title = "£/MW"
    intraday_market_sys_fig.layout.xaxis.range = time_range
    intraday_market_sys_fig.layout.yaxis.range = [-100, 100]
    intraday_market_sys_fig.layout.yaxis2.range = [-10000, 10000]
    intraday_market_sys_fig.for_each_trace(
        lambda t: t.update(line=dict(color=t.marker.color))
    )

    return intraday_market_sys_fig


def generate_balancing_market_fig(df: pd.DataFrame) -> go.Figure:
    """Creates Plotly figure for Balancing Market graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly graph_objects figure
    """
    balancing_market_fig = make_subplots(specs=[[{"secondary_y": True}]])

    if len(df.columns) == 1:
        return balancing_market_fig

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
    balancing_market_fig.layout.yaxis.title = "MW"
    balancing_market_fig.layout.yaxis2.title = "£/MW"
    balancing_market_fig.layout.xaxis.range = time_range
    balancing_market_fig.layout.yaxis.range = [-250, 250]
    balancing_market_fig.layout.yaxis2.range = [-50000, 50000]
    balancing_market_fig.for_each_trace(
        lambda t: t.update(line=dict(color=t.marker.color))
    )

    return balancing_market_fig


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
            range_y=[-600, 600],
            range_x=time_range,
        ).update_layout(yaxis_title="MW")

    return energy_deficit_fig


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


def generate_dsr_fig(df: pd.DataFrame) -> go.Figure:
    """Creates plotly figure for Demand Side Response graph.

    Args:
        df: DSR data DataFrame. TODO: Will this be DSR, Opal or both?

    Returns:
        Plotly express figure
    """
    dsr_fig = make_subplots(specs=[[{"secondary_y": True}]])

    if len(df.columns) == 1:
        return dsr_fig

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
    dsr_fig.layout.xaxis.title = "Time"  # TODO: Check units
    dsr_fig.layout.yaxis.title = "kW"
    dsr_fig.layout.yaxis2.title = "£/MW"
    dsr_fig.layout.xaxis.range = time_range
    dsr_fig.layout.yaxis.range = [-1, 1]  # TODO: Check range
    dsr_fig.layout.yaxis2.range = [-1, 1]
    dsr_fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

    return dsr_fig


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
            range_y=[-8, 8],
            range_x=time_range,
        ).update_layout(yaxis_title="MW", legend_title=None)

    return dsr_commands_fig


def create_waffle_chart(
    names: list[str],
    counts: list[int],
    colors: list[str] | None = None,
    rows: int | None = None,
    gap: float = 3.0,
) -> go.Figure:
    """Create waffle chart.

    Args:
        names (list[str]): List of names
        counts (list[int]): List of counts
        colors (list[str], optional): List of colors. If None, will use plotly
            default color map. Defaults to None.
        rows (int, optional): Number of rows in the chart. Number of columns
            is set automatically. If None, will produce a square chart.
            Defaults to None.
        gap (str, optional): Gap between squares (pixel units). Defaults to 0.0.

    Raises:
        ValueError: Raised if names, counts and colors are not equal length
        TypeError: Raised if counts are not integers

    Returns:
        go.Figure: Waffle chart
    """
    # Set default colors
    if not colors:
        colors = [DEFAULT_PLOTLY_COLORS[i] for i in range(len(names))]

    # Check fields, counts, colors are all same length
    if not len(names) == len(counts) == len(colors):
        raise ValueError(
            "names, counts and colors (if specified) arguments must be "
            "lists of equal length"
        )

    # Check counts is all integers
    if not all(isinstance(item, int) for item in counts):
        raise TypeError("Counts must be integers")

    # Shape
    total = sum(counts)
    if not rows:
        rows = max(int(total**0.5), 1)  # Default to square chart
    columns = int(np.ceil(total / rows))

    # Create numpy array TODO: more pythonic
    z_flat = np.ones([columns * rows])
    v = 0
    position = 0
    for c in counts:
        z_flat[position : position + c] = v / len(names)
        v += 1
        position += c
    z = z_flat.reshape((rows, columns))

    # Create color scale
    colorscale = [[i / len(names), c] for i, c in enumerate(colors)]
    colorscale.append([1, "rgb(255, 255, 255)"])

    # Waffle plot
    waffle = go.Figure(
        go.Heatmap(
            z=z,
            xgap=gap,
            ygap=gap,
            colorscale=colorscale,
            showscale=False,
            zmin=0,
            zmax=1,
        )
    )
    waffle.update_layout(yaxis=dict(scaleanchor="x"), plot_bgcolor="rgba(0,0,0,0)")
    waffle.update_xaxes(visible=False)
    waffle.update_yaxes(visible=False, autorange="reversed")
    return waffle


def generate_agent_activity_breakdown_fig(df: pd.DataFrame) -> go.Figure:
    """Creates waffle chart for agent activity breakdown figure.

    Args:
        df: Opal dataframe TODO: Should we be using DSR instead?

    Returns:
        Waffle chart
    """
    if len(df.columns) == 1:
        agent_activity_breakdown_fig = px.pie()
    else:
        household_activities = [
            c for c in df.columns.values.tolist() if "Household Activity" in c
        ]
        names = [h.split("(")[1].split(")")[0] for h in household_activities]
        counts = [int(df[h].iloc[-1]) for h in household_activities]
        agent_activity_breakdown_fig = create_waffle_chart(names=names, counts=counts)
        agent_activity_breakdown_fig.update_layout(title_text=df.iloc[-1]["Time"])
    return agent_activity_breakdown_fig


def generate_ev_charging_breakdown_fig(df: pd.DataFrame) -> go.Figure:
    """Creates waffle chart for EV charging breakdown figure.

    Args:
        df: Opal dataframe TODO: Should we be using DSR instead?

    Returns:
        Waffle chart
    """
    if len(df.columns) == 1:
        ev_charging_breakdown_fig = px.pie()
    else:
        ev_states = [c for c in df.columns.values.tolist() if "Ev Status" in c]
        names = [h.split("(")[1].split(")")[0] for h in ev_states]
        counts = [int(df[h].iloc[-1]) for h in ev_states]
        ev_charging_breakdown_fig = create_waffle_chart(names=names, counts=counts)
        ev_charging_breakdown_fig.update_layout(title_text=df.iloc[-1]["Time"])
    return ev_charging_breakdown_fig


def generate_weather_fig(df: pd.DataFrame) -> go.Figure:
    """Creates plotly figure for Weather table.

    TODO: This data isn't available yet. For now I'm just making up data
    Will also need to modify bins and labels

    Args:
        df: Wesim dataframe?

    Returns:
        Plotly figure
    """
    sun_bins = [0, 0.33, 0.67]
    sun_labels = ["☀️", "☀️☀️", "☀️☀️☀️"]
    wind_bins = [0, 0.33, 0.67]
    wind_labels = ["💨", "💨💨", "💨💨💨"]

    if len(df.columns) == 1:
        weather_fig = go.Figure()

    else:
        # Make up data TODO: replace with real data
        columns = ["Time1", "Time2", "Time3", "Time4", "Time5", "Time6"]
        sun_data = np.random.uniform(0, 1, 6)
        sun_data_labels = [sun_labels[i - 1] for i in np.digitize(sun_data, sun_bins)]
        wind_data = np.random.uniform(0, 1, 6)
        wind_data_labels = [
            wind_labels[i - 1] for i in np.digitize(wind_data, wind_bins)
        ]
        data = [[sun_data_labels[i], wind_data_labels[i]] for i in range(len(columns))]

        weather_fig = go.Figure(
            data=[
                go.Table(
                    header=dict(values=columns, align="left"),
                    cells=dict(values=data, align="left"),
                )
            ]
        )

    return weather_fig


def generate_reserve_generation_fig(df: pd.DataFrame) -> go.Figure:
    """Creates Plotly figure for Reserve/Standby Generation graph.

    TODO: This data isn't in Opal yet - need to modify y when available
    Just using dummy data for now
    Will also need to modify y axis range

    Args:
        df: Opal dataframe

    Returns:
        Plotly express line graph
    """
    if len(df.columns) == 1:
        reserve_generation_fig = px.line()
    else:
        reserve_generation_fig = px.line(
            df,
            x="Time",
            y=df["Exp. Offshore Wind Generation"] - df["Real Offshore Wind Generation"],
            range_y=[-600, 600],
            range_x=time_range,
        ).update_layout(
            yaxis_title="MW"
        )  # TODO: check units

    return reserve_generation_fig
