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


def html(page: str) -> dict[str, str | dict[str, str | dict[str, str]]]:
    """App specification for a html app.

    Args:
        page: The name of the dash page to link to the OVE section.

    Returns:
        dict: JSON for app specification in OVE section API call.
    """
    return {
        "url": f"{API_URL}/app/html",
        "states": {"load": {"url": f"{PLOT_URL}/{page}"}},
    }


webrtc = {"url": f"{API_URL}/app/webrtc", "states": {"load": "ScreenShare"}}

"""Initial config for sections."""
INIT_SECTIONS = {
    "Control": {"space": "Tablet", "app": html("control")},
    "NMX": {"space": "PC01-Top", "app": webrtc},
    "Balance of Supply and Demand": {"space": "PC01-Left", "app": html("supplydemand")},
    "Markets and Reserve": {"space": "PC01-Right", "app": html("plot3")},
    "NMX Georgraphic Map": {"space": "PC02-Top", "app": webrtc},
    "NMX 11kV Schematic": {"space": "PC02-Left", "app": webrtc},
    "NMX Issues": {"space": "PC02-Right", "app": webrtc},
    "Market": {"space": "Hub01", "app": html("market")},
    "Agent": {"space": "Hub02", "app": html("agent")},
}


def wait_for_ove() -> None:
    """Function to wait for the OVE Core API to be available after startup."""
    while requests.get(f"{API_URL}/app/html").status_code != 200:
        time.sleep(5)


def create_all() -> None:
    """Function for creating all initial sections."""
    wait_for_ove()
    spaces = json.loads(requests.get(f"{API_URL}/spaces").text)
    for section in INIT_SECTIONS.values():
        data = spaces[section["space"]][0] | section
        response = requests.post(f"{API_URL}/section", json=data)
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