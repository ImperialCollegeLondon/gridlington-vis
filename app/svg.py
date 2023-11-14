"""Module for handling and displaying SVGs."""

import base64
import math
from pathlib import Path

import numpy as np
import pandas as pd


class SVG:
    """Class to format SVGs for display."""

    def __init__(self, txt: str) -> None:  # type: ignore # noqa
        """Initialise class.

        Args:
            txt (str): String of svg.
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


# Load SVGs
with open(Path(__file__).parent / "map.svg", "rt", encoding="utf-8") as f:
    svg_map = SVG(f.read())

with open(Path(__file__).parent / "sld.svg", "rt", encoding="utf-8") as f:
    svg_sld = SVG(f.read())


def write_agents(
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
    """Create string of svg objects representing agents/EVs at a given locus.

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
        str: A string containing svg objects for each agent/EV
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


def generate_agent_location_sld_img(df: pd.DataFrame) -> str:
    """Generate encoded SVG of agent locations for placement over the SLD image.

    Args:
        df (pd.DataFrame): TODO

    Returns:
        str: Encoded SVG of agent locations for use via html.Img
    """
    # Make up data TODO: use real data
    circles = svg_sld.raw.split("<circle")[1:]
    xs = [float(c.split('cx="')[1].split('"')[0]) for c in circles]
    ys = [float(c.split('cy="')[1].split('"')[0]) for c in circles]
    data = pd.DataFrame({"x": xs, "y": ys, "count": np.random.randint(0, 100, len(xs))})

    # Write SVG
    svg = svg_sld.header
    for _, row in data.iterrows():
        svg += write_agents(row["x"], row["y"], int(row["count"]))
    svg += "</svg>"

    # Encode SVG
    svg_url = SVG(svg).url
    return svg_url


def generate_ev_location_sld_img(df: pd.DataFrame) -> str:
    """Generate encoded SVG of EV locations for placement over the SLD image.

    Args:
        df (pd.DataFrame): TODO

    Returns:
        str: Encoded SVG of EV locations for use via html.Img
    """
    # Make up data TODO: use real data
    circles = svg_sld.raw.split("<circle")[1:]
    xs = [float(c.split('cx="')[1].split('"')[0]) for c in circles]
    ys = [float(c.split('cy="')[1].split('"')[0]) for c in circles]
    data = pd.DataFrame({"x": xs, "y": ys, "count": np.random.randint(0, 100, len(xs))})

    # Write SVG
    svg = svg_sld.header
    for _, row in data.iterrows():
        svg += write_agents(row["x"], row["y"], int(row["count"]))
    svg += "</svg>"

    # Encode SVG
    svg_url = SVG(svg).url
    return svg_url
