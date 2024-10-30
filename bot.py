# SPDX-License-Identifier: BSD-3-Clause

# flake8: noqa F401
from collections.abc import Callable

import numpy as np

from vendeeglobe import (
    Checkpoint,
    Heading,
    Instructions,
    Location,
    Vector,
    config,
)
from vendeeglobe.utils import distance_on_surface
from vendeeglobe import play

play.course_preview=[
                     Checkpoint(latitude=43.797109, longitude=-11.264905, radius=50),
                     Checkpoint(longitude=-29.908577, latitude=17.999811, radius=50),
]

class Bot:
    """
    This is the ship-controlling bot that will be instantiated for the competition.
    """

    def __init__(self):
        self.team = "TeamName"  # This is your team name
        # This is the course that the ship has to follow
        self.course = [
            Checkpoint(latitude=40.87907046007358, longitude=-32.46582250480802, radius=1), # bom på øy
            Checkpoint(latitude=17.0138350185302, longitude=-69.19020108068081, radius=1), # jamaicaish
            Checkpoint(latitude=10.514597482803084, longitude=-80.22749180750842, radius=1), # pre panama
            Checkpoint(latitude=6.322062464497975, longitude=-78.697351206516, radius=1), # post panama
            Checkpoint(latitude=16.75287814411725, longitude=-164.1000368159, radius=1), # check 1

            Checkpoint(latitude=-47, longitude=146.1000368159, radius=1), # sør for australia

            Checkpoint(latitude=-9, longitude=77, radius=1), # check 2

            Checkpoint(latitude=14.9, longitude=54, radius=1), # pre arab
            Checkpoint(latitude=11.5, longitude=44, radius=1), # sues
            Checkpoint(latitude=28, longitude=34, radius=1), # sues
            Checkpoint(latitude=29, longitude=32, radius=1), # exit sues

            Checkpoint(latitude=14.881699, longitude=-21.024326, radius=50.0),
            Checkpoint(latitude=44.076538, longitude=-18.292936, radius=50.0),
            Checkpoint(
                latitude=config.start.latitude,
                longitude=config.start.longitude,
                radius=5,
            ),
        ]

    def run(
        self,
        t: float,
        dt: float,
        longitude: float,
        latitude: float,
        heading: float,
        speed: float,
        vector: np.ndarray,
        forecast: Callable,
        world_map: Callable,
    ) -> Instructions:
        """
        This is the method that will be called at every time step to get the
        instructions for the ship.

        Parameters
        ----------
        t:
            The current time in hours.
        dt:
            The time step in hours.
        longitude:
            The current longitude of the ship.
        latitude:
            The current latitude of the ship.
        heading:
            The current heading of the ship.
        speed:
            The current speed of the ship.
        vector:
            The current heading of the ship, expressed as a vector.
        forecast:
            Method to query the weather forecast for the next 5 days.
            Example:
            current_position_forecast = forecast(
                latitudes=latitude, longitudes=longitude, times=0
            )
        world_map:
            Method to query map of the world: 1 for sea, 0 for land.
            Example:
            current_position_terrain = world_map(
                latitudes=latitude, longitudes=longitude
            )

        Returns
        -------
        instructions:
            A set of instructions for the ship. This can be:
            - a Location to go to
            - a Heading to point to
            - a Vector to follow
            - a number of degrees to turn Left
            - a number of degrees to turn Right

            Optionally, a sail value between 0 and 1 can be set.
        """
        # Initialize the instructions
        instructions = Instructions()

        # TODO: Remove this, it's only for testing =================
        # current_position_forecast = forecast(
        #     latitudes=latitude, longitudes=longitude, times=0
        # )
        current_position_terrain = world_map(latitudes=latitude, longitudes=longitude)
        # ===========================================================

        # Check if we hit land, and set heating to 90 degrees of current heading
        # if current_position_terrain == 0:
        #     print(instructions.heading)
        #     instructions.heading = heading + 15
        #     return instructions


        # Go through all checkpoints and find the next one to reach
        for ch in self.course:
            # Compute the distance to the checkpoint
            dist = distance_on_surface(
                longitude1=longitude,
                latitude1=latitude,
                longitude2=ch.longitude,
                latitude2=ch.latitude,
            )
            # # Consider slowing down if the checkpoint is close
            # jump = dt * np.linalg.norm(speed)
            # if dist < 2.0 * ch.radius + jump:
            #     instructions.sail = min(ch.radius / jump, 1)
            # else:
            #     instructions.sail = 1.0

            # Check if the checkpoint has been reached
            if dist < ch.radius:
                ch.reached = True
            if not ch.reached:
                instructions.location = Location(
                    longitude=ch.longitude, latitude=ch.latitude
                )
                break

        return instructions
