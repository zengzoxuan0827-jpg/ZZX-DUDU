from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(r"C:\Users\Windows\Documents\ChatGPT\嘟嘟今天吃什么")
OUT = ROOT / "assets" / "previews" / "badge-like-button-preview.png"


def font(size: int, bold: bool = False):
    name = "msyhbd.ttc" if bold else "msyh.ttc"
    return ImageFont.truetype(str(Path(r"C:\Windows\Fonts") / name), size)


def draw_badge_like(draw: ImageDraw.ImageDraw, x: int, y: int, size: int, active: bool) -> None:
    blue = (142, 206, 255) if active else (202, 231, 255)
    blue_deep = (104, 179, 239) if active else (152, 204, 245)
    pink = (255, 129, 169) if active else (255, 165, 191)
    yellow = (255, 213, 86)

    cx = x + size // 2
    cy = y + size // 2
    r = size // 2 - 3
    points = []
    for i in range(8):
        import math
        angle = math.pi / 8 + i * math.pi / 4
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=blue, outline=blue_deep)

    inset = size * .14
    draw.rounded_rectangle((x + inset, y + inset, x + size - inset, y + size - inset), radius=int(size * .28), fill=(225, 243, 255), outline=blue_deep, width=2)
    draw.arc((x + size * .18, y + size * .16, x + size * .84, y + size * .78), 205, 38, fill=(255, 255, 255), width=max(2, size // 16))

    hx, hy = cx - size * .03, cy + size * .08
    heart = [
        (hx, hy + size * .24),
        (hx - size * .31, hy + size * .02),
        (hx - size * .27, hy - size * .23),
        (hx - size * .08, hy - size * .25),
        (hx, hy - size * .10),
        (hx + size * .08, hy - size * .25),
        (hx + size * .29, hy - size * .21),
        (hx + size * .31, hy + size * .04),
    ]
    draw.polygon(heart, fill=pink)
    draw.line((cx - size * .13, cy - size * .10, cx - size * .13, cy + size * .08, cx, cy + size * .08), fill=(255, 245, 248), width=max(4, size // 12))
    draw.rounded_rectangle((x + size * .65, y + size * .28, x + size * .82, y + size * .43), radius=max(4, size // 13), fill=yellow)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (760, 430), (255, 246, 234))
    draw = ImageDraw.Draw(img)

    draw.text((44, 38), "喜欢按钮预览", fill=(36, 42, 58), font=font(30, True))
    draw.text((44, 82), "参考粉色爱心徽章，适配当前宝宝辅食 App 的圆润风格。", fill=(126, 119, 111), font=font(17))

    draw.rounded_rectangle((44, 128, 716, 294), radius=34, fill=(255, 252, 244))
    draw.text((76, 164), "南瓜胡萝卜软饭", fill=(31, 39, 59), font=font(24, True))
    draw.text((76, 204), "宝宝喜欢，可优先推荐", fill=(111, 122, 146), font=font(16))
    draw_badge_like(draw, 585, 160, 58, True)

    draw_badge_like(draw, 100, 248, 58, False)
    draw.text((109, 324), "默认", fill=(84, 82, 88), font=font(15, True))
    draw_badge_like(draw, 258, 238, 78, True)
    draw.text((274, 324), "选中", fill=(84, 82, 88), font=font(15, True))
    draw.text((430, 300), "用于：宝宝喜欢 / 收藏辅食 / 接受度高", fill=(126, 119, 111), font=font(16))

    img.save(OUT, quality=95)
    print(OUT)


if __name__ == "__main__":
    main()
