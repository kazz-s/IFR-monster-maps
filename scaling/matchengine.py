import json

from PIL import Image
import requests
from requests.auth import HTTPBasicAuth


Image.MAX_IMAGE_PIXELS = 1 << 28  # 16k x 16k


def compare(image1, image2):
    return requests.post(
        url="https://matchengine.tineye.com/sandbox/rest/compare/",
        auth=HTTPBasicAuth("matchengine_user", "matchengine_password"),
        params={"generate_overlay": True},
        files={
            "image1": open(image1, "rb"),
            "image2": open(image2, "rb"),
        },
    ).json()


def is_valid(diff):
    return all(
        (
            diff["status"] == "ok",
            not diff["error"],
            diff["result"],
        )
    )


def main(new_img, tempalte):

    diff = compare(new_img, tempalte)
    with open("diff.json", "w") as f:
        json.dump(diff, f, indent=2)

    if is_valid(diff):
        box = (
            diff["result"][0]["query_overlap_rect"]["left"],
            diff["result"][0]["query_overlap_rect"]["top"],
            diff["result"][0]["query_overlap_rect"]["right"],
            diff["result"][0]["query_overlap_rect"]["bottom"],
        )

        Image.open(new_img).crop(box).save("cropped.png")
    else:
        raise ValueError("no match")


map_offsets = {
    "Mobs/1.jpg": (0, 0),
    "Mobs/2.jpg": (5816, 0),
    "Mobs/3.jpg": (0, 6581),
    "Mobs/4.jpg": (5816, 6581),
}


def locate(mob):
    for map, offsets in map_offsets.items():
        diff = compare(map, mob)
        with open("diff.json", "w") as f:
            json.dump(diff, f, indent=2)
        if is_valid(diff):
            overlap = diff["result"][0]["query_overlap_rect"]
            return (
                overlap["left"] + offsets[0] + 2583,
                overlap["top"] + offsets[1] + 1453,
            )
    raise ValueError("no match")


def linspec(start, end, n):
    d = end - start
    return (start + (i * d) // n for i in range(n + 1))


def split(map, parts=4, s=2):

    img = Image.open(map)
    w = list(linspec(0, img.width, parts))
    h = list(linspec(0, img.height, parts * 2))

    print(w)
    print(h)

    for left, right in zip(w[:-s], w[s:]):
        for top, bottm in zip(h[:-s], h[s:]):
            img.crop((left, top, right, bottm)).save(f"{left}-{top}.jpg")
            # print(f"{left:5} {top:5} {right:5} {bottm:5}")


if __name__ == "__main__":
    # main("golden-isle_16k.jpg", "../map.jpg")
    # main("2.jpg", "Mobs/Gryphons/Gryphons.png")
    split("map.jpg")

    # from pathlib import Path

    # for i in Path("Mobs/SS").iterdir():
    #     print(i)
    #     print(f"{str(i):40} - {locate(str(i))}")
