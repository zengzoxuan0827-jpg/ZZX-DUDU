from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"C:\Users\Windows\AppData\Local\Temp\codex-clipboard-2106a0c1-6609-4e31-ad58-b86e85bb7b60.png")
OUT_DIR = ROOT / "assets" / "baby-moods"


def crop_face(sheet: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    face = sheet.crop(box).convert("RGBA")
    w, h = face.size
    ellipse_alpha = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(ellipse_alpha)
    draw.ellipse((18, 5, w - 18, h - 3), fill=255)
    ellipse_alpha = ellipse_alpha.filter(ImageFilter.GaussianBlur(1.4))

    bg_alpha = Image.new("L", (w, h), 0)
    src = face.load()
    out = bg_alpha.load()
    for y in range(h):
        for x in range(w):
            r, g, b, _ = src[x, y]
            brightness = (r + g + b) / 3
            saturation = max(r, g, b) - min(r, g, b)
            if brightness > 230 and saturation < 34:
                out[x, y] = 0
            elif brightness > 218 and saturation < 42:
                out[x, y] = 80
            else:
                out[x, y] = 255

    bg_alpha = bg_alpha.filter(ImageFilter.GaussianBlur(1.2))
    alpha = Image.new("L", (w, h), 0)
    alpha.paste(bg_alpha)
    alpha = Image.composite(alpha, Image.new("L", (w, h), 0), ellipse_alpha)
    face.putalpha(alpha)
    return face


def main() -> None:
    if not SOURCE.exists():
        print(f"SKIP split_baby_mood_icons: source sheet missing: {SOURCE}")
        print("  (preserving existing assets/baby-moods/*.png from a prior run)")
        return
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sheet = Image.open(SOURCE)
    w, h = sheet.size

    boxes = {
        "happy": (55, 22, w // 2 - 45, h // 2 - 32),
        "sad": (w // 2 + 45, 22, w - 55, h // 2 - 32),
        "angry": (55, h // 2 + 12, w // 2 - 45, h - 34),
        "normal": (w // 2 + 45, h // 2 + 12, w - 55, h - 34),
    }

    for name, box in boxes.items():
        icon = crop_face(sheet, box)
        icon.thumbnail((270, 270), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (320, 320), (0, 0, 0, 0))
        x = (320 - icon.width) // 2
        y = (320 - icon.height) // 2
        canvas.alpha_composite(icon, (x, y))
        canvas.save(OUT_DIR / f"{name}.png")
        print(OUT_DIR / f"{name}.png")


if __name__ == "__main__":
    main()
