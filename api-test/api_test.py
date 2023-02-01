import requests
import json

"""
Constants for API URLs.
"""
APP_URL = "http://146.179.34.13:8080/app/html"
API_URL = "http://liionsden.rcs.ic.ac.uk:8080"
PLOT_URL = "http://liionsden.rcs.ic.ac.uk:8050"

"""
Initial config for sections.
"""
INIT_SECTIONS = [
    {
        "x": 0,
        "y": 0,
        "w": 1440,
        "h": 808,
        "space": "Tablet",
        "app": {"url": APP_URL, "states": {"load": {"url": f"{PLOT_URL}"}}},
    },
    {
        "x": 500,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC01-Top",
        "app": {"url": APP_URL, "states": {"load": {"url": f"{PLOT_URL}/plot1"}}},
    },
    {
        "x": 0,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC01-Left",
        "app": {"url": APP_URL, "states": {"load": {"url": f"{PLOT_URL}/plot2"}}},
    },
    {
        "x": 0,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC01-Right",
        "app": {"url": APP_URL, "states": {"load": {"url": f"{PLOT_URL}/plot3"}}},
    },
    {
        "x": 0,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC02-Top",
        "app": {"url": APP_URL, "states": {"load": {"url": f"{PLOT_URL}/plot4"}}},
    },
    {
        "x": 0,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC02-Left",
        "app": {"url": APP_URL, "states": {"load": {"url": f"{PLOT_URL}/plot5"}}},
    },
    {
        "x": 0,
        "y": 0,
        "w": 1920,
        "h": 1080,
        "space": "PC02-Right",
        "app": {"url": APP_URL, "states": {"load": {"url": f"{PLOT_URL}/plot6"}}},
    },
    {
        "x": 0,
        "y": 0,
        "w": 3840,
        "h": 2160,
        "space": "Hub01",
        "app": {"url": APP_URL, "states": {"load": {"url": f"{PLOT_URL}/plot7"}}},
    },
    {
        "x": 0,
        "y": 0,
        "w": 3840,
        "h": 2160,
        "space": "Hub02",
        "app": {"url": APP_URL, "states": {"load": {"url": f"{PLOT_URL}/plot8"}}},
    },
]

"""
Template of section config JSON.
"""
template = {
    "space": "SpaceOne",
    "x": 0,
    "y": 0,
    "w": 1440,
    "h": 808,
    "app": {
        "url": APP_URL,
        "states": {"load": {"url": f"{PLOT_URL}/plot1"}},
    },
}


def create_all():
    """
    Function for creating all initial sections.
    """

    for section in INIT_SECTIONS:
        response = requests.post("http://146.179.34.13:8080/section", json=section)
        print(response.text)


def move_section(id_num, space):
    """
    Function to move a section by ID to a specified space.

    Args:
        id_num (int): ID for section to move.
        space (str): Name of destination space.
    """

    url = f"{API_URL}/sections/{id_num}?includeAppStates=true"
    response = requests.get(url)
    data = json.loads(response.text)

    template["space"] = space
    template["x"] = data["x"]
    template["y"] = data["y"]
    template["w"] = data["w"]
    template["h"] = data["h"]
    template["app"] = data["app"]

    url = f"{API_URL}/sections/{id_num}"
    response = requests.post(url, json=template)
    print(response.text)


def swap_sections(id_a, id_b):
    """
    Function to swap the spaces of two sections by ID.

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


def delete_all():
    """
    Function for deleting all sections.
    """
    response = requests.get(f"{API_URL}/sections")
    data = json.loads(response.text)
    id_nums = []

    for section in data:
        id_nums.append(section["id"])

    for num in id_nums:
        url = f"{API_URL}/sections/{num}"
        requests.delete(url)
