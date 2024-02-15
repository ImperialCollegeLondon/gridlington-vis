"""Calls the Datahub to update data."""

import pandas as pd
from dash import Input, Output, callback, dcc  # type: ignore
from dash.exceptions import PreventUpdate  # type: ignore

from . import LIVE_MODEL, PRODUCTION, log
from .datahub_api import get_opal_data, get_wesim_data  # , get_dsr_data

N_INTERVALS_DATA = 0

DF_OPAL = pd.DataFrame({"Col": [0]})

WESIM_START_DATE = "2035-01-22 00:00"  # corresponding to hour 0 TODO: check

if PRODUCTION:
    WESIM = {key: pd.DataFrame(**item) for key, item in get_wesim_data().items()}
    for df in WESIM.values():
        if "Hour" in df.columns:
            df["Time"] = (
                pd.Timestamp(WESIM_START_DATE) + pd.to_timedelta(df["Hour"], unit="h")
            ).astype(str)
else:
    WESIM = {"df": pd.DataFrame({"Col": [0]})}

data_interval = dcc.Interval(id="data_interval")


@callback(
    [Output("data_interval", "disabled")],
    [Input("data_interval", "n_intervals")],
)
def update_data(n_intervals: int) -> tuple[bool,]:
    """Function to update OPAL data.

    Args:
        n_intervals (int): The number of times the data has updated.
            indexes by 1 every interval.

    Returns:
        tuple[bool,]: Boolean that specifies whether the iterator should
            terminate

    """
    global DF_OPAL, N_INTERVALS_DATA

    if n_intervals is None:
        raise PreventUpdate

    data_ended = False
    if LIVE_MODEL:
        log.debug("Updating data from live model")
        data_opal = get_opal_data()
        DF_OPAL = pd.DataFrame(**data_opal)  # type: ignore[call-overload]
    else:
        from .pre_set_data import OPAL_DATA

        log.debug("Updating pre-set data")
        DF_OPAL = OPAL_DATA.loc[:n_intervals]
        if n_intervals == len(OPAL_DATA):
            log.debug("Reached end of pre-set data")
            data_ended = True

    N_INTERVALS_DATA = n_intervals
    return (data_ended,)
