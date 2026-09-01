from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(r"C:\Users\Windows\Documents\ChatGPT\嘟嘟今天吃什么")
BABY = Path(r"C:\Users\Windows\AppData\Local\Temp\codex-clipboard-b6e96c1a-e840-4c00-85a8-ea3b6d71896f.png")
OUT = ROOT / "assets" / "previews" / "icon-transparent-scale-preview.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "msyhbd.ttc" if bold else "msyh.ttc"
    return ImageFont.truetype(str(Path(r"C:\Windows\Fonts") / name), size)


def baby_cutout(path: Path, size: int = 138) -> Image.Image:
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    alpha = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(alpha)
    draw.ellipse((8, 0, w - 8, h - 2), fill=255)
    alpha = alpha.filter(ImageFilter.GaussianBlur(1.2))
    img.putalpha(alpha)
    img.thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(img, ((size - img.width) // 2, (size - img.height) // 2))
    return canvas


def paste_fit(base: Image.Image, path: Path, center: tuple[int, int], box: int) -> None:
    icon = Image.open(path).convert("RGBA")
    px = icon.load()
    for y in range(icon.height):
        for x in range(icon.width):
            r, g, b, a = px[x, y]
            brightness = (r + g + b) / 3
            saturation = max(r, g, b) - min(r, g, b)
            # Remove baked-in soft ground shadows and pale background remnants.
            if a < 255 or (brightness > 118 and saturation < 82):
                px[x, y] = (r, g, b, 0)
    icon.thumbnail((box, box), Image.Resampling.LANCZOS)
    x = center[0] - icon.width // 2
    y = center[1] - icon.height // 2
    base.alpha_composite(icon, (x, y))


def draw_flat_icon(base: Image.Image, kind: str, center: tuple[int, int]) -> None:
    draw = ImageDraw.Draw(base)
    cx, cy = center
    if kind == "carrot":
        draw.polygon([(cx - 30, cy + 25), (cx - 5, cy - 24), (cx + 8, cy - 14), (cx - 17, cy + 32)], fill=(255, 139, 37))
        draw.line([(cx - 18, cy + 6), (cx - 4, cy - 1)], fill=(255, 185, 86), width=3)
        draw.line([(cx - 10, cy + 18), (cx + 1, cy + 12)], fill=(255, 185, 86), width=3)
        draw.ellipse((cx - 2, cy - 35, cx + 12, cy - 13), fill=(89, 188, 78))
        draw.ellipse((cx - 16, cy - 35, cx, cy - 12), fill=(106, 207, 91))
        draw.ellipse((cx + 8, cy - 31, cx + 23, cy - 10), fill=(75, 166, 70))
    elif kind in {"rice", "full", "half"}:
        draw.ellipse((cx - 31, cy - 21, cx + 31, cy + 7), fill=(255, 241, 201), outline=(224, 180, 104), width=3)
        draw.rounded_rectangle((cx - 28, cy - 9, cx + 28, cy + 30), radius=14, fill=(229, 178, 101), outline=(198, 145, 76), width=3)
        if kind != "half":
            for dx, dy in [(-18, -15), (-7, -18), (5, -15), (16, -17), (-1, -8)]:
                draw.ellipse((cx + dx - 4, cy + dy - 3, cx + dx + 5, cy + dy + 4), fill=(255, 255, 244))
        else:
            for dx, dy in [(-12, -13), (0, -14), (12, -12)]:
                draw.ellipse((cx + dx - 4, cy + dy - 3, cx + dx + 5, cy + dy + 4), fill=(255, 255, 244))
    elif kind == "empty":
        draw.ellipse((cx - 30, cy - 18, cx + 30, cy + 8), fill=(255, 240, 209), outline=(224, 180, 104), width=3)
        draw.rounded_rectangle((cx - 27, cy - 7, cx + 27, cy + 27), radius=14, fill=(231, 181, 105), outline=(198, 145, 76), width=3)
        draw.ellipse((cx - 22, cy - 13, cx + 22, cy + 4), fill=(251, 225, 178))
    elif kind == "clock":
        draw.ellipse((cx - 27, cy - 27, cx + 27, cy + 27), fill=(255, 220, 77), outline=(245, 174, 22), width=4)
        draw.ellipse((cx - 19, cy - 19, cx + 19, cy + 19), fill=(255, 250, 231), outline=(245, 174, 22), width=3)
        draw.line((cx, cy, cx, cy - 12), fill=(245, 174, 22), width=4)
        draw.line((cx, cy, cx + 11, cy + 5), fill=(245, 174, 22), width=4)
        draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=(245, 174, 22))


def rounded_card(draw: ImageDraw.ImageDraw, xy, radius, fill):
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGBA", (760, 560), (255, 246, 234, 255))
    draw = ImageDraw.Draw(canvas)

    draw.text((44, 32), "图标调整预览", fill=(36, 42, 58), font=font(30, True))
    draw.text((44, 76), "透明底 / 无投影 / 图标轻量化", fill=(126, 119, 111), font=font(18))

    # Mood card preview
    rounded_card(draw, (44, 118, 716, 282), 34, (255, 252, 244, 255))
    mood = baby_cutout(BABY, 138)
    canvas.alpha_composite(mood, (62, 130))
    draw.text((220, 154), "今天有点生气", fill=(31, 39, 59), font=font(28, True))
    draw.text((220, 198), "头像保持透明底，不加投影，视觉更干净。", fill=(111, 122, 146), font=font(17))
    for i, label in enumerate(["开心", "难过", "生气", "一般"]):
        x = 220 + i * 94
        fill = (255, 200, 40, 255) if label == "生气" else (255, 255, 255, 255)
        rounded_card(draw, (x, 232, x + 76, 266), 17, fill)
        draw.text((x + 22, 239), label, fill=(35, 39, 50), font=font(14, True))

    draw.text((54, 318), "页面图标缩小预览", fill=(36, 42, 58), font=font(22, True))
    draw.text((54, 350), "以下图标不放底块、不加投影，只保留透明 PNG 本体。", fill=(126, 119, 111), font=font(15))

    samples = [
        ("食材", ROOT / "assets" / "ingredients" / "carrot.png", 64),
        ("推荐", ROOT / "assets" / "ingredients" / "rice.png", 66),
        ("整碗", ROOT / "assets" / "rice-amount" / "full.png", 48),
        ("半碗", ROOT / "assets" / "rice-amount" / "half.png", 48),
        ("空碗", ROOT / "assets" / "rice-amount" / "empty.png", 48),
        ("时间", ROOT / "assets" / "time-clock-3d.png", 48),
    ]

    x0 = 60
    for index, (label, path, size) in enumerate(samples):
        cx = x0 + index * 108
        flat_kind = {
            "食材": "carrot",
            "推荐": "rice",
            "整碗": "full",
            "半碗": "half",
            "空碗": "empty",
            "时间": "clock",
        }[label]
        draw_flat_icon(canvas, flat_kind, (cx, 424))
        draw.text((cx - 16, 482), label, fill=(84, 82, 88), font=font(15, True))

    canvas.convert("RGB").save(OUT, quality=95)
    print(OUT)


if __name__ == "__main__":
    main()
