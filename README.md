# Notes

## Installation and setup

The `docker-compose.setup.ove.yml` file is used as a template to generate the `docker-compose.yml` file. The `docker-compose.yml` file is used to start the services.

1. Using a python3 environment with the `pyyaml` library added, run `python configure.py develop` to create the `docker-compose.yml` file. This also generates the `config/credentials.json` file. The script should automatically detect the IP address of the host machine and use it to configure the services.
2. Run `docker-compose up -d` to start the OVE services.
3. There is a convenience script, `run.sh` which combines the above two steps for running in develop mode.
4. The Dash app should be available at http://localhost:8050/. There are four pages displaying an animated plot at `http://localhost:8050/plot1`, `http://localhost:8050/plot2` etc. <!-- markdownlint-disable-line MD034 -->
5. The OVE landing page should be available at http://localhost:8080. <!-- markdownlint-disable-line MD034 -->
6. Go to `http://localhost:8080/ui/launcher` to launch a new OVE application. Select HTML from the dropdown list of app options. The URL should be `http://localhost:8050/plot1`, `http://localhost:8050/plot2` etc. depending on which page you want to display, then click launch at the bottom of the page.
7. Click "Preview" at the bottom of the same page after launching, or navigate manually to e.g. http://192.168.1.249:8080/ui/preview?oveSpace=SpaceOne to preview each space in your browser. <!-- markdownlint-disable-line MD034 -->

N.B. The `configure.py` setup process is required because the actual IP address of the host machine is needed to configure the services. `localhost` or `127.0.0.1` cannot be used (at least OVE doesn't work).

## College VM configuration

A test version of the app is deployed at http://liionsden.rcs.ic.ac.uk:8080/ (internal access only). <!-- markdownlint-disable-line MD034 -->

Utimately, we will want to automate this setup as much as possible so the environment (local testing vs. deployment) is autodetected. For now, the configuration files differ from those generated in the above setup in the following ways:

**config/default.conf:**

```diff
-   server_name "";
+   server_name liionsden.rcs.ic.ac.uk;
```

## Current steps for Running a WebRTC app and sharing an application window

1. Make sure nothings running
2. Run `run.sh`` for vis system to run config script and docker-compose
   * For local/develop versions, use locally built images (the run.sh should cover the config for this). Images must be named:
     * ove-apps:9.9.9
     * ove-ove:9.9.9
     * ove-ui:9.9.9
   * Check get_ip_address is correct
   * Check ip address from configure.py is running OVE
3. Go to OVE Core at http://localhost:8080  <!-- markdownlint-disable-line MD034 -->
4. Select "Launch new OVE Application instances"
5. Select WebRTC application, fill in settings and launch instance
6. Start call button on controller and get session ID
   * Note: closing controller ends the session
7. Go to openvidu ip address and manually trust website (OPENVIDU_HOST in the docker-compose.yml)
8. Log in with username: admin, password: (OPENVIDU_SECRET from docker-compose.yml)
9. Enter session ID (from controller window) as room name and join the call
10. Share a window and check it can be viewed from other windows

**Note:** Only one screen can be shared from one browser, so multiple screens will require multiple computers/browsers/incognito windows etc.
