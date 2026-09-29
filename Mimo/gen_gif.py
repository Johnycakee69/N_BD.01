from PIL import Image, ImageDraw, ImageFont
import math, random
W, H = 500, 600
frames = 24
random.seed(7)
confetti = [(random.randint(0, W), random.randint(0, H),
             random.choice([(255, 230, 109), (255, 107, 107), (200, 182, 255),
                            (144, 190, 109), (247, 37, 133), (76, 201, 240)]))
            for _ in range(80)]
try:
    font_big = ImageFont.load_default(size=36)
    font_mid = ImageFont.load_default(size=28)
    font_sm = ImageFont.load_default(size=22)
except Exception:
    font_big = font_mid = font_sm = ImageFont.load_default()

HAIR = (36, 29, 25)
HAIR_DK = (25, 20, 17)
TEX = (74, 63, 53)
SHINE = (107, 93, 79)


def bez(p0, p1, p2, p3, n=20):
    """Cubic bezier sample points."""
    out = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t**3 * p3[0]
        y = mt**3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t**3 * p3[1]
        out.append((x, y))
    return out


def hair_silhouette(cy):
    """Soft side-swept hair: fluffy crown, rounded hairline, tapered sides.
    Head centre is (250, cy+20), spans x 160..340, top cy-70.
    """
    top = cy - 112
    pts = []
    # outer contour: left temple -> over the crown -> right temple
    pts += bez((156, cy + 30), (154, cy - 46), (196, top), (250, top))
    pts += bez((250, top), (304, top), (346, cy - 46), (344, cy + 30))
    # round off the right side tip
    pts += bez((344, cy + 30), (344, cy + 40), (334, cy + 42), (326, cy + 34))
    # inner right edge, up to the temple
    pts += bez((326, cy + 34), (330, cy + 12), (326, cy - 6), (320, cy - 22))
    # fringe hairline sweeping right -> left (clear of the eyes at cy+10)
    pts += bez((320, cy - 22), (306, cy - 32), (290, cy - 30), (276, cy - 26))
    pts += bez((276, cy - 26), (258, cy - 22), (242, cy - 27), (226, cy - 33))
    pts += bez((226, cy - 33), (208, cy - 37), (192, cy - 33), (178, cy - 27))
    # inner left edge, down to the temple
    pts += bez((178, cy - 27), (176, cy - 8), (174, cy + 8), (174, cy + 26))
    # round off the left side tip back to the start
    pts += bez((174, cy + 26), (168, cy + 40), (156, cy + 40), (156, cy + 30))
    return pts


ims = []
for f in range(frames):
    bounce = int(12 * math.sin(2 * math.pi * f / frames))
    wiggle = math.sin(2 * math.pi * f / frames) * 4
    img = Image.new("RGB", (W, H), (26, 11, 46))
    d = ImageDraw.Draw(img)
    d.ellipse([50, 20, 450, 450], fill=(75, 30, 138))
    d.ellipse([90, 60, 410, 410], fill=(123, 44, 191))
    d.text((W // 2, 30), "HAPPY BIRTHDAY!", font=font_big, anchor="mt", fill=(255, 230, 109))
    d.text((W // 2, 70), "from Jungkook", font=font_mid, anchor="mt", fill=(224, 195, 252))

    cy = 280 + bounce
    # body
    d.rounded_rectangle([180, cy + 90, 320, cy + 210], radius=25, fill=(123, 44, 191),
                        outline=(90, 24, 154), width=4)
    d.text((250, cy + 140), "JK", font=font_big, anchor="mm", fill="white")
    # head
    d.ellipse([160, cy - 70, 340, cy + 110], fill=(255, 217, 179),
              outline=(234, 182, 140), width=3)

    # ---- hair: first try classic ----
    d.pieslice([155, cy - 80, 345, cy + 60], start=180, end=360, fill=(21, 21, 21))
    d.ellipse([180, cy - 45, 240, cy + 10], fill=(21, 21, 21))
    d.ellipse([260, cy - 45, 320, cy + 10], fill=(21, 21, 21))

    # eyes (blink near end of loop)
    blink = 0.15 if f % 24 > 20 else 1
    for ex in (210, 290):
        d.ellipse([ex - 13, cy + 10, ex + 13, cy + 10 + 30 * blink], fill="white")
        if blink > 0.5:
            d.ellipse([ex - 7, cy + 18, ex + 7, cy + 32], fill=(58, 35, 23))
            d.ellipse([ex - 3, cy + 17, ex + 2, cy + 22], fill="white")
    # brows
    d.arc([197, cy - 6, 223, cy + 8], start=190, end=350, fill=HAIR, width=3)
    d.arc([277, cy - 6, 303, cy + 8], start=190, end=350, fill=HAIR, width=3)
    # smile + tooth
    d.arc([225, cy + 45, 275, cy + 80], start=10, end=170, fill=(122, 59, 46), width=3)
    d.rectangle([238, cy + 58, 262, cy + 68], fill="white")
    # blush
    d.ellipse([175, cy + 40, 205, cy + 55], fill=(255, 154, 162))
    d.ellipse([295, cy + 40, 325, cy + 55], fill=(255, 154, 162))

    # sign
    sx0, sy0 = 95, cy + 120 + int(wiggle)
    sx1, sy1 = 405, cy + 200 + int(wiggle)
    d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=12, fill=(255, 248, 220),
                        outline=(255, 77, 109), width=5)
    d.text(((sx0 + sx1) // 2, (sy0 + sy1) // 2 - 8), "HAPPY BIRTHDAY",
           font=font_sm, anchor="mm", fill=(255, 77, 109))
    d.text(((sx0 + sx1) // 2, (sy0 + sy1) // 2 + 18), "- ARMY -",
           font=font_sm, anchor="mm", fill=(123, 44, 191))

    # confetti
    for i, (cx, cy0, col) in enumerate(confetti):
        yy = (cy0 + f * 12 + i * 7) % H
        xx = (cx + math.sin((f + i) / 5) * 10) % W
        d.rectangle([xx, yy, xx + 8, yy + 12], fill=col)

    ims.append(img)

ims[0].save("jungkook-birthday.gif", save_all=True, append_images=ims[1:],
            duration=80, loop=0)
print("saved jungkook-birthday.gif")
