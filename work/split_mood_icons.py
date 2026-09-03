from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "assets" / "mood-icons-jelly.png"
image = Image.open(source).convert("RGBA")
width, height = image.size
cell_width, cell_height = width // 2, height // 2

items = [
    ("happy", 0, 0),
    ("sad", 1, 0),
    ("angry", 0, 1),
    ("normal", 1, 1),
]

output_dir = ROOT / "assets" / "moods"
output_dir.mkdir(parents=True, exist_ok=True)

for name, col, row in items:
    crop = image.crop(
        (
            col * cell_width,
            row * cell_height,
            (col + 1) * cell_width,
            (row + 1) * cell_height,
        )
    )
    transparent_pixels = []
    for red, green, blue, alpha in crop.get_flattened_data():
        if red > 246 and green > 246 and blue > 246:
            transparent_pixels.append((red, green, blue, 0))
        else:
            transparent_pixels.append((red, green, blue, alpha))
    crop.putdata(transparent_pixels)

    bounds = crop.getbbox()
    if bounds:
        crop = crop.crop(bounds)

    crop.thumbnail((320, 260), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (320, 260), (0, 0, 0, 0))
    canvas.alpha_composite(crop, ((320 - crop.width) // 2, (260 - crop.height) // 2))
    canvas.save(output_dir / f"{name}.png")

print(f"created {len(items)} mood icons")
