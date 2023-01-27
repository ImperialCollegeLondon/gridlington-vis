import pip._vendor.requests
import ast


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


# Function for sending request to create section one in specified space arg
def create_section_one(space):
    section_one["space"] = space
    response = pip._vendor.requests.post("http://localhost:8080/section", json=section_one)
    print(response.text)


# Function for sending request to create section two in specified space arg
def create_section_two(space):
    section_two["space"] = space
    response = pip._vendor.requests.post("http://localhost:8080/section", json=section_two)
    print(response.text)


# Function for deleting all sections
def delete_all():
    response = pip._vendor.requests.get("http://localhost:8080/sections")
    data = ast.literal_eval(response.text)
    id_nums = []

    for section in data:
        id_nums.append(section["id"])
    
    for num in id_nums:
        url = f"http://localhost:8080/sections/{num}"
        pip._vendor.requests.delete(url)


create_section_one("SpaceOne")
create_section_two("SpaceOne")