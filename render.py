#!/usr/bin/env python3
"""Clawd Studio — hand-built, consistently rigged pixel-art GIF stickers.

Run: python render.py
Dependency: Pillow>=10
All artwork is original fan-art, independently drawn using small geometric shapes.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import random

ROOT = Path(__file__).resolve().parent
GIFS = ROOT / 'gifs'
PNGS = ROOT / 'png'
PREVIEW = ROOT / 'preview'
for folder in (GIFS, PNGS, PREVIEW): folder.mkdir(parents=True, exist_ok=True)

W, SCALE, FRAMES, MS = 96, 4, 32, 60
C = {
    'outline': '#703E38', 'shadow': '#B65F4A', 'body': '#DA7758',
    'light': '#F09B76', 'shine': '#FFD1A0', 'deep': '#994A3F',
    'ink': '#352D32', 'pink': '#F56B90', 'pink_hi': '#FFB6C6',
    'red': '#F15959', 'gold': '#FFCA64', 'cream': '#FFF0C9',
    'blue': '#6FC8EE', 'blue_hi': '#B9ECFF', 'mint': '#84D4B2',
    'purple': '#A999F2', 'darkblue': '#293A52', 'screen': '#405B70',
    'white': '#FFFFFF', 'steam': '#BCC5C5',
}
COLORS = [(0,0,0)] + [tuple(bytes.fromhex(c[1:])) for c in C.values()]
PALETTE = [v for rgb in COLORS for v in rgb]
PALETTE += [0] * (768 - len(PALETTE))
INDEX = {rgb:i for i,rgb in enumerate(COLORS)}

SETS = [
    ('wave','Hi!','挥手打招呼'), ('yay','Yay!','开心庆祝'),
    ('love','Love','爱心暴击'), ('typing','Typing','疯狂敲代码'),
    ('think','Thinking','认真思考'), ('sleep','Sleep','困困睡觉'),
    ('cry','Cry','委屈哭哭'), ('angry','Angry','气鼓鼓'),
    ('wow','Wow!','震惊了'), ('coffee','Coffee','续命咖啡'),
    ('dance','Dance','快乐跳舞'), ('hug','Hug','给你抱抱'),
]

# Canvas draws a little pixel art directly, no antialias and no assets lifted from the web.
class Draw:
    def __init__(self, im):
        self.im = im
        self.d = ImageDraw.Draw(im)
    def r(self, x, y, w, h, fill):
        self.d.rectangle((int(round(x)),int(round(y)),int(round(x+w-1)),int(round(y+h-1))),fill=fill)
    def p(self,x,y,fill): self.r(x,y,2,2,fill)
    def rect(self,x,y,w,h,fill,outer='outline',stroke=2):
        self.r(x-stroke,y-stroke,w+2*stroke,h+2*stroke,C.get(outer,outer))
        self.r(x,y,w,h,C.get(fill,fill))


def star(d,x,y,color='gold',r=4):
    d.r(x-r,y-1,2*r+1,3,C[color]); d.r(x-1,y-r,3,2*r+1,C[color]); d.r(x,y,1,1,C['cream'])

def heart(d,x,y,scale=1,color='pink'):
    # 11x10 pixel heart, coherent blocky geometry.
    matrix=['.##...##.','####.####','#########','#########','.#######.','..#####..','...###...','....#....']
    for yy,row in enumerate(matrix):
        for xx,ch in enumerate(row):
            if ch=='#': d.r(x+xx*scale,y+yy*scale,scale,scale,C[color])
    if scale>=2:
        d.r(x+2*scale,y+1*scale,scale,scale,C['pink_hi'])

def bubble(d,x,y,tone='cream'):
    d.rect(x,y,11,8,tone,stroke=1)
    d.r(x+2,y+8,2,2,C[tone])

def body(d, t, kind, bob=0, lean=0):
    x, y = 28+lean, 30+bob
    # Ground contact is deliberately understated so stickers remain transparent.
    # Little feet: silhouettes and warm highlights.
    for lx in (32,41,55,64):
        d.rect(lx+lean,54+bob,5,10,'body',stroke=1)
        d.r(lx+lean+1,61+bob,3,2,C['shadow'])
    # Waving arms: short, squared stub claws consistent with the official mascot's shape.
    wave = kind in ('wave','yay','dance','hug','love')
    lift = round(5*max(0,math.sin(t))) if wave else 0
    lift_left = round(4*max(0,math.sin(t+1))) if kind in ('yay','dance','hug') else 0
    d.rect(18+lean,40+bob-lift_left,11,10,'body',stroke=2)
    d.rect(67+lean,40+bob-lift,11,10,'body',stroke=2)
    d.r(20+lean,42+bob-lift_left,7,3,C['light'])
    d.r(70+lean,42+bob-lift,6,3,C['light'])
    # Main body: outline + darker lower edge, a silhouette shared by every animation.
    d.rect(x,y,40,28,'body',stroke=2)
    d.r(x+2,y+2,36,5,C['light'])
    d.r(x+4,y+2,22,2,C['shine'])
    d.r(x+4,y+7,4,1,C['light'])
    d.r(x+2,y+22,36,4,C['shadow'])
    d.r(x+3,y+26,34,2,C['deep'])
    d.r(x+37,y+4,3,13,C['shadow'])
    # Face with intentional emotion-specific eye language.
    ex = kind
    if ex == 'sleep':
        for eyex in (37,55): d.r(eyex+lean,42+bob,5,2,C['ink'])
    elif ex == 'angry':
        for eyex in (37,55): d.r(eyex+lean,43+bob,5,4,C['ink'])
        d.r(36+lean,39+bob,7,2,C['ink']); d.r(54+lean,39+bob,7,2,C['ink'])
        d.r(37+lean,38+bob,2,2,C['ink']); d.r(59+lean,38+bob,2,2,C['ink'])
    elif ex == 'love':
        d.r(36+lean,42+bob,6,4,C['pink']); d.r(54+lean,42+bob,6,4,C['pink'])
        d.r(38+lean,40+bob,2,3,C['pink_hi']); d.r(56+lean,40+bob,2,3,C['pink_hi'])
    elif ex in ('yay','hug') and math.sin(t)>0.0:
        for eyex in (37,55):
            d.r(eyex+lean,43+bob,5,2,C['ink']); d.r(eyex+lean+1,42+bob,3,1,C['ink'])
    elif ex=='cry':
        for eyex in (37,55):
            d.r(eyex+lean,41+bob,5,2,C['ink']); d.r(eyex+lean,44+bob,4,2,C['ink'])
    elif ex=='wow':
        for eyex in (37,55):
            d.r(eyex+lean,39+bob,5,8,C['ink']); d.r(eyex+lean+1,40+bob,1,2,C['cream'])
    elif ex=='think':
        d.r(37+lean,42+bob,5,5,C['ink']); d.r(55+lean,43+bob,5,3,C['ink'])
        d.r(39+lean,42+bob,1,2,C['cream'])
    elif ex=='dance' and math.sin(t)>0:
        d.r(37+lean,42+bob,5,2,C['ink']);d.r(55+lean,40+bob,4,6,C['ink'])
    else:
        for eyex in (37,55):
            d.r(eyex+lean,41+bob,4,6,C['ink'])
            d.r(eyex+lean+1,41+bob,1,2,C['cream'])
    # Tiny character detail, mouth only when expressive enough.
    if kind in ('wave','yay','hug','love','dance'):
        d.r(47+lean,51+bob,5,2,C['deep'])
        d.r(48+lean,52+bob,3,1,C['pink_hi'])
    if kind=='angry': d.r(47+lean,52+bob,5,2,C['deep'])
    if kind=='wow': d.r(47+lean,50+bob,4,6,C['ink'])
    if kind=='cry': d.r(47+lean,51+bob,4,3,C['ink'])
    if kind=='sleep': d.r(47+lean,50+bob,3,2,C['deep'])
    if kind=='think': d.r(48+lean,52+bob,4,1,C['deep'])
    # Rosy cheeks.
    if kind in ('love','hug','wave','yay'):
        d.r(33+lean,50+bob,3,2,C['pink_hi']); d.r(61+lean,50+bob,3,2,C['pink_hi'])
    return x,y


def draw_frame(kind, k):
    t=2*math.pi*k/FRAMES
    s=math.sin(t); a=abs(s)
    im=Image.new('RGBA',(W,W),(0,0,0,0))
    d=Draw(im)
    bob=round(-2*(s+1)/2) if kind in ('wave','love','think','coffee','typing','hug') else round(-4*max(0,s))
    lean=round(2*math.sin(t)) if kind=='dance' else 0
    if kind=='cry': lean = round(math.sin(4*t))
    if kind=='angry': lean = round(math.sin(4*t))
    if kind=='wow': bob=round(-3*max(0,math.sin(t)))

    # Rear scene: particle trails / thematic motifs behind character.
    if kind=='wave':
        if math.sin(t)>-0.7:
            star(d,84,26-round(2*math.sin(t)),'gold',3)
            if math.sin(2*t)>0.5: star(d,77,17,'gold',2)
    if kind=='yay':
        rng=random.Random(73)
        for n in range(22):
            xx=rng.randint(10,86); yy=8+(rng.randint(-15,32)+k*64/FRAMES)%64
            if abs(xx-48)>20 or yy<27:
                d.r(xx, yy, 2, 3, C[['gold','pink','mint','purple'][n%4]])
    if kind=='love':
        for n in range(3):
            phase=((k/FRAMES+n/3)%1)*16
            heart(d, 69+n*6-((phase//5)%3)*2, 23-phase,1, 'pink' if n%2==0 else 'pink_hi')
    if kind=='think':
        bubble(d,78,19-2*max(0,s))
        d.r(81,20-2*max(0,s),3,2,C['ink'])
        d.r(83,22-2*max(0,s),2,2,C['ink'])
        d.r(82,25-2*max(0,s),2,2,C['ink'])
        d.r(74,32,2,2,C['cream']);d.r(70,35,2,2,C['cream'])
    if kind=='sleep':
        # Night sky accents, pulsing Zs, crescent moon.
        d.r(78,19,7,7,C['gold']);d.r(81,16,7,7,(0,0,0,0))
        for i in range(3):
            xx=65+i*7; yy=33-i*9-round(1+math.sin(t+i))
            d.r(xx,yy,5,2,C['purple']);d.r(xx+3,yy+2,2,2,C['purple']);d.r(xx,yy+4,5,2,C['purple'])
    if kind=='angry':
        for x in (18,72):
            if math.sin(2*t)>-0.7:
                d.r(x,27-round(2*(1+math.sin(2*t))),4,8,C['red'])
                d.r(x+1,23-round(2*(1+math.sin(2*t))),2,4,C['gold'])
    if kind=='wow':
        for x in (18,77):
            star(d,x,23+round(math.sin(2*t)),'gold',4)
        d.r(81,10,3,11,C['red']);d.r(81,24,3,3,C['red'])
    if kind=='coffee':
        for i in range(3):
            xx=74+i*4; yy=19-round(3*math.sin(t+i*2*math.pi/3))
            d.r(xx,yy,2,5,C['steam'])
            d.r(xx+1,yy-3,2,2,C['white'])
    if kind=='dance':
        for x in (15,77): star(d,x,29+round(3*s),'gold',3)
        for i in range(3):
            x=73+5*i; y=18+(i%2)*5-round(2+2*math.sin(t+i))
            d.r(x,y,3,3,C['purple']); d.r(x+2,y-7,2,10,C['purple'])
    if kind=='hug':
        if math.sin(t)>-0.7:
            star(d,18,19,'gold',2);star(d,78,19,'gold',2)

    body(d,t,kind,bob,lean)
    # Front accessories with pixel-art highlights.
    if kind=='cry':
        # Tears must sit in front of the shell and the face, not disappear behind it.
        for xx in (38+lean,56+lean):
            d.r(xx,46+bob,3,10+round(1+math.sin(2*t)),C['blue'])
            d.r(xx,47+bob,1,5,C['blue_hi'])
            d.r(xx+round((1+math.sin(2*t))/2),60+bob+round(1+math.sin(2*t)),3,3,C['blue_hi'])
    if kind=='typing':
        # Laptop in front of character, screen pulses with code bars.
        d.rect(25,49+bob,46,25,'darkblue',stroke=2)
        d.r(29,53+bob,38,15,C['screen'])
        d.r(32,56+bob,5+round(4.5*(1+math.sin(2*t))),2,C['mint'])
        d.r(32,62+bob,12,2,C['gold'])
        d.r(46,62+bob,7+round(3*(1+math.sin(2*t))),2,C['mint'])
        d.rect(21,72+bob,54,4,'deep',stroke=1)
        for x in (29,40,51,62):d.r(x,73+bob,6,1,C['shine'])
        if math.sin(4*t)>0:
            d.r(19,44+bob,4,4,C['light']);d.r(73,44+bob,4,4,C['light'])
        star(d,77,26, 'mint', 2)
    if kind=='coffee':
        # Cream ceramic mug and tiny heart logo.
        d.rect(66,48+bob,17,14,'cream',stroke=2)
        d.r(83,52+bob,6,7,C['outline']);d.r(84,53+bob,4,4,C['cream'])
        heart(d,70,52+bob,1,'pink')
        d.r(69,48+bob,12,2,C['gold'])
    if kind=='hug':
        heartbeat=2 if math.sin(t)>0 else 1
        heart(d,42-heartbeat*4,52+bob,heartbeat,'pink')
    if kind=='love':
        heart(d,44,54+bob,1,'pink')
    if kind=='dance':
        # Headphones over the crab, animated ear pads.
        d.r(32+lean,27+bob,32,3,C['purple'])
        d.r(29+lean,30+bob,5,10,C['purple'])
        d.r(63+lean,30+bob,5,10,C['purple'])
        d.r(30+lean,31+bob,2,7,C['cream'])
        d.r(65+lean,31+bob,2,7,C['cream'])
    if kind=='sleep':
        # Little nightcap / tassel: simple enough not to change species.
        d.r(30,29+bob,35,2,C['cream']);d.r(36,22+bob,23,7,C['purple'])
        d.r(55,20+bob,5,4,C['purple']);d.r(60,19+bob,4,4,C['gold'])
    if kind=='angry':
        d.r(17,50+bob,9,3,C['deep']);d.r(72,50+bob,9,3,C['deep'])
    if kind=='yay':
        star(d,84,17, 'gold', 4)

    # A periodic shell glint returns smoothly to its starting position.
    d.r(40 + round(7*math.sin(t)), 36+bob, 1, 1, C['shine'])

    # Fixed color index palette ensures GIF transparency and smooth transitions.
    p=Image.new('P',(W,W),0)
    p.putpalette(PALETTE)
    mapped=[]
    rgba=im.getdata()
    for rr,gg,bb,aa in rgba:
        mapped.append(INDEX.get((rr,gg,bb),0) if aa>127 else 0)
    p.putdata(mapped)
    p.info['transparency']=0
    return p


def render_set():
    previews=[]
    for slug,label,zh in SETS:
        frames=[draw_frame(slug,k) for k in range(FRAMES)]
        # Store at the authentic native-pixel resolution to keep them sharp and lightweight.
        path=GIFS/f'{slug}.gif'
        frames[0].save(path,save_all=True,append_images=frames[1:],duration=MS,loop=0,
                       transparency=0,disposal=2,optimize=False)
        # Explicit alpha keeps the poster background transparent.
        rgba=Image.new('RGBA',(W,W),(0,0,0,0))
        pal=frames[5].getpalette()
        rgba.putdata([(*pal[i*3:i*3+3],255) if i else (0,0,0,0) for i in frames[5].getdata()])
        rgba=rgba.resize((W*SCALE,W*SCALE),Image.Resampling.NEAREST)
        rgba.save(PNGS/f'{slug}.png', optimize=True)
        previews.append((slug,zh,rgba))
        print(f'{slug:8} {path.stat().st_size/1024:.1f}KB | {FRAMES} frames')
    # High-res preview sheet with a harmonious background; stickers themselves stay transparent.
    cell=392; columns=4; rows=3
    sheet=Image.new('RGB',(columns*cell,rows*cell),(248,244,238))
    draw=ImageDraw.Draw(sheet)
    for idx,(slug,zh,rgba) in enumerate(previews):
        i=idx%columns; j=idx//columns; cx=i*cell; cy=j*cell
        draw.rounded_rectangle((cx+12,cy+12,cx+cell-12,cy+cell-12),radius=22,
                               fill=(255,252,248),outline=(233,222,210),width=2)
        # checkerboard underlay hints that stickers have transparent backgrounds
        for yy in range(8):
            for xx in range(8):
                if (xx+yy)%2==0:
                    draw.rectangle((cx+42+xx*38,cy+32+yy*38,cx+42+(xx+1)*38-1,cy+32+(yy+1)*38-1),fill=(251,248,245))
        piece=rgba.resize((342,342),Image.Resampling.NEAREST)
        sheet.paste(piece,(cx+25,cy+23),piece)
        try:
            font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',19)
        except OSError: font=ImageFont.load_default()
        draw.text((cx+24,cy+350),slug.upper(),font=font,fill=(93,72,67))
    sheet.save(PREVIEW/'contact-sheet.png',optimize=True)
    print('Preview:',PREVIEW/'contact-sheet.png')

if __name__=='__main__': render_set()
