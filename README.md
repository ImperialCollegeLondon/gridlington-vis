# Notes

## Installation and setup

- Create a new conda environment and install requirements in `requirements.txt`.
- The `docker-compose.setup.ove.yml` file is used as a template to generate the `docker-compose.yml` file. The `docker-compose.yml` file is used to start the services.
- Run `python configure_ip.py` to create `docker-compose.yml` file, as well as the `config/credentials.json` file. The script should automatically detect the IP address of the host machine. and use it to configure the services.

N.B. The above process is required because the actual IP address is needed to configure the services. `localhost` or `127.0.0.1` cannot be used (at least `ove` doesn't work).
