"""
Run this script to create the docker-compose.yml file using the
docker-compose.setup.ove.yml file and the IP address of the machine
Finds the line in docker-compose.setup.ove.yml that contain the host IP
address and replaces the value with the IP address of the machine in the new
file. Also replaces the openvidu-call version to 2.12.0.

Does the same for config/credentials.json file.
"""

import socket
import yaml
import json

# Get the IP address of the machine on Macos
ip = socket.gethostbyname(socket.gethostname())

# Dictionary of the lines to replace in the docker-compose.yml file
lines_to_replace = {
    "OVE_HOST": f"{ip}:8080",
    "TOURIS_HOST": f"{ip}:7080",
    "OPENVIDU_HOST": f"{ip}:4443",
    "openvidu.publicurl": f"https://{ip}:4443",
}

# Read the docker-compose.setup.ove.yml file
with open("docker-compose.setup.ove.yml", "r") as f:
    docker_compose = yaml.safe_load(f)

# Replace the values in the docker-compose.yml file
docker_compose["services"]["openvidu-openvidu-call"]["environment"][
    "openvidu.publicurl"
] = lines_to_replace["openvidu.publicurl"]
docker_compose["services"]["ovehub-ove-apps"]["environment"][
    "OVE_HOST"
] = lines_to_replace["OVE_HOST"]
docker_compose["services"]["ovehub-ove-apps"]["environment"][
    "TOURIS_HOST"
] = lines_to_replace["TOURIS_HOST"]
docker_compose["services"]["ovehub-ove-apps"]["environment"][
    "OPENVIDU_HOST"
] = lines_to_replace["OPENVIDU_HOST"]
docker_compose["services"]["ovehub-ove-ui"]["environment"][
    "OVE_HOST"
] = lines_to_replace["OVE_HOST"]
# Also replace the openvidu-call version
docker_compose["services"]["openvidu-openvidu-call"][
    "image"
] = "openvidu/openvidu-call:2.12.0"

# Write the new docker-compose.yml file
with open("docker-compose.yml", "w") as f:
    yaml.safe_dump(docker_compose, f)

# Read the config/credentials.json file
with open("credentials_setup.json", "r") as f:
    credentials = json.load(f)

# Replace the IP in the config/credentials.json file
credentials["stores"][0]["proxyUrl"] = f"http://{ip}:6081/default/"

# Write the new config/credentials.json file
with open("config/credentials.json", "w") as f:
    json.dump(credentials, f, indent=2)
