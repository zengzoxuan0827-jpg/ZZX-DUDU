from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(r"C:\Users\Windows\Documents\ChatGPT\嘟嘟今天吃什么")
SRC_DIR = ROOT / "assets" / "rice-amount"
OUT_DIR = ROOT / "assets" / "clean-rice-amount"
NAMES = ("full", "half", "empty")


def seal_internal_alpha(name: str) -> None:
    img = Image.open(SRC_DIR / f"{name}.png").convert("RGBA")
    width, height = img.size
    pixels = img.load()
    outside = set()
    queue = deque()

    for x in range(width):
        for y in (0, height - 1):
            if pixels[x, y][3] == 0:
                queue.append((x, y))
                outside.add((x, y))
    for y in range(height):
        for x in (0, width - 1):
            if pixels[x, y][3] == 0 and (x, y) not in outside:
                queue.append((x, y))
                outside.add((x, y))

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in outside:
                if pixels[nx, ny][3] == 0:
                    outside.add((nx, ny))
                    queue.append((nx, ny))

    holes = [(x, y) for y in range(height) for x in range(width) if pixels[x, y][3] == 0 and (x, y) not in outside]
    for x, y in holes:
        samples = []
        for radius in range(1, 7):
            for ny in range(max(0, y - radius), min(height, y + radius + 1)):
                for nx in range(max(0, x - radius), min(width, x + radius + 1)):
                    r, g, b, a = pixels[nx, ny]
                    if a > 0 and (nx, ny) not in holes:
                        samples.append((r, g, b, a))
            if samples:
                break

        if samples:
            total_alpha = sum(a for _, _, _, a in samples)
            r = round(sum(r * a for r, _, _, a in samples) / total_alpha)
            g = round(sum(g * a for _, g, _, a in samples) / total_alpha)
            b = round(sum(b * a for _, _, b, a in samples) / total_alpha)
            pixels[x, y] = (r, g, b, 255)
        else:
            pixels[x, y] = (248, 224, 178, 255)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img.save(OUT_DIR / f"{name}.png")


def main() -> None:
    for name in NAMES:
        seal_internal_alpha(name)


if __name__ == "__main__":
    main()
