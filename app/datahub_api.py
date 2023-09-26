"""Interacts with the DataHub API."""

import requests

"""
Constant for API URLs.
"""
DH_URL = "http://127.0.0.1:8000"


def get_opal_data(start: int = None, end: int = None) -> dict[str, dict]:  # type: ignore[type-arg]
    """Function for making a GET request for Opal data.

    Args:
        start: Starting index for data filtering
        end: Ending index for data filtering

    Returns:
        A dictionary of the Opal Data received from the Datahub API.
    """
    query = ""
    if start or end:
        query = query + "?"
        if start:
            query = query + f"start={start}&"
        if end:
            query = query + f"end={end}&"
    
    req = requests.get(f"{DH_URL}/opal{query.rstrip('&')}")

    if "data" in req.json().keys():
        data = req.json()["data"]
        return data
    else:
        raise Exception("Opal data was not found")


def get_dsr_data(start: int = None, end: int = None, col: list[str] = None) -> dict[str, dict]:  # type: ignore[type-arg]
    """Function for making a GET request for Opal data.

    Args:
        start: Starting index for data filtering
        end: Ending index for data filtering
        col: List of column names to filter by

    Returns:
        A dictionary of the DSR Data received from the Datahub API.
    """
    query = ""
    if start or end or col:
        query = query + "?"
        if start:
            query = query + f"start={start}&"
        if end:
            query = query + f"end={end}&"
        if col:
            cols = ",".join(col).lower()
            query = query + f"col={cols}&"

    req = requests.get(f"{DH_URL}/dsr{query.rstrip('&')}")

    if "data" in req.json().keys():
        data = req.json()["data"]
        return data
    else:
        raise Exception("DSR data was not found")


def get_wesim_data() -> dict[str, dict]:  # type: ignore[type-arg]
    """Function for making a GET request for Wesim data."""

    req = requests.get(f"{DH_URL}/wesim")
    if "data" in req.json().keys():
        data = req.json()["data"]
        return data
    else:
        raise Exception("Wesim data was not found")
