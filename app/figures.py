"""Functions for generating plotly figures."""
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
        x="Time",  # TODO: Check units
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
    intraday_market_sys_fig.layout.xaxis.range = [0, 421.14]
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
    balancing_market_fig.layout.xaxis.title = "Time"  # TODO: Check units
    balancing_market_fig.layout.yaxis.title = "MW"
    balancing_market_fig.layout.yaxis2.title = "£/MW"
    balancing_market_fig.layout.xaxis.range = [0, 421.14]
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
            range_x=[0, 421.14],
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
    dsr_fig.layout.xaxis.range = [0, 421.14]
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
            range_x=[0, 421.14],
        ).update_layout(yaxis_title="MW", legend_title=None)

    return dsr_commands_fig


# def generate_agent_location_fig(
#     df: pd.DataFrame, x_max: int = 1, y_max: int = 1
# ) -> px.scatter:
#     """Creates plotly scatterplot for agent locations figure.

#     Args:
#         df: TODO
#         x_max: Maximum x coordinate
#         y_max: Maximum y coordinate

#     Returns:
#         Plotly express scatterplot
#     """
#     if len(df.columns) == 1:
#         agent_location_fig = px.scatter()
#     else:
#         x_coordinates = np.random.uniform(
#             0, x_max, 1000
#         )  # TODO: replace with actual data
#         y_coordinates = np.random.uniform(
#             0, y_max, 1000
#         )  # TODO: replace with actual data

#         agent_location_fig = px.scatter(
#             x=x_coordinates,
#             y=y_coordinates,
#             range_x=[0, x_max],
#             range_y=[0, y_max],
#         )
#     agent_location_fig.update_xaxes(visible=False)
#     agent_location_fig.update_yaxes(visible=False)
#     agent_location_fig.update_layout(
#         {
#             "plot_bgcolor": "rgba(0, 0, 0, 0)",
#             "paper_bgcolor": "rgba(0, 0, 0, 0)",
#             "margin": dict(l=0, r=0, t=0, b=0),
#         }
#     )

#     return agent_location_fig


def generate_agent_activity_breakdown_fig(df: pd.DataFrame) -> px.pie:
    """Creates plotly pie chart for Agent activity breakdown figure.

    TODO: this is just an easy first draft. A waffle plot may be better

    Args:
        df: Opal dataframe

    Returns:
        Plotly express pie chart
    """
    if len(df.columns) == 1:
        agent_activity_breakdown_fig = px.pie()
    else:
        household_activities = [
            c for c in df.columns.values.tolist() if "Household Activity" in c
        ]
        agent_activity_breakdown_fig = px.pie(
            names=[h.split("(")[1].split(")")[0] for h in household_activities],
            values=[df[h].iloc[-1] for h in household_activities],
        ).update_layout(legend_title_text="Household Activity")
        # TODO: check I'm plotting the right thing here

    return agent_activity_breakdown_fig


def generate_ev_charging_breakdown_fig(df: pd.DataFrame) -> px.pie:
    """TODO.

    Args:
        df: TODO

    Returns:
        TODO
    """
    # TODO: populate function
    return px.pie()
