"""Interacts with the OVE Core API."""
import json
import logging
import os
import time

import requests

"""
Constants for API URLs.
"""
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8080")
PLOT_URL = os.environ.get("PLOT_URL", "http://127.0.0.1:8050")

"""
Initial config for sections.
"""
INIT_SECTIONS = {
    "Control": {
        "x": 0,
        "y": 0,
        "w": 1440,
        "h": 808,
        "space": "Tablet",
        "app": {
            "url": f"{API_URL}/app/html",
            "states": {"load": {"url": f"{PLOT_URL}"}},
        },
    },
    "NMX": {
        "x": 0,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC01-Top",
        "app": {"url": f"{API_URL}/app/webrtc", "states": {"load": "ScreenShare"}},
    },
    "Balance of Supply and Demand": {
        "x": 0,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC01-Left",
        "app": {
            "url": f"{API_URL}/app/html",
            "states": {"load": {"url": f"{PLOT_URL}/supplydemand"}},
        },
    },
    "Market IN PROGRESS": {
        "x": 0,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC01-Left",
        "app": {
            "url": f"{API_URL}/app/html",
            "states": {"load": {"url": f"{PLOT_URL}/market"}},
        },
    },
    "Markets and Reserve": {
        "x": 0,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC01-Right",
        "app": {
            "url": f"{API_URL}/app/html",
            "states": {"load": {"url": f"{PLOT_URL}/plot3"}},
        },
    },
    "NMX Georgraphic Map": {
        "x": 0,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC02-Top",
        "app": {"url": f"{API_URL}/app/webrtc", "states": {"load": "ScreenShare"}},
    },
    "NMX 11kV Schematic": {
        "x": 0,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC02-Left",
        "app": {"url": f"{API_URL}/app/webrtc", "states": {"load": "ScreenShare"}},
    },
    "NMX Issues": {
        "x": 0,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC02-Right",
        "app": {"url": f"{API_URL}/app/webrtc", "states": {"load": "ScreenShare"}},
    },
    "Market": {
        "x": 0,
        "y": 0,
        "w": 3840,
        "h": 2160,
        "space": "Hub01",
        "app": {
            "url": f"{API_URL}/app/html",
            "states": {"load": {"url": f"{PLOT_URL}/plot7"}},
        },
    },
    "Agent": {
        "x": 0,
        "y": 0,
        "w": 3840,
        "h": 2160,
        "space": "Hub02",
        "app": {
            "url": f"{API_URL}/app/html",
            "states": {"load": {"url": f"{PLOT_URL}/plot8"}},
        },
    },
}


def wait_for_ove() -> None:
    """Function to wait for the OVE Core API to be available after startup."""
    while requests.get(f"{API_URL}/app/html").status_code != 200:
        time.sleep(5)


def create_all() -> None:
    """Function for creating all initial sections."""
    wait_for_ove()
    for section in INIT_SECTIONS.values():
        response = requests.post(f"{API_URL}/section", json=section)
        logging.info(response.text)


def move_section(id_num: int, space: str) -> None:
    """Function to move a section by ID to a specified space.

    Args:
        id_num (int): ID for section to move.
        space (str): Name of destination space.
    """
    url = f"{API_URL}/sections/{id_num}?includeAppStates=true"
    response = requests.get(url)
    data = json.loads(response.text)

    new_data = {}

    new_data["space"] = space
    new_data["x"] = data["x"]
    new_data["y"] = data["y"]
    new_data["w"] = data["w"]
    new_data["h"] = data["h"]
    new_data["app"] = data["app"]

    url = f"{API_URL}/sections/{id_num}"
    response = requests.post(url, json=new_data)
    print(response.text)


def swap_sections(id_a: int, id_b: int) -> None:
    """Function to swap the spaces of two sections by ID.

    Args:
        id_a (int): ID for the first of two sections to swap.
        id_b (int): ID for the second of two sections to swap.
    """
    url = f"{API_URL}/sections/{id_a}"
    response = requests.get(url)
    data_a = json.loads(response.text)

    url = f"{API_URL}/sections/{id_b}"
    response = requests.get(url)
    data_b = json.loads(response.text)

    move_section(id_a, data_b["space"])
    move_section(id_b, data_a["space"])


def delete_all() -> None:
    """Function for deleting all sections."""
    response = requests.get(f"{API_URL}/sections")
    data = json.loads(response.text)
    id_nums = []

    for section in data:
        id_nums.append(section["id"])

    for num in id_nums:
        url = f"{API_URL}/sections/{num}"
        requests.delete(url)


if __name__ == "__main__":
    create_all()
