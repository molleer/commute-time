from pathlib import Path
import pycli2
from datetime import datetime


def avg(nums: list[int]) -> float:
    return sum(nums) / len(nums)


def format(file: Path) -> None:
    rolling_average: list[int] = []
    lines: list[list[str]] = [line.split(";") for line in file.read_text().splitlines()]
    groups: dict[int, dict[str, dict[str, list[float]]]] = {}

    first_origin: str = lines[0][1]

    for row in lines:
        time = datetime.fromisoformat(row[0] + "Z")
        origin = row[1]
        duration = int(row[3][:-1])
        rolling_average.append(duration)

        if len(rolling_average) > 3:
            rolling_average.pop(0)

        weekday = time.weekday()
        clock = time.astimezone().strftime("%H:%M")
        groups.setdefault(weekday, {})
        groups[weekday].setdefault(origin, {})
        groups[weekday][origin].setdefault(clock, [])
        groups[weekday][origin][clock].append(avg(rolling_average))

    table: dict[str, list[str]] = {}

    for weekday in groups:
        for origin in groups[weekday]:
            for clock in groups[weekday][origin]:
                table.setdefault(clock, [""] * 14)
                i = weekday + (7 if origin == first_origin else 1)
                table[clock][i] = str(
                    sum(groups[weekday][origin][clock])
                    / len(groups[weekday][origin][clock])
                ).replace(".", ",")

    print(
        ";".join(
            [
                "time",
                *[f"not {first_origin} {n}" for n in range(7)],
                *[f"{first_origin} {n}" for n in range(7)],
            ]
        )
    )
    for clock in sorted(table):
        print(";".join([clock, *table[clock]]))


if __name__ == "__main__":
    pycli2.run(format)
