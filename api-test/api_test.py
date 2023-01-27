import pip._vendor.requests

# Initial config for sections
section_one = {
    "space": "SpaceOne",
    "x": 0,
    "y": 0,
    "w": 1000,
    "h": 800,
    "app": {
        "url": "http://192.168.1.203:8080/app/html",
        "states": {"load": {"url": "http://localhost:8050/plot1"}},
    },
}

section_two = {
    "space": "SpaceOne",
    "x": 30,
    "y": 1,
    "w": 1200,
    "h": 808,
    "app": {
        "url": "http://192.168.1.203:8080/app/html",
        "states": {"load": {"url": "http://localhost:8050/plot1"}},
    },
}

# Function for sending request to create section one
def create_section_one():
    pip._vendor.requests.post("http://localhost:8080/section", json=section_one)

# Function for sending request to create section two
def create_section_two():
    pip._vendor.requests.post("http://localhost:8080/section", json=section_two)


create_section_one()
create_section_two()