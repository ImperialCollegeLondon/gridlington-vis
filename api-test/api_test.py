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
        "url": "http://146.179.34.13:8080/app/html",
        "states": {"load": {"url": "http://liionsden.rcs.ic.ac.uk:8050/plot1"}},
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
    response = pip._vendor.requests.post("http://liionsden.rcs.ic.ac.uk:8080/section", json=section_one)
    print(response.text)


# Function for sending request to create section two in specified space arg
def create_section_two(space):
    section_two["space"] = space
    response = pip._vendor.requests.post("http://localhost:8080/section", json=section_two)
    print(response.text)


def move_section(id_num, space):
    template = {
        "space": "SpaceOne",
        "x": 0,
        "y": 0,
        "w": 1440,
        "h": 808,
        "app": {
            "url": "http://146.179.34.13:8080/app/html",
            "states": {"load": {"url": "http://liionsden.rcs.ic.ac.uk:8050/plot1"}},
        },
    }

    url = f"http://146.179.34.13:8080/sections/{id_num}?includeAppStates=true"
    response = pip._vendor.requests.get(url)
    print(response.text)
    data = ast.literal_eval(response.text)

    template["space"] = space
    #template["x"] = data["x"]
    template["y"] = data["y"]
    template["w"] = data["w"]
    template["h"] = data["h"]

    template["app"] = data["app"]

    print(template)
    response = pip._vendor.requests.post(url, json=template)
    print(response.text)


# Function for deleting all sections
def delete_all():
    response = pip._vendor.requests.get("http://146.179.34.13:8080/sections")
    data = ast.literal_eval(response.text)
    id_nums = []

    for section in data:
        id_nums.append(section["id"])
    
    for num in id_nums:
        url = f"http://146.179.34.13:8080/sections/{num}"
        pip._vendor.requests.delete(url)




JSON = [
    {
        "x":500,
        "y":0,
        "w":1920,
        "h":1080,
        "space":"PC01-Top",
        "app":{
            "url":"http://146.179.34.13:8080/app/html",
            "states": {
                "load": {"url": "http://liionsden.rcs.ic.ac.uk:8050/plot1"}
                }}},
    {"x":0,"y":0,"w":1920,"h":1080,"space":"PC01-Left","app":{"url":"http://146.179.34.13:8080/app/html"
    , "states": {"load": {"url": "http://liionsden.rcs.ic.ac.uk:8050/plot2"}}}},
    {"x":0,"y":0,"w":1920,"h":1080,"space":"PC01-Right","app":{"url":"http://146.179.34.13:8080/app/html", "states": {"load": {"url": "http://liionsden.rcs.ic.ac.uk:8050/plot3"}}}},
    {"x":0,"y":0,"w":1920,"h":1080,"space":"PC02-Top","app":{"url":"http://146.179.34.13:8080/app/html", "states": {"load": {"url": "http://liionsden.rcs.ic.ac.uk:8050/plot4"}}}},
    {"x":0,"y":0,"w":1920,"h":1080,"space":"PC02-Left","app":{"url":"http://146.179.34.13:8080/app/html", "states": {"load": {"url": "http://liionsden.rcs.ic.ac.uk:8050/plot5"}}}},
    {"x":0,"y":0,"w":1920,"h":1080,"space":"PC02-Right","app":{"url":"http://146.179.34.13:8080/app/html", "states": {"load": {"url": "http://liionsden.rcs.ic.ac.uk:8050/plot6"}}}},
    {"x":0,"y":0,"w":3840,"h":2160,"space":"Hub02","app":{"url":"http://146.179.34.13:8080/app/html", "states": {"load": {"url": "http://liionsden.rcs.ic.ac.uk:8050/plot8"}}}},
    {"x":0,"y":0,"w":3840,"h":2160,"space":"Hub01","app":{"url":"http://146.179.34.13:8080/app/html", "states": {"load": {"url": "http://liionsden.rcs.ic.ac.uk:8050/plot7"}}}}
]

def create_all():
    for section in JSON:
        response = pip._vendor.requests.post("http://146.179.34.13:8080/section", json=section)
        print(response.text)


#delete_all()
#create_all()
move_section(8,"PC02-Top")

#create_section_one("PC01-Top")