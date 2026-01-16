import logging
import requests
from dotenv import load_dotenv
import os
import pycli2
import datetime

load_dotenv()


def get_shortest_time(origin: str, destination: str) -> None:
    with requests.post(
        "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix",
        json={
            "origins": [{"waypoint": {"address": origin}}],
            "destinations": [{"waypoint": {"address": destination}}],
        },
        params={"key": os.environ["API_KEY"], "$fields": "duration"},
    ) as response:
        response.raise_for_status()

        data = response.json()
        if not data:
            logging.error("Failed to fine route")
            exit(1)

    print(
        ";".join(
            [
                datetime.datetime.now().isoformat(),
                origin,
                destination,
                data[0]["duration"],
            ]
        )
    )


if __name__ == "__main__":
    pycli2.run(get_shortest_time)
