import logging
import requests
from dotenv import load_dotenv
import os
import pycli2
import datetime

load_dotenv()


def get_shortest_time(origin: str, destination: str) -> None:
    with requests.post(
        "https://routes.googleapis.com/directions/v2:computeRoutes",
        json={
            "origin": {"address": origin},
            "destination": {"address": destination},
            "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
            "trafficModel": "BEST_GUESS",
            "travelMode": "DRIVE",
        },
        params={"key": os.environ["API_KEY"], "$fields": "routes"},
    ) as response:
        response.raise_for_status()

        data = response.json()
        if not data["routes"]:
            logging.error("Failed to fine route")
            exit(1)

    print(
        ";".join(
            [
                datetime.datetime.now().isoformat(),
                origin,
                destination,
                data["routes"][0]["staticDuration"],
            ]
        )
    )


if __name__ == "__main__":
    pycli2.run(get_shortest_time)
