"""Creates the docker-compose file for the machine it is run on.

Run this script to create the docker-compose.yml file using the
docker-compose.setup.ove.yml file and the IP address of the machine
Finds the line in docker-compose.setup.ove.yml that contain the host IP
address and replaces the value with the IP address of the machine in the new
file.
"""

import logging
import socket
import sys

import yaml

logging.basicConfig(level=logging.INFO)


def get_ip_address() -> str:
    """Get the IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.254.254.254", 1))
    ip = s.getsockname()[0]
    s.close()
    logging.info(f"IP address of the machine: {ip}...")
    return ip


def generate_docker_compose(
    template_file: str,
    ip: str,
    develop: bool = False,
    live_model: bool = False,
) -> None:
    """Generate the docker-compose.yml file.

    Uses a template file and the IP address of the machine.

    Args:
        template_file: Path to the template file.
        ip: IP address of the machine.
        develop: Flag for when running in develop mode (localhost for datahub).
        live_model: Flag for when running with a live model. This requires an available
            connection to a datahub, either in production or local for develop.

    Returns:
        None
    """
    lines_to_replace = {
        "OVE_HOST": f"{ip}:8080",
        "OPENVIDU_HOST": f"https://{ip}:4443",
        "PLOT_URL": f"{ip}:8050",
        "DH_URL": f"{ip}:80",
    }

    # Read the template file
    logging.info("Generating docker-compose.yml...")
    with open(template_file, "r") as f:
        docker_compose = yaml.safe_load(f)

    # Replace the values in the docker-compose.yml file
    docker_compose["services"]["ovehub-ove-apps"]["environment"]["OVE_HOST"] = (
        lines_to_replace["OVE_HOST"]
    )
    docker_compose["services"]["ovehub-ove-apps"]["environment"]["OPENVIDU_HOST"] = (
        lines_to_replace["OPENVIDU_HOST"]
    )
    docker_compose["services"]["ovehub-ove-ui"]["environment"]["OVE_HOST"] = (
        lines_to_replace["OVE_HOST"]
    )

    # Add the dash app to to docker-compose.yml file
    logging.info("Adding dash app to docker-compose.yml...")
    docker_compose["services"]["dash"] = {
        "ports": ["8050:8050"],
        "environment": {
            "API_URL": f"http://{lines_to_replace['OVE_HOST']}",
            "PLOT_URL": f"http://{lines_to_replace['PLOT_URL']}",
            "DH_URL": f"http://{lines_to_replace['DH_URL']}",
            "LOG_LEVEL": "DEBUG",
        },
        "depends_on": ["nginx"],
    }
    docker_compose["services"]["dash"]["volumes"] = ["./data:/data", "./logs:/logs"]

    if develop:
        docker_compose["services"]["dash"]["build"] = "."
        docker_compose["services"]["dash"]["volumes"] += ["./app:/app"]
        docker_compose["services"]["dash"]["environment"]["DH_URL"] = "http://127.0.0.1"
        docker_compose["services"]["dash"]["environment"]["LOG_LEVEL"] = "DEBUG"
    else:
        docker_compose["services"]["dash"]["environment"]["PRODUCTION"] = "true"
        docker_compose["services"]["dash"][
            "image"
        ] = "ghcr.io/imperialcollegelondon/gridlington-vis:latest"

    if live_model:
        docker_compose["services"]["dash"]["environment"]["LIVE_MODEL"] = "true"

    # Configure logging for nginx
    logging.info("Adding volume for nginx logs...")
    docker_compose["services"]["nginx"]["volumes"] += [
        "./logs/nginx.log:/etc/nginx/logs/error.log"
    ]

    # Write the new docker-compose.yml file
    with open("docker-compose.yml", "w") as f:
        yaml.safe_dump(docker_compose, f)
    logging.info("docker-compose.yml generated.")


if __name__ == "__main__":
    ip = get_ip_address()
    generate_docker_compose(
        "docker-compose.setup.ove.yml",
        ip,
        develop="develop" in sys.argv,
        live_model="live_model" in sys.argv,
    )
