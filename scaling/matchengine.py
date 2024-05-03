import json

from PIL import Image
import requests
from requests.auth import HTTPBasicAuth


Image.MAX_IMAGE_PIXELS = 1 << 28  # 16k x 16k


def compare(image1, image2):
    return requests.post(
        url="https://matchengine.tineye.com/sandbox/rest/compare/",
        auth=HTTPBasicAuth("matchengine_user", "matchengine_password"),
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
            diff["result"][0]["target_overlap_percent"] > 99,
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

    Image.open(new_img).crop(box).save("cropped.jpg")


if __name__ == "__main__":
    main("golden-isle_16k.jpg", "../map.jpg")
