from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
import pycli2
import datetime

load_dotenv()


class TextValue(BaseModel):
    text: str
    value: int


class Leg(BaseModel):
    duration: TextValue


class Route(BaseModel):
    legs: list[Leg]


class Direction(BaseModel):
    routes: list[Route]


def get_shortest_time(origin: str, destination: str) -> None:
    with requests.get(
        "https://maps.googleapis.com/maps/api/directions/json",
        {"origin": origin, "destination": destination, "key": os.environ["API_KEY"]},
    ) as response:
        response.raise_for_status()
        direction = Direction.model_validate(response.json())

    shortes_time = -1

    for route in direction.routes:
        total_time = 0
        for leg in route.legs:
            total_time += leg.duration.value

        if shortes_time == -1 or total_time < shortes_time:
            shortes_time = total_time

    print(
        ";".join(
            [
                datetime.datetime.now().isoformat(),
                origin,
                destination,
                str(shortes_time),
            ]
        )
    )


if __name__ == "__main__":
    pycli2.run(get_shortest_time)
