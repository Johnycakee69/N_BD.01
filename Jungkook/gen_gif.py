from PIL import Image, ImageDraw, ImageFont
import math, random
W,H=500,600
frames=24
random.seed(7)
confetti=[(random.randint(0,W), random.randint(0,H), random.choice([(255,230,109),(255,107,107),(200,182,255),(144,190,109),(247,37,133),(76,201,240)])) for _ in range(80)]
try:
    font_big=ImageFont.truetype("/usr/share/fonts/noto/NotoSerifDisplay-Regular.ttf",42)
    font_mid=ImageFont.truetype("/usr/share/fonts/noto/NotoSerif-Italic.ttf",30)
    font_sm=ImageFont.truetype("/usr/share/fonts/noto/NotoSerif-Regular.ttf",22)
    font_sm_b=ImageFont.truetype("/usr/share/fonts/noto/NotoSerif-Bold.ttf",22)
except:
    font_big=font_mid=font_sm=font_sm_b=ImageFont.load_default()

ims=[]
for f in range(frames):
    bounce=int(12*math.sin(2*math.pi*f/frames))
    wiggle=math.sin(2*math.pi*f/frames)*4
    img=Image.new("RGB",(W,H),(26,11,46))
    d=ImageDraw.Draw(img)
    # bg glow
    d.ellipse([50,20,450,450],fill=(75,30,138))
    d.ellipse([90,60,410,410],fill=(123,44,191))
    # title - elegant serif, letter-spaced feel
    d.text((W//2,28),"H A P P Y  B I R T H D A Y !",font=font_big,anchor="mt",fill=(249,241,214))
    d.text((W//2,76),"from Jungkook",font=font_mid,anchor="mt",fill=(224,195,252))
    cy=280+bounce
    # body
    d.rounded_rectangle([180,cy+90,320,cy+210],radius=25,fill=(123,44,191),outline=(90,24,154),width=4)
    d.text((250,cy+140),"JK",font=font_big,anchor="mm",fill="white")
    # head
    d.ellipse([160,cy-70,340,cy+110],fill=(255,217,179),outline=(234,182,140),width=3)
    # hair - classic neat cap (first try)
    d.pieslice([155,cy-80,345,cy+60],start=180,end=360,fill=(21,21,21))
    d.ellipse([180,cy-45,240,cy+10],fill=(21,21,21))
    d.ellipse([260,cy-45,320,cy+10],fill=(21,21,21))
    # eyes (blink every ~18 frames)
    blink = 0.15 if f%24>20 else 1
    for ex in [210,290]:
        d.ellipse([ex-13,cy+10,ex+13,cy+10+30*blink],fill="white")
        if blink>0.5:
            d.ellipse([ex-7,cy+18,ex+7,cy+32],fill=(58,35,23))
    # smile
    d.arc([225,cy+45,275,cy+80],start=10,end=170,fill=(122,59,46),width=3)
    d.rectangle([238,cy+58,262,cy+68],fill="white")
    # blush
    d.ellipse([175,cy+40,205,cy+55],fill=(255,154,162))
    d.ellipse([295,cy+40,325,cy+55],fill=(255,154,162))
    # sign
    sx0,sy0=95,cy+120+int(wiggle)
    sx1,sy1=405,cy+200+int(wiggle)
    d.rounded_rectangle([sx0,sy0,sx1,sy1],radius=12,fill=(255,248,220),outline=(255,77,109),width=5)
    d.text(((sx0+sx1)//2,(sy0+sy1)//2-8),"H A P P Y  B I R T H D A Y",font=font_sm,anchor="mm",fill=(255,77,109))
    d.text(((sx0+sx1)//2,(sy0+sy1)//2+18),"- A R M Y -",font=font_sm,anchor="mm",fill=(123,44,191))
    # confetti falling
    for i,(cx,cy0,col) in enumerate(confetti):
        yy=(cy0+f*12+i*7)%H
        xx=(cx+math.sin((f+i)/5)*10)%W
        d.rectangle([xx,yy,xx+8,yy+12],fill=col)
    ims.append(img)

ims[0].save("jungkook-birthday.gif",save_all=True,append_images=ims[1:],duration=80,loop=0)
print("saved jungkook-birthday.gif")
