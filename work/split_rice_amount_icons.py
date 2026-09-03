from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "assets" / "rice-amount-icons-3d.png"
image = Image.open(source).convert("RGBA")
width, height = image.size
cell_width = width // 3

items = [("full", 0), ("half", 1), ("empty", 2)]
output_dir = ROOT / "assets" / "rice-amount"
output_dir.mkdir(parents=True, exist_ok=True)

for name, col in items:
    crop = image.crop((col * cell_width, 0, (col + 1) * cell_width, height))
    pixels = []
    for red, green, blue, alpha in crop.getdata():
        if red > 246 and green > 242 and blue > 232:
            pixels.append((red, green, blue, 0))
        else:
            pixels.append((red, green, blue, alpha))
    crop.putdata(pixels)

    bounds = crop.getbbox()
    if bounds:
        crop = crop.crop(bounds)

    crop.thumbnail((240, 180), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (240, 180), (0, 0, 0, 0))
    canvas.alpha_composite(crop, ((240 - crop.width) // 2, (180 - crop.height) // 2))
    canvas.save(output_dir / f"{name}.png")

print(f"created {len(items)} rice amount icons")
