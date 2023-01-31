import pip._vendor.requests
import ast


APP_URL = "http://146.179.34.13:8080/app/html"
API_URL = "http://liionsden.rcs.ic.ac.uk:8080"
PLOT_URL = "http://liionsden.rcs.ic.ac.uk:8050"


# Initial config for sections
INIT_SECTIONS = [
    {
        "x":500,
        "y":0,
        "w":1920,
        "h":1080,
        "space":"PC01-Top",
        "app":{
            "url":APP_URL,
            "states": {
                "load": {
                    "url": f"{PLOT_URL}/plot1"
                }
            }
        }
    },
    {
        "x":0,
        "y":0,
        "w":1920,
        "h":1080,
        "space":"PC01-Left",
        "app":{
            "url":APP_URL,
            "states": {
                "load": {
                    "url": f"{PLOT_URL}/plot2"
                }
            }
        }
    },
    {
        "x":0,
        "y":0,
        "w":1920,
        "h":1080,
        "space":"PC01-Right",
        "app":{
            "url":APP_URL,
            "states": {
                "load": {
                    "url": f"{PLOT_URL}/plot3"
                }
            }
        }
    },
    {
        "x":0,
        "y":0,
        "w":1920,
        "h":1080,
        "space":"PC02-Top",
        "app":{
            "url":APP_URL,
            "states": {
                "load": {
                    "url": f"{PLOT_URL}/plot4"
                }
            }
        }
    },
    {
        "x":0,
        "y":0,
        "w":1920,
        "h":1080,
        "space":"PC02-Left",
        "app":{
            "url":APP_URL,
            "states": {
                "load": {
                    "url": f"{PLOT_URL}/plot5"
                }
            }
        }
    },
    {
        "x":0,
        "y":0,
        "w":1920,
        "h":1080,
        "space":"PC02-Right",
        "app":{
            "url":APP_URL,
            "states": {
                "load": {
                    "url": f"{PLOT_URL}/plot6"
                }
            }
        }
    },
    {
        "x":0,
        "y":0,
        "w":3840,
        "h":2160,
        "space":"Hub01",
        "app":{
            "url":APP_URL,
            "states": {
                "load": {
                    "url": f"{PLOT_URL}/plot7"
                }
            }
        }
    },
    {
        "x":0,
        "y":0,
        "w":3840,
        "h":2160,
        "space":"Hub02",
        "app":{
            "url":APP_URL,
            "states": {
                "load": {
                    "url": f"{PLOT_URL}/plot8"
                }
            }
        }
    }
]

section_one = {
    "space": "PC01-Top",
    "x": 0,
    "y": 0,
    "w": 1000,
    "h": 800,
    "app": {
        "url": APP_URL,
        "states": {"load": {"url": f"{PLOT_URL}/plot1"}},
    },
}

section_two = {
    "space": "PC02-Top",
    "x": 30,
    "y": 1,
    "w": 1200,
    "h": 808,
    "app": {
        "url": APP_URL,
        "states": {"load": {"url": f"{PLOT_URL}/plot2"}},
    },
}

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


# Function for creating all initial sections
def create_all():
    for section in INIT_SECTIONS:
        response = pip._vendor.requests.post("http://146.179.34.13:8080/section", json=section)
        print(response.text)


# Function for sending request to create section one in specified space arg
def create_section_one(space):
    section_one["space"] = space
    response = pip._vendor.requests.post(f"{API_URL}/section", json=section_one)
    print(response.text)


# Function for sending request to create section two in specified space arg
def create_section_two(space):
    section_two["space"] = space
    response = pip._vendor.requests.post(f"{API_URL}/section", json=section_two)
    print(response.text)


# Function to move a section by id to a specified space
def move_section(id_num, space):
    url = f"{API_URL}/sections/{id_num}?includeAppStates=true"
    response = pip._vendor.requests.get(url)
    #print(response.text)
    data = ast.literal_eval(response.text)

    template["space"] = space
    template["x"] = data["x"]
    template["y"] = data["y"]
    template["w"] = data["w"]
    template["h"] = data["h"]
    template["app"] = data["app"]

    url = f"{API_URL}/sections/{id_num}"
    response = pip._vendor.requests.post(url, json=template)
    print(response.text)


# Function to swap the spaces of two sections by id
def swap_sections(id_a, id_b):
    url = f"{API_URL}/sections/{id_a}?includeAppStates=true"
    response = pip._vendor.requests.get(url)
    data_a = ast.literal_eval(response.text)

    url = f"{API_URL}/sections/{id_b}?includeAppStates=true"
    response = pip._vendor.requests.get(url)
    data_b = ast.literal_eval(response.text)

    template["space"] = data_b["space"]
    template["y"] = data_a["y"]
    template["w"] = data_a["w"]
    template["h"] = data_a["h"]
    template["x"] = data_a["x"]
    template["app"] = data_a["app"]

    url = f"{API_URL}/sections/{id_a}"
    response = pip._vendor.requests.post(url, json=template)
    print(response.text)

    template["space"] = data_a["space"]
    template["y"] = data_b["y"]
    template["w"] = data_b["w"]
    template["h"] = data_b["h"]
    template["x"] = data_b["x"]
    template["app"] = data_b["app"]

    url = f"{API_URL}/sections/{id_b}"
    response = pip._vendor.requests.post(url, json=template)
    print(response.text)


# Function for deleting all sections
def delete_all():
    response = pip._vendor.requests.get(f"{API_URL}/sections")
    data = ast.literal_eval(response.text)
    id_nums = []

    for section in data:
        id_nums.append(section["id"])
    
    for num in id_nums:
        url = f"{API_URL}/sections/{num}"
        pip._vendor.requests.delete(url)


delete_all()
create_all()