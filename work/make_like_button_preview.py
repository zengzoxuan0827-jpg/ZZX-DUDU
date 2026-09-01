from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"C:\Users\Windows\Documents\ChatGPT\嘟嘟今天吃什么")
OUT = ROOT / "assets" / "previews" / "like-button-preview.png"


def font(size: int, bold: bool = False):
    name = "msyhbd.ttc" if bold else "msyh.ttc"
    return ImageFont.truetype(str(Path(r"C:\Windows\Fonts") / name), size)


def draw_like_button(draw: ImageDraw.ImageDraw, x: int, y: int, active: bool = False) -> None:
    fill = (255, 201, 40) if active else (255, 255, 255)
    line = (45, 43, 48) if active else (245, 174, 22)
    text = (60, 43, 0) if active else (126, 119, 111)
    draw.rounded_rectangle((x, y, x + 76, y + 76), radius=24, fill=fill)

    cx, cy = x + 38, y + 34
    w = 3
    draw.arc((cx - 22, cy - 21, cx + 22, cy + 23), start=30, end=320, fill=line, width=w)
    draw.arc((cx - 24, cy - 8, cx - 9, cy + 7), start=86, end=270, fill=line, width=w)
    draw.arc((cx + 9, cy - 8, cx + 24, cy + 7), start=270, end=92, fill=line, width=w)
    draw.arc((cx - 6, cy - 24, cx + 8, cy - 11), start=105, end=410, fill=line, width=w)
    draw.ellipse((cx - 10, cy - 5, cx - 6, cy - 1), fill=line)
    draw.ellipse((cx + 6, cy - 5, cx + 10, cy - 1), fill=line)
    draw.arc((cx - 9, cy - 3, cx + 9, cy + 14), start=20, end=160, fill=line, width=w)

    hx, hy = x + 55, y + 52
    heart = [
        (hx, hy + 10), (hx - 14, hy - 2), (hx - 12, hy - 13), (hx - 3, hy - 13),
        (hx, hy - 8), (hx + 3, hy - 13), (hx + 12, hy - 13), (hx + 14, hy - 2)
    ]
    draw.line(heart + [(hx, hy + 10)], fill=line, width=w, joint="curve")
    draw.text((x + 19, y + 86), "喜欢", fill=text, font=font(15, True))


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (760, 420), (255, 246, 234))
    draw = ImageDraw.Draw(img)

    draw.text((44, 38), "喜欢按钮预览", fill=(36, 42, 58), font=font(30, True))
    draw.text((44, 82), "参考宝宝脸 + 爱心语义，适配当前圆润 Apple 风界面。", fill=(126, 119, 111), font=font(17))

    draw.rounded_rectangle((44, 128, 716, 290), radius=34, fill=(255, 252, 244))
    draw.text((76, 164), "南瓜胡萝卜软饭", fill=(31, 39, 59), font=font(24, True))
    draw.text((76, 204), "接受度高，可优先推荐", fill=(111, 122, 146), font=font(16))
    draw_like_button(draw, 570, 156, active=False)

    draw.text((118, 330), "默认态", fill=(84, 82, 88), font=font(16, True))
    draw_like_button(draw, 94, 230, active=False)
    draw.text((298, 330), "选中态", fill=(84, 82, 88), font=font(16, True))
    draw_like_button(draw, 274, 230, active=True)
    draw.text((454, 330), "用于：宝宝喜欢 / 收藏辅食 / 接受度高", fill=(126, 119, 111), font=font(16))

    img.save(OUT, quality=95)
    print(OUT)


if __name__ == "__main__":
    main()
