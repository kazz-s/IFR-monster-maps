from PIL import Image
import yaml

Image.MAX_IMAGE_PIXELS = 1 << 28  # 16k x 16k


def get_rate(from_, to_):
    p = Image.open(from_)
    q = Image.open(to_)

    return (
        q.width / p.width,
        q.height / p.height,
    )


def main():
    w_k, h_k = get_rate(from_="../map.jpg", to_="cropped.jpg")

    def scale(xy: str):
        x, y = [int(i) for i in xy.split(", ")]
        return f"{int(x*w_k)}, {int(y*h_k)}"

    with open("../monsters_location.yml") as f:
        current = yaml.safe_load(f)

    scalled = {k: [scale(xy) for xy in v] for k, v in current.items()}

    with open("monsters_location.yml", "w") as f:
        yaml.dump(scalled, f)


if __name__ == "__main__":
    main()
