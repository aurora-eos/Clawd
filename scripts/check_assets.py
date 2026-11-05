"""Validate every decoded frame, alpha channel and loop metadata."""
from pathlib import Path
from PIL import Image, ImageChops
import json
ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT))
from render import SETS, W, SCALE, FRAMES, MS
SLUGS = [item[0] for item in SETS]
rows=[]
assert {p.stem for p in (ROOT/'gifs').glob('*.gif')} == set(SLUGS)
assert {p.stem for p in (ROOT/'png').glob('*.png')} == set(SLUGS)
for slug in SLUGS:
    im=Image.open(ROOT/'gifs'/f'{slug}.gif')
    assert im.size==(W,W) and im.info['loop']==0
    frames=[]; duration=0
    for k in range(im.n_frames):
        im.seek(k)
        assert im.info['duration']%MS==0
        duration+=im.info['duration']
        f=im.convert('RGBA');alpha=f.getchannel('A')
        assert alpha.getextrema()==(0,255)
        box=alpha.getbbox()
        assert box and box[0]>0 and box[1]>0 and box[2]<W and box[3]<W
        frames.append(f.copy())
    assert duration==FRAMES*MS
    assert any(ImageChops.difference(frames[0],f).convert('RGB').getbbox() for f in frames[1:])
    png=Image.open(ROOT/'png'/f'{slug}.png')
    assert png.size==(W*SCALE,W*SCALE) and png.mode=='RGBA'
    assert png.getchannel('A').getextrema()==(0,255)
    def delta(a,b):
        return sum(x!=y for x,y in zip(a.getdata(),b.getdata()))
    changes=[delta(frames[i],frames[(i+1)%len(frames)]) for i in range(len(frames))]
    rows.append(dict(sticker=slug,encoded_frames=len(frames),duration_ms=duration,seam_changed_pixels=changes[-1],max_step_changed_pixels=max(changes),gif_bytes=(ROOT/'gifs'/f'{slug}.gif').stat().st_size))
print(json.dumps(rows,indent=2))
