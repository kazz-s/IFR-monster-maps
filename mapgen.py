import logging
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from yaml import safe_load as load

MAP = "map.jpg"
COORDS = "monsters_location.yml"
R = 10

basepath = Path(__file__).parent

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

with open(basepath / COORDS) as f:
    monsters_location = load(f)


def draw_map(coords, color="blue") -> Image:
    fenyx_map = Image.open(basepath / MAP)
    draw = ImageDraw.Draw(fenyx_map)
    for x, y in coords:
        draw.ellipse((x - R, y - R, x + R, y + R), fill=color, outline="white")
    draw.text(
        xy=(10, 10),
        text=monster,
        fill=(255, 0, 0),
        font=ImageFont.load_default(size=82),
    )
    return fenyx_map


if __name__ == "__main__":
    for monster in monsters_location:
        coords = (
            (int(_) for _ in xy.split(","))
            for xy in monsters_location[monster]
        )
        draw_map(coords).save(basepath / "Maps" / f"{monster}.jpg")
        logger.info("Saving %s.jpg", monster)
