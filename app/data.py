"""Calls the Datahub to update data."""
import pandas as pd
from dash import Input, Output, callback, dcc  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore

from . import LIVE_MODEL, log
from .datahub_api import get_opal_data, get_wesim_data  # , get_dsr_data

##################
interval = 7000
##################

DF_OPAL = pd.DataFrame({"Col": [0]})

WESIM_START_DATE = "2035-01-22 00:00"  # corresponding to hour 0 TODO: check

if LIVE_MODEL:
    WESIM = {key: pd.DataFrame(**item) for key, item in get_wesim_data().items()}
    for df in WESIM.values():
        if "Hour" in df.columns:
            df["Time"] = (
                pd.Timestamp(WESIM_START_DATE) + pd.to_timedelta(df["Hour"], unit="h")
            ).astype(str)
else:
    WESIM = {"df": pd.DataFrame({"Col": [0]})}

data_interval = dcc.Interval(id="data_interval", interval=interval)
empty_output = dcc.Store(id="empty", data=[])


@callback(
    [Output("empty", "data")],
    [Input("data_interval", "n_intervals")],
)
def update_data(n_intervals: int) -> tuple[list[None],]:
    """Function to update the data.

    Args:
        n_intervals (int): The number of times this page has updated.
            indexes by 1 every 7 seconds.

    Returns:
        Opal data dictionary

    """
    global DF_OPAL

    if n_intervals is None:
        raise PreventUpdate

    if LIVE_MODEL:
        log.debug("Updating plots from live model")
        data_opal = get_opal_data()
        DF_OPAL = pd.DataFrame(**data_opal)  # type: ignore[call-overload]
    else:
        from .pre_set_data import OPAL_DATA

        log.debug("Updating plots with pre-set data")
        DF_OPAL = OPAL_DATA.loc[:n_intervals]
    return ([],)
