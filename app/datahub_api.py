"""Interacts with the DataHub API."""

import requests

"""
Constant for API URLs.
"""
DH_URL = "http://127.0.0.1:8000"


def get_opal_data() -> dict[str, dict]:  # type: ignore[type-arg]
    """Function for making a GET request for Opal data."""
    req = requests.get(f"{DH_URL}/opal")
    data = req.json()["data"]
    return data


def get_drs_data() -> dict[str, dict]:  # type: ignore[type-arg]
    """Function for making a GET request for Opal data."""
    req = requests.get(f"{DH_URL}/dsr")
    data = req.json()["data"]
    return data


def get_wesim_data() -> dict[str, dict]:  # type: ignore[type-arg]
    """Function for making a GET request for Wesim data."""
    req = requests.get(f"{DH_URL}/wesim")
    data = req.json()["data"]
    return data
