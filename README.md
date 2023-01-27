# Notes

## Installation and setup

The `docker-compose.setup.ove.yml` file is used as a template to generate the `docker-compose.yml` file. The `docker-compose.yml` file is used to start the services. 

- Using a python3 environment with the `pyyaml` library added, run `python configure.py` to create the `docker-compose.yml` file. This also generates the `config/credentials.json` file. The script should automatically detect the IP address of the host machine and use it to configure the services.
- Run `docker-compose up -d` to start the OVE services.
- The Dash app should be available at `http://localhost:8050/`. There are four pages displaying an animated plot at `http://localhost:8050/plot1`, `http://localhost:8050/plot2` etc.
- The OVE landing page should bre available at http://localhost:8080.
- Go to `http://localhost:8080/ui/launcher` to launch a new OVE application. Select HTML from the dropdown list of app options. The URL should be `http://localhost:8050/plot1`, `http://localhost:8050/plot2` etc. depending on which page you want to display, then click launch at the bottom of the page.
- Click "Preview" at the bottom of the same page after launching, or navigate manually to e.g. http://192.168.1.249:8080/ui/preview?oveSpace=SpaceOne to preview each space in your browser.

N.B. The `configure.py` setup process is required because the actual IP address of the host machine is needed to configure the services. `localhost` or `127.0.0.1` cannot be used (at least OVE doesn't work).

## College VM configuration

A test version of the app is deployed at http://liionsden.rcs.ic.ac.uk:8080/ (internal access only). 

Utimately, we will want to automate this setup as much as possible so the environment (local testing vs. deployment) is autodetected. For now, the configuration files differ from those generated in the above setup in the following ways: 

**config/default.conf:**

```diff
-   server_name "";
+   server_name liionsden.rcs.ic.ac.uk;
```
