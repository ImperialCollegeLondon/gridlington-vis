# Notes

## Installation and setup

- Create a new conda environment and install requirements in `requirements.txt`.
- The `docker-compose.setup.ove.yml` file is used as a template to generate the `docker-compose.yml` file. The `docker-compose.yml` file is used to start the services.
- Run `python configure_ip.py` to create `docker-compose.yml` file, as well as the `config/credentials.json` file. The script should automatically detect the IP address of the host machine. and use it to configure the services.

N.B. The above process is required because the actual IP address is needed to configure the services. `localhost` or `127.0.0.1` cannot be used (at least OVE doesn't work).

## OVE testing

- Run `docker-compose up -d` to start the OVE services.
- Run `python app.py` to start the dash app. The app should be available at `http://localhost:8050/`.
- There are four pages displaying an animated plot at `http://localhost:8050/plot1`, `http://localhost:8050/plot2` etc.
- Go to `http://localhost:8080/ui/launcher` to launch a new OVE application. The URL should be `http://localhost:8050/plot1`, `http://localhost:8050/plot2` etc. depending on which page you want to display.

## TODO

- Finesse the OVE configuration process.
- Use the python API to launch OVE applications.
- Containerise dash app.
