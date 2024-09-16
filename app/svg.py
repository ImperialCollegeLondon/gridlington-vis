"""Module for handling and displaying SVGs."""

import base64
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


class SVG:
    """Class to format SVGs for display."""

    def __init__(self, txt: str) -> None:  # type: ignore # noqa
        """Initialise class.

        Args:
            txt (str): String of SVG.
                e.g. Output of open(path, "rt", encoding="utf-8").read()
        """
        self.raw = txt

        # Header
        prefix, svg_content = self.raw.split("<svg", 1)
        svg_tag = svg_content.split(">", 1)[0]
        self.header = f"{prefix}<svg{svg_tag}>"

        # Image dimensions
        self.width, self.height = [
            int(self.raw.split(x, 1)[1].split(" ", 1)[0][2:-3])
            for x in ["width", "height"]
        ]
        self.aspect_ratio = self.width / self.height

        # Encode
        encoded = base64.b64encode(bytes(self.raw, "utf-8"))
        self.url = f"data:image/svg+xml;base64,{encoded.decode()}"


"""Load SVGs and Gridlington Datafile"""
with open(Path(__file__).parent / "map.svg", "rt", encoding="utf-8") as f:
    svg_map = SVG(f.read())

with open(Path(__file__).parent / "sld.svg", "rt", encoding="utf-8") as f:
    svg_sld = SVG(f.read())

with open(Path(__file__).parent / "GridlingtonData.json", "rt", encoding="utf-8") as f:
    Gridlington = json.load(f)

with open(
    Path(__file__).parent / "Agent_Location_Data.json", "rt", encoding="utf-8"
) as f:
    Agent_Locations = json.load(f)


def rotate_point_svg(
    point: tuple[float, float],
    center: tuple[float, float],
    angle: float,
) -> tuple[float, float]:
    """Rotates a point around a center point with a flipped y-axis (like in SVG).

    Args:
        point (tuple): The (x, y) coordinates of the point to rotate.
        center (tuple): The (cx, cy) coordinates of the center point.
        angle (float): The angle of rotation in degrees.

    Returns:
        tuple: The (x, y) coordinates of the rotated point.
    """
    angle_rad = math.radians(angle)  # Convert angle to radians
    x, y = point
    cx, cy = center

    # Translate point back to origin
    x -= cx
    y -= cy

    # Rotate point (accounting for flipped y-axis)
    x_new = x * math.cos(angle_rad) + y * math.sin(angle_rad)
    y_new = -x * math.sin(angle_rad) + y * math.cos(angle_rad)

    # Translate point back
    x_new += cx
    y_new += cy

    return x_new, y_new


def write_agents_sld(
    centre_x: float,
    centre_y: float,
    agent_count: int,
    angle_mid: float = 180.0,
    angle_range: float = 30.0,
    radius: float = 17.06,
    radius_delta: float = 4.0,
    dot_size: float = 1.5,
    colour: str = "#FFAA00",
) -> str:
    """Creates an SVG string of circles representing agents/EVs at a given locus.

    Args:
        centre_x (float): Centre of node (x coordinate)
        centre_y (float): Centre of node (y coordinate)
        agent_count (int): Number of agents/EVs
        angle_mid (float, optional): Normal distribution midpoint for dot
            placement. Defaults to 180.
        angle_range (float, optional): Normal distribution width for dot
            placement. Defaults to 30.
        radius (float, optional): Base radius for the dots. Defaults to 17.06.
        radius_delta (float, optional): How far to radially shift a dot if its
            home is filled. Defaults to 4.
        dot_size (float, optional): Size of each dot. Defaults to 1.5.
        colour (str, optional): HTML color code for the dots.
            Defaults to "#6A0DAD".

    Returns:
        str: An SVG string containing circles for each agent/EV
    """
    # Randomly generate angles
    rng = np.random.default_rng()
    angles = rng.normal(loc=angle_mid, scale=angle_range, size=agent_count)

    # Write agents
    agents_svg = ""
    used_angles = np.ones(360)  # number of dots at each angle
    for agent in range(agent_count):
        dot_ang = int(round(angles[agent - 1]))  # select our angle
        dot_r = radius + (
            radius_delta * used_angles[dot_ang - 1]
        )  # offset our dot so that its not on top of a previous one
        dot_xdiff = dot_r * math.cos(
            math.radians(dot_ang)
        )  # x position of our dot (from centre)
        dot_ydiff = dot_r * math.sin(
            math.radians(dot_ang)
        )  # y position of our dot (from centre)

        agents_svg += (
            f'<circle fill="{colour}" '
            f'stroke="#000000" '
            f'stroke-width="0" '
            f'cx="{centre_x + dot_ydiff}" '
            f'cy="{centre_y + dot_xdiff}" '
            f'r="{dot_size}"/>\n'
        )
        used_angles[dot_ang - 1] += 1  # mark down one more dot at this angle

    return agents_svg


def get_agent_sld_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Get agent SLD coordinates from Opal/DSR(?) dataframe.

    TODO: We want this function to take polygon data for each agent and
        convert it to x,y coordinates for location on the SLD (should
        correspond to the centre of one of the nodes in the diagram).
        This function will then output a dataframe of x,y coordinates and
        counts, corresponding to the number of agents at each node.

    For now, this is just making up random data

    Args:
        df (pd.DataFrame): Opal/DSR dataframe?

    Returns:
        pd.DataFrame: A dataframe agent counts at each x/y coordinate
    """
    nodes = svg_sld.raw.split("<circle")[1:]
    x_coordinates = [float(c.split('cx="')[1].split('"')[0]) for c in nodes]
    y_coordinates = [float(c.split('cy="')[1].split('"')[0]) for c in nodes]
    counts = np.random.randint(0, 100, len(x_coordinates))
    location_data = pd.DataFrame(
        {"x": x_coordinates, "y": y_coordinates, "count": counts}
    )
    return location_data


def get_ev_sld_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Get EV SLD coordinates from Opal/DSR(?) dataframe.

    TODO: We want this function to take polygon data for each EV and
        convert it to x,y coordinates for location on the SLD (should
        correspond to the centre of one of the nodes in the diagram).
        This function will then output a dataframe of x,y coordinates and
        counts, corresponding to the number of EVs at each node.

    For now, this is just making up random data

    Args:
        df (pd.DataFrame): Opal/DSR dataframe?

    Returns:
        pd.DataFrame: A dataframe EV counts at each x/y coordinate
    """
    nodes = svg_sld.raw.split("<circle")[1:]
    x_coordinates = [float(c.split('cx="')[1].split('"')[0]) for c in nodes]
    y_coordinates = [float(c.split('cy="')[1].split('"')[0]) for c in nodes]
    counts = np.random.randint(0, 100, len(x_coordinates))
    location_data = pd.DataFrame(
        {"x": x_coordinates, "y": y_coordinates, "count": counts}
    )
    return location_data


def get_agent_map_coordinates(df: pd.DataFrame) -> tuple[list[float], list[float]]:
    """Get agent map coordinates from Opal/DSR(?) dataframe.

    TODO: We want this function to take polygon data for each agent and
        convert it to x,y coordinates for location on the map. This function
        will then output two lists containing the x and y coordinates of each
        agent

    For now, this is just making up random data

    Args:
        df (pd.DataFrame): Opal/DSR dataframe?

    Returns:
        tuple[list[float], list[float]]: lists of x and y coordinates
    """
    time_of_day = len(df.columns)
    x_coordinates = []
    y_coordinates = []
    # agent_polys = np.random.uniform(
    #     0, len(Gridlington["Polygons"]["ID"]) - 1, 1000
    # ).tolist()

    agent_polys = Agent_Locations[time_of_day]

    for poly in agent_polys:
        poly_c = Gridlington["Polygons"]["SVG_Centre"][round(poly)]
        x_coordinates.append(poly_c[0] * (svg_map.width - 400))
        y_coordinates.append(poly_c[1] * (svg_map.width - 400))

    return x_coordinates, y_coordinates


def get_ev_map_coordinates(df: pd.DataFrame) -> tuple[list[float], list[float]]:
    """Get agent map coordinates from Opal/DSR(?) dataframe.

    TODO: We want this function to take polygon data for each EV and
        convert it to x,y coordinates for location on the map. This function
        will then output two lists containing the x and y coordinates of each
        EV

    For now, this is just making up random polygon number

    Args:
        df (pd.DataFrame): Opal/DSR dataframe?

    Returns:
        tuple[list[float], list[float]]: lists of x and y coordinates
    """
    x_coordinates = []
    y_coordinates = []
    # ev_polys = np.random.uniform(
    #     0, len(Gridlington["Polygons"]["ID"]) - 1, 1000
    # ).tolist()
    ev_polys = [1]

    for poly in ev_polys:
        poly_c = Gridlington["Polygons"]["SVG_Centre"][round(poly)]
        x_coordinates.append(poly_c[0] * (svg_map.width - 400))
        y_coordinates.append(poly_c[1] * (svg_map.width - 400))

    return x_coordinates, y_coordinates


def generate_sld_location_svg(
    location_data: pd.DataFrame,
    **kwargs: str | float,
) -> SVG:  # type: ignore # noqa
    """Generates an SVG of agent/EV locations for placement over the SLD image.

    Args:
        location_data (pd.DataFrame): A dataframe with columns x, y and count,
            representing the number of agents/EVs at each node
        kwargs: optional extra arguments for write_agents_sld

    Returns:
        SVG: SVG of EV/agent locations for placement over SLD
    """
    svg = svg_sld.header
    for _, row in location_data.iterrows():
        svg += write_agents_sld(
            centre_x=row["x"],
            centre_y=row["y"],
            agent_count=int(row["count"]),
            **kwargs,  # type: ignore # noqa
        )
    svg += "</svg>"
    return SVG(svg)


def generate_map_location_svg(
    x_coordinates: list[float],
    y_coordinates: list[float],
    dot_size: float = 3,
    colour: str = "#FFF000",
) -> SVG:
    """Generates an SVG of agent/EV locations for placement over the map image.

    Args:
        x_coordinates (list): List of x coordinates
        y_coordinates (list): List of y coordinates
        dot_size (float, optional): Size of each dot. Defaults to 1.5.
        colour (str, optional): HTML color code for the dots.
            Defaults to "#6A0DAD".

    Returns:
        SVG: SVG of EV/agent locations for placement over map
    """
    svg = svg_map.header
    for x, y in zip(x_coordinates, y_coordinates):
        svg += (
            f'<circle fill="{colour}" '
            f'stroke="#FFFFFF" '
            f'stroke-width="0" '
            f'cx="{x}" '
            f'cy="{y}" '
            f'r="{dot_size}"/>\n'
        )
    svg += "</svg>"
    return SVG(svg)


def generate_map_clock_svg(
    opal_data: pd.DataFrame,
    clock_cx: float = 2319,
    clock_cy: float = 250,
    clock_r: float = 150,
    sim_hour: float = 1,
    sim_min: float = 0,
) -> SVG:
    """Generates an SVG of the clock hands to show the time.

    Args:
        opal_data (pd.DataFrame): Opal dataframe
        clock_cx (float, optional): Clock centre x coordinate (defaults to 2319)
        clock_cy (float, optional): Clock centre y coordinate (defaults to 250)
        clock_r (float, optional): Clock radius (defaults to 150)
        sim_hour (float, optional): the hour component of the sim time (defaults to 1)
        sim_min (float, optional): the minute component of the sim time (defaults to 0)

    Returns:
        SVG: SVG of clock hands for placement over map
    """
    if len(opal_data.columns) == 1:  # No data so default to 3 o clock
        sim_hour = 3
        sim_min = 0
        sim_date = "Please Wait ..."
        # print("oops")
    else:  # strip the last datapoint for time into date and time, and then hours, mins
        sim_date_time = opal_data["Time"].values[-1]
        [sim_date, sim_time] = sim_date_time.split(" ", 1)
        [sim_hour, sim_min, sim_sec] = sim_time.split(":", 2)
        sim_hour = int(sim_hour)
        sim_min = int(sim_min)

    hour_colour = "#085573"
    hour_width = 9

    hour_length = clock_r / 2

    hour_x1 = clock_cx
    hour_y1 = clock_cy
    hour_x2 = clock_cx
    hour_y2 = clock_cy - hour_length

    if sim_hour >= 12:
        hour_angle = (sim_hour - 12) * -30
    else:
        hour_angle = sim_hour * -30

    [hour_x1, hour_y1] = rotate_point_svg(
        (hour_x1, hour_y1), (clock_cx, clock_cy), hour_angle
    )
    [hour_x2, hour_y2] = rotate_point_svg(
        (hour_x2, hour_y2), (clock_cx, clock_cy), hour_angle
    )

    clock_hour = (
        '<line x1="'
        + f"{hour_x1:.2f}"
        + '" y1="'
        + f"{hour_y1:.2f}"
        + '" x2="'
        + f"{hour_x2:.2f}"
        + '" y2="'
        + f"{hour_y2:.2f}"
        + '" stroke="'
        + hour_colour
        + '" stroke-width="'
        + str(hour_width)
        + '" />\n'
    )

    minute_colour = "#10A3DD"
    minute_width = 7
    minute_length = 5 * clock_r / 6

    minute_x1 = clock_cx
    minute_y1 = clock_cy
    minute_x2 = clock_cx
    minute_y2 = clock_cy - minute_length

    minute_angle = sim_min * -6

    [minute_x1, minute_y1] = rotate_point_svg(
        (minute_x1, minute_y1), (clock_cx, clock_cy), minute_angle
    )
    [minute_x2, minute_y2] = rotate_point_svg(
        (minute_x2, minute_y2), (clock_cx, clock_cy), minute_angle
    )

    clock_minute = (
        '<line x1="'
        + f"{minute_x1:.2f}"
        + '" y1="'
        + f"{minute_y1:.2f}"
        + '" x2="'
        + f"{minute_x2:.2f}"
        + '" y2="'
        + f"{minute_y2:.2f}"
        + '" stroke="'
        + minute_colour
        + '" stroke-width="'
        + str(minute_width)
        + '" />\n'
    )

    clock_time = (
        '<text x="'
        + str(clock_cx)
        + '" y="'
        + str(clock_cy + clock_r + 60)
        + '" fill="black" font-size="35" text-anchor="middle">'
        + f"{sim_hour:02}"
        + ":"
        + f"{sim_min:02}"
        + "</text>\n"
    )

    clock_date = (
        '<text x="'
        + str(clock_cx)
        + '" y="'
        + str(clock_cy + clock_r + 120)
        + '" fill="black" font-size="35" text-anchor="middle">'
        + sim_date
        + "</text>\n"
    )

    svg = svg_map.header
    svg += clock_hour
    svg += clock_minute
    svg += clock_time
    svg += clock_date
    svg += "</svg>"
    return SVG(svg)
