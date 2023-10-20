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

This service is mostly automated with a few steps required to be run outside of the docker container causing som limitations. To run a production version of this, the required files and directories are:

- `docker-compose.setup.ove.yml`
- `configure.py`
- `run.sh`
- `config/`
- `logs/` - this can be empty
- A `.env` file to define `MY_SECRET` for the OpenVidu login

To run the production version should be as simple as running `bash run.sh` with the above files alongside any override for watchtower etc.

Utimately, we will want to automate this setup as much as possible so the environment (local testing vs. deployment) is autodetected. For now, the configuration files differ from those generated in the above setup in the following ways:

**config/default.conf:**

```diff
-   server_name "";
+   server_name liionsden.rcs.ic.ac.uk;
```

## Current steps for Running a WebRTC app and sharing an application window

1. Make sure nothing's running
2. Run `bash run_develop.sh` for vis system to run config script and `docker-compose.yml`
   - For production, use `run.sh`
3. Go to OVE Core at the IP address defined in the `API_URL` environment variable you will now find in `docker-compose.yml`
4. Go to OpenVidu IP address and manually trust website (OPENVIDU_HOST in the `docker-compose.yml`)
5. Log in with username: admin, password: (OPENVIDU_SECRET from docker-compose.yml)
6. Open the View - link under Space Layouts, will be something like `IP`/view.html?oveViewId=PC01-Top-0
7. Open the Controller - link is ID Number under sections
8. Start the call from the Controller - will generate and display a Session ID
9. Copy the Session ID into the OpenVidu textbox to join the call (there should be three users connected to the call)
10. Share the application (NMX) window into the video call
11. Go to the Controller and select the desired screen to share. It should have a yellow box around it once selected.
12. Confirm the view is displaying the screen.

**Note:** Only one screen can be shared from one browser, so multiple screens will require multiple computers/browsers/incognito windows etc.
