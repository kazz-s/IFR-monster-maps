import logging
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from yaml import safe_load as load

Image.MAX_IMAGE_PIXELS = 1 << 28  # 16k x 16k

MAP = "map.jpg"
COORDS = "monsters_location.yml"
r = 50
R = 57

basepath = Path(__file__).parent

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

with open(basepath / COORDS) as f:
    monsters_location = load(f)


def draw_map(coords, color="blue", title="") -> Image:
    fenyx_map = Image.open(basepath / MAP)
    draw = ImageDraw.Draw(fenyx_map)
    for x, y in coords:
        draw.ellipse((x - R, y - R, x + R, y + R), fill="white")
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
    draw.text(
        xy=(60, 60),
        text=title,
        fill=(255, 0, 0),
        font=ImageFont.load_default(size=470),
    )
    return fenyx_map


if __name__ == "__main__":
    for monster in monsters_location:
        if monster != "Chimeras":
            continue
        coords = (
            (int(_) for _ in xy.split(","))
            for xy in monsters_location[monster]
        )
        draw_map(coords, title=monster).save(
            basepath / "Maps" / f"{monster}.jpg"
        )
        logger.info("Saving %s.jpg", monster)
