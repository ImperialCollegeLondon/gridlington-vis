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


def write_agents_sld(
    centre_x: float,
    centre_y: float,
    agent_count: int,
    angle_mid: float = 180.0,
    angle_range: float = 30.0,
    radius: float = 17.06,
    radius_delta: float = 4.0,
    dot_size: float = 1.5,
    colour: str = "#6A0DAD",
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
    x_coordinates = []
    y_coordinates = []
    agent_polys = np.random.uniform(
        0, len(Gridlington["Polygons"]["ID"]) - 1, 1000
    ).tolist()

    for poly in agent_polys:
        poly_c = Gridlington["Polygons"]["SVG_Centre"][round(poly)]
        x_coordinates.append(poly_c[0] * svg_map.width)
        y_coordinates.append(poly_c[1] * svg_map.width)

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
    agent_polys = np.random.uniform(
        0, len(Gridlington["Polygons"]["ID"]) - 1, 1000
    ).tolist()

    for poly in agent_polys:
        poly_c = Gridlington["Polygons"]["SVG_Centre"][round(poly)]
        x_coordinates.append(poly_c[0] * svg_map.width)
        y_coordinates.append(poly_c[1] * svg_map.width)

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
    dot_size: float = 1.5,
    colour: str = "#6A0DAD",
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
            f'stroke="#000000" '
            f'stroke-width="0" '
            f'cx="{x}" '
            f'cy="{y}" '
            f'r="{dot_size}"/>\n'
        )
    svg += "</svg>"
    return SVG(svg)
