"""Interacts with the DataHub API."""
import os

import requests

from . import log

"""
Constant for API URLs.
"""
DH_URL = os.environ.get("DH_URL", "http://127.0.0.1:80")


class DataHubConnectionError(requests.exceptions.ConnectionError):
    """Exception for when a connection with the DataHub cannot be established."""


class DataHubRequestError(requests.exceptions.HTTPError):
    """Exception for when a request to the DataHub does not return the desired data."""


def request_datahub(
    data_source: str,
    payload: dict[str, int | str | None] = {},
) -> requests.Response:
    """Send a GET request to the DataHub.

    Args:
        data_source (str): The endpoint for the request. Either "opal", "dsr" or "wesim"
        payload (dict, optional): Dictionary mapping query parameters to values.

    Raises:
        DataHubConnectionError: Raised when there is a connection error in the request.
        DataHubRequestError: Raised when there is a bad request

    Returns:
        requests.Response: The request response, with the requested data.
    """
    try:
        log.info(f"Requesting {data_source.upper()} data from the DataHub")
        req = requests.get(f"{DH_URL}/{data_source}", params=payload)
    except requests.exceptions.ConnectionError as err:
        raise DataHubConnectionError(err)

    try:
        req.raise_for_status()
    except requests.exceptions.HTTPError as err:
        log.error(req.json()["detail"])
        raise DataHubRequestError(err)

    return req


def get_opal_data(
    start: int | None = None, end: int | None = None
) -> dict[str, list]:  # type: ignore[type-arg]
    """Function for making a GET request for Opal data.

    Args:
        start: Starting index for data filtering
        end: Ending index for data filtering

    Returns:
        A dictionary of the Opal Data received from the Datahub API.
    """
    req = request_datahub("opal", dict(start=start, end=end))

    return req.json()["data"]


def get_dsr_data(
    start: int | None = None, end: int | None = None, col: list[str] | None = None
) -> dict[str, dict]:  # type: ignore[type-arg]
    """Function for making a GET request for Opal data.

    Args:
        start: Starting index for data filtering
        end: Ending index for data filtering
        col: List of column names to filter by

    Returns:
        A dictionary of the DSR Data received from the Datahub API.
    """
    if col:
        col_string = ",".join(col).lower()

    req = request_datahub("dsr", dict(start=start, end=end, col=col_string))

    return req.json()["data"]


def get_wesim_data() -> dict[str, dict]:  # type: ignore[type-arg]
    """Function for making a GET request for Wesim data."""
    req = request_datahub("wesim")

    return req.json()["data"]


def start_model() -> str:
    """Function for starting the model.

    Returns:
        str: Message to display on the control app
    """
    try:
        # Get signal to see if model is already running
        start_signal = request_datahub("start").json()
        if start_signal:
            return "Model is already running"

        # If not running, send signal to start
        requests.post(f"{DH_URL}/set_model_signals", json={"start": True})

        # Get signal to see if model has started properly
        start_signal = request_datahub("start").json()
        return (
            "Model started successfully"
            if start_signal
            else "Failed to start the model"
        )

    except (DataHubConnectionError, DataHubRequestError):
        return "Failed to connect to the DataHub"


def stop_model() -> str:
    """Function for stopping the model.

    Returns:
        str: Message to display on the control app
    """
    try:
        # Get signal to see if model is already stopped
        stop_signal = request_datahub("stop").json()
        if stop_signal:
            return "Model is not running"

        # If running, send signal to stop
        requests.post(f"{DH_URL}/set_model_signals", json={"start": False})

        # Get signal to see if model has stopped properly
        stop_signal = request_datahub("stop").json()
        return (
            "Model stopped successfully"
            if not stop_signal
            else "Failed to stop the model"
        )
    except (DataHubConnectionError, DataHubRequestError):
        return "Failed to connect to the DataHub"
