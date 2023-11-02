"""Functions for generating plotly express figures."""
import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
from plotly.subplots import make_subplots  # type: ignore


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
        ).update_layout(yaxis_title="GW")
    return system_freq_fig


def generate_intraday_market_sys_fig(df: pd.DataFrame) -> go:
    """Creates Plotly figure for Intra-day Market System graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly graph_objects figure
    """
    intraday_market_sys_fig = make_subplots(specs=[[{"secondary_y": True}]])

    if len(df.columns) == 1:
        return intraday_market_sys_fig

    intraday_market_sys_fig_left = px.line(
        df,
        x="Time",
        y=[
            "Intra-Day Market Generation",
            "Intra-Day Market Storage",
            "Intra-Day Market Demand",
        ],
    ).update_layout(yaxis_title="Power")

    intraday_market_sys_fig_right = (
        px.line(
            df,
            x="Time",
            y=[
                "Intra-Day Market Value",
            ],
        )
        .update_layout(yaxis_title="Cost")
        .update_traces(yaxis="y2")
    )

    intraday_market_sys_fig.add_traces(
        intraday_market_sys_fig_left.data + intraday_market_sys_fig_right.data
    )

    return intraday_market_sys_fig


def generate_balancing_market_fig(df: pd.DataFrame) -> go:
    """Creates Plotly figure for Balancing Market graph.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly graph_objects figure
    """
    balancing_market_fig = make_subplots(specs=[[{"secondary_y": True}]])

    if len(df.columns) == 1:
        return balancing_market_fig

    balancing_market_fig_left = px.line(
        df,
        x="Time",
        y=[
            "Balancing Mechanism Generation",
            "Balancing Mechanism Storage",
            "Balancing Mechanism Demand",
        ],
    ).update_layout(yaxis_title="Power")

    balancing_market_fig_right = (
        px.line(
            df,
            x="Time",
            y=[
                "Balancing Mechanism Value",
            ],
        )
        .update_layout(yaxis_title="Cost")
        .update_traces(yaxis="y2")
    )

    balancing_market_fig.add_traces(
        balancing_market_fig_left.data + balancing_market_fig_right.data
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
        ).update_layout(yaxis_title="GW")

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
        intraday_market_bids_fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["Total Generation", "Total Demand"], align="left"
                    ),
                    cells=dict(
                        values=[df["Total Generation"], df["Total Demand"]],
                        align="left",
                    ),
                )
            ]
        )

    return intraday_market_bids_fig


def generate_dsr_bids_fig(df: pd.DataFrame) -> go.Figure:
    """Creates plotly Figure object for DSR Bids and Offers table.

    Args:
        df: Opal data DataFrame

    Returns:
        Plotly graph_objects figure
    """
    if len(df.columns) == 1:
        dsr_bids_fig = go.Figure()

    else:
        dsr_bids_fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=["Total Generation", "Total Demand"], align="left"
                    ),
                    cells=dict(
                        values=[df["Total Generation"], df["Total Demand"]],
                        align="left",
                    ),
                )
            ]
        )

    return dsr_bids_fig


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
        dsr_commands_fig = px.line(
            df,
            x="Time",
            y=[
                df["Real Gridlington Demand"]
                - df["Expected Gridlington Demand"]
                + (df["Real Ev Charging Power"] - df["Expected Ev Charging Power"]),
                df["Real Ev Charging Power"] - df["Expected Ev Charging Power"],
            ],
        ).update_layout(yaxis_title="XXXXXXX")

    return dsr_commands_fig
