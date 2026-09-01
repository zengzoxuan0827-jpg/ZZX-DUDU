from pathlib import Path
from PIL import Image


ROOT = Path(r"C:\Users\Windows\Documents\ChatGPT\嘟嘟今天吃什么")
TARGETS = [
    ("ingredients", "clean-ingredients", ["carrot", "pumpkin", "rice", "noodles"]),
    ("rice-amount", "clean-rice-amount", ["full", "half", "empty"]),
]
SINGLE_TARGETS = [
    (ROOT / "assets" / "time-clock-3d.png", ROOT / "assets" / "clean-icons" / "time-clock.png"),
]


def clean_alpha(src: Path, dst: Path) -> None:
    img = Image.open(src).convert("RGBA")
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            brightness = (r + g + b) / 3
            saturation = max(r, g, b) - min(r, g, b)
            # Remove transparent antialias remnants and pale baked-in ground shadows,
            # while keeping colored food/body texture.
            if a < 230 or (brightness > 170 and saturation < 34):
                px[x, y] = (r, g, b, 0)
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst)
    print(dst)


def main() -> None:
    for source_dir, target_dir, names in TARGETS:
        for name in names:
            clean_alpha(
                ROOT / "assets" / source_dir / f"{name}.png",
                ROOT / "assets" / target_dir / f"{name}.png",
            )
    for src, dst in SINGLE_TARGETS:
        clean_alpha(src, dst)


if __name__ == "__main__":
    main()
