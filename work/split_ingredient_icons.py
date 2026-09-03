from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "assets" / "ingredient-icons-3d.png"
image = Image.open(source).convert("RGBA")
width, height = image.size
cell_width, cell_height = width // 4, height // 2

items = [
    ("pumpkin", 0, 0),
    ("carrot", 1, 0),
    ("rice", 2, 0),
    ("tomato", 3, 0),
    ("egg", 0, 1),
    ("noodles", 1, 1),
    ("broccoli", 2, 1),
    ("sweet-potato", 3, 1),
]

output_dir = ROOT / "assets" / "ingredients"
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
    for red, green, blue, alpha in crop.getdata():
        if red > 245 and green > 240 and blue > 232:
            transparent_pixels.append((red, green, blue, 0))
        else:
            transparent_pixels.append((red, green, blue, alpha))
    crop.putdata(transparent_pixels)

    bounds = crop.getbbox()
    if bounds:
        crop = crop.crop(bounds)

    crop.thumbnail((240, 240), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
    canvas.alpha_composite(crop, ((240 - crop.width) // 2, (240 - crop.height) // 2))
    canvas.save(output_dir / f"{name}.png")

print(f"created {len(items)} icons")
