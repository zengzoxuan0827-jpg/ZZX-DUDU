from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BABY_SHEET = Path(r"C:\Users\Windows\AppData\Local\Temp\codex-clipboard-2106a0c1-6609-4e31-ad58-b86e85bb7b60.png")
OUT = ROOT / "assets" / "previews" / "mood-card-baby-preview.png"


def make_soft_cutout(img: Image.Image) -> Image.Image:
    img = img.convert("RGBA")
    w, h = img.size
    alpha = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(alpha)
    draw.ellipse((18, 5, w - 18, h - 3), fill=255)
    alpha = alpha.filter(ImageFilter.GaussianBlur(1.6))
    img.putalpha(alpha)
    return img


def main() -> None:
    if not BABY_SHEET.exists():
        print(f"SKIP make_baby_mood_preview: source image missing: {BABY_SHEET}")
        print("  (preserving existing assets/previews/mood-card-baby-preview.png)")
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)

    sheet = Image.open(BABY_SHEET)
    sw, sh = sheet.size

    # Top-left face is the happy expression, matching "今天很开心".
    happy = sheet.crop((55, 22, sw // 2 - 45, sh // 2 - 32))
    happy = make_soft_cutout(happy)
    happy.thumbnail((124, 118), Image.Resampling.LANCZOS)

    card = Image.new("RGBA", (367, 185), (0, 0, 0, 0))
    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((6, 8, 361, 178), radius=30, fill=(255, 205, 82, 34))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    card.alpha_composite(shadow)

    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle((0, 0, 367, 170), radius=30, fill=(255, 251, 239, 255))

    x = 24 + (124 - happy.width) // 2
    y = 32 + (118 - happy.height) // 2
    card.alpha_composite(happy, (x, y))

    title_font = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 26)
    body_font = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 14)
    draw.text((168, 38), "今天很开心", fill=(24, 33, 55), font=title_font)
    draw.text((168, 78), "主题色跟随心情变化，推荐", fill=(111, 122, 146), font=body_font)
    draw.text((168, 104), "一岁+软烂好入口的辅食。", fill=(111, 122, 146), font=body_font)

    card.convert("RGB").save(OUT, quality=95)
    print(OUT)


if __name__ == "__main__":
    main()
