"""Calls the Datahub to update data."""
import pandas as pd
from dash import Input, Output, callback, dcc, html  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore

from . import LIVE_MODEL, log
from .datahub_api import get_opal_data  # , get_dsr_data

##################
interval = 7000
##################

df_opal = pd.DataFrame({"Col": [0]})

data_div = html.Div(
    children=[
        dcc.Interval(id="interval", interval=interval),
        dcc.Store(id="data_opal", data=df_opal.to_dict(orient="records")),
    ]
)


@callback(
    [Output("data_opal", "data")],
    [Input("interval", "n_intervals")],
)
def update_data(n_intervals: int) -> tuple[list[dict[str, object]],]:
    """Function to update the data.

    Args:
        n_intervals (int): The number of times this page has updated.
            indexes by 1 every 7 seconds.

    Returns:
        Opal data dictionary

    """
    if n_intervals is None:
        raise PreventUpdate

    if LIVE_MODEL:
        log.debug("Updating plots from live model")
        data_opal = get_opal_data()
        new_df_opal = pd.DataFrame(**data_opal)  # type: ignore[call-overload]
    else:
        from .pre_set_data import OPAL_DATA

        log.debug("Updating plots with pre-set data")
        new_df_opal = OPAL_DATA.loc[:n_intervals]
    return (new_df_opal.to_dict(orient="records"),)
