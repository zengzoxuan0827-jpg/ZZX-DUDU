from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "clean-icons"


def draw_icon(active: bool) -> Image.Image:
    size = 240
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = size // 2

    badge = (142, 207, 255, 255) if active else (210, 235, 255, 255)
    badge_edge = (92, 171, 236, 255) if active else (152, 205, 244, 255)
    inner = (232, 246, 255, 255)
    heart = (255, 126, 169, 255) if active else (255, 171, 198, 255)
    heart_deep = (241, 91, 142, 255) if active else (244, 132, 170, 255)
    yellow = (255, 215, 89, 255)

    points = []
    import math
    for i in range(8):
        angle = math.pi / 8 + i * math.pi / 4
        r = 100
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=badge, outline=badge_edge)
    draw.rounded_rectangle((52, 52, 188, 188), radius=46, fill=inner, outline=badge_edge, width=7)
    draw.arc((58, 50, 184, 178), 205, 40, fill=(255, 255, 255, 210), width=13)

    h = [
        (120, 172), (68, 128), (75, 78), (107, 76),
        (120, 99), (134, 76), (168, 80), (172, 128)
    ]
    draw.polygon(h, fill=heart_deep)
    draw.polygon([(120, 160), (78, 124), (83, 88), (108, 88), (120, 109), (132, 88), (158, 91), (162, 125)], fill=heart)
    draw.line((102, 94, 102, 127, 122, 127), fill=(255, 244, 250, 220), width=15)
    draw.rounded_rectangle((154, 72, 190, 104), radius=14, fill=yellow)

    return img


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    draw_icon(False).save(OUT_DIR / "like-3d.png")
    draw_icon(True).save(OUT_DIR / "like-3d-active.png")
    print(OUT_DIR / "like-3d.png")
    print(OUT_DIR / "like-3d-active.png")


if __name__ == "__main__":
    main()
