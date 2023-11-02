"""Functions for generating plotly express figures."""
import pandas as pd
import plotly.express as px  # type: ignore


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
