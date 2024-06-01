import logging

from mapgen import monsters_location

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

LIMIT = 100


def main():
    for monster in monsters_location:
        points = [
            complex(*(int(_) for _ in xy.split(",")))
            for xy in monsters_location[monster]
        ]

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                if 0 < abs(points[j] - points[i]) < LIMIT:
                    logger.warning(
                        "%s: (%d, %d) and (%d, %d) are too close.",
                        monster,
                        points[i].real,
                        points[i].imag,
                        points[j].real,
                        points[j].imag,
                    )


if __name__ == "__main__":
    main()
