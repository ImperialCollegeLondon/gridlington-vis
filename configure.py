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
import logging

logging.basicConfig(level=logging.INFO)


def get_ip_address():
    """Get the IP address of the machine"""

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.254.254.254", 1))
    ip = s.getsockname()[0]
    s.close()
    logging.info(f"IP address of the machine: {ip}...")
    return ip


def generate_docker_compose(template_file, ip):
    """
    Generate the docker-compose.yml file using a template file and the IP
    address of the machine.

    Args:
        template_file (str): Path to the template file.
        ip (str): IP address of the machine.

    Returns:
        None
    """
    lines_to_replace = {
        "OVE_HOST": f"{ip}:8080",
        "TOURIS_HOST": f"{ip}:7080",
        "OPENVIDU_HOST": f"{ip}:4443",
        "openvidu.publicurl": f"https://{ip}:4443",
    }

    # Read the template file
    logging.info(f"Generating docker-compose.yml...")
    with open(template_file, "r") as f:
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

    # Add the dash app to to docker-compose.yml file
    logging.info(f"Adding dash app to docker-compose.yml...")
    docker_compose["services"]["dash"] = {
        "build": ".",
        "ports": ["8050:8050"],
        "volumes": ["./dash:/app"],
    }

    # Configure logging for nginx
    logging.info(f"Adding volume for nginx logs...")
    docker_compose["services"]["nginx"]["volumes"] += [
        "./logs/nginx.log:/etc/nginx/logs/error.log"
    ]

    # Write the new docker-compose.yml file
    with open("docker-compose.yml", "w") as f:
        yaml.safe_dump(docker_compose, f)
    logging.info(f"docker-compose.yml generated.")


def generate_credentials_json(template_file, ip):
    """
    Generate the config/credentials.json file using a template file and the IP
    address of the machine.

    Args:
        template_file (str): Path to the template file.
        ip (str): IP address of the machine.

    Returns:
        None
    """
    # Read the template file
    logging.info(f"Editing config/credentials.json...")
    with open(template_file, "r") as f:
        credentials = json.load(f)

    # Replace the IP in the config/credentials.json file
    credentials["stores"][0]["proxyUrl"] = f"http://{ip}:6081/default/"

    # Write the new config/credentials.json file
    with open("config/credentials.json", "w") as f:
        json.dump(credentials, f, indent=2)
    logging.info(f"config/credentials.json generated.")


if __name__ == "__main__":
    ip = get_ip_address()
    generate_docker_compose("docker-compose.setup.ove.yml", ip)
    generate_credentials_json("credentials.setup.json", ip)
