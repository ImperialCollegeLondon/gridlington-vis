"""Contains the logic for processing the pre-set data."""
from glob import glob

import pandas as pd

from . import log
from .datahub_api import DataHubConnectionError, DataHubRequestError, get_opal_data

OPAL_START_DATE = "2035-01-22 00:00"


def read_opal_data() -> pd.DataFrame:
    """Function to get the pre-set opal data.

    Note - this function still calls the datahub - just to get the column names.
    This requires the datahub to be running. For a fully independent solution, the
    data will need to come with the columns pre-defined.

    Returns:
        pd.DataFrame: Opal data with each row being the data at a certain time.
    """
    df = pd.DataFrame()
    for index, file in enumerate(glob("data/opal/*.csv")):
        log.debug(f"Reading file: {file}")
        df[index] = pd.read_csv(file, header=0, index_col=0)
    df = (
        df.transpose()
        .sort_values(by=0)  # type: ignore [call-overload]
        .drop(columns=[0, 5, 6, 7])
        .reset_index(drop=True)
    )
    try:
        df.columns = get_opal_data()["columns"]  # type: ignore [assignment]
    except (DataHubConnectionError, DataHubRequestError):
        log.warning(
            "Issue with DataHub connection or request - using default Opal headers."
        )
        df.columns = pd.read_csv("data/opal_headers.csv").columns

    df["Time"] = (
        pd.Timestamp(OPAL_START_DATE) + pd.to_timedelta(df["Time"], unit="S")
    ).astype(str)

    return df


OPAL_DATA = read_opal_data()

log.debug(OPAL_DATA)
