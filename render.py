#!/usr/bin/env python3
"""Original flat pixel fan art; deterministic 48-frame scene loops. python render.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
ROOT=Path(__file__).resolve().parent
W,SCALE,FRAMES,MS=128,4,48,80
SETS=[('wave','Hello','探头打招呼'),('yay','Yay!','开心蹦蹦'),('love','Love','偷偷比心'),('typing','Deadline','深夜赶工'),('think','Thinking','灵感来了'),('sleep','Good night','裹被睡觉'),('cry','Sad','哭成小水洼'),('angry','Angry','气到冒烟'),('wow','Wow','吓到后退'),('coffee','Coffee','咖啡续命'),('dance','Dance','耳机小舞步'),('hug','Hug','给你抱抱'),('bubbles','Bubbles','午后吹泡泡'),('rain','Rainy day','雨天等你'),('gift','For you','礼物送给你'),('garden','Gardening','浇花小能手'),('noodles','Noodle break','嗦面暂停中'),('kite','Windy day','去放风筝'),('read','Reading','窝着看书'),('toast','Breakfast','早餐烤吐司'),('camp','Camping','星空小露营'),('paint','Painting','画一朵小花'),('scooter','On my way','滑板出发啦'),('bath','Bath time','泡个热水澡')]
C={'orange':'#D98263','dark':'#AB644F','ink':'#292522','cheek':'#EBA48F','cream':'#FFF2D8','yellow':'#F5CA69','pink':'#EAA0A7','blue':'#9ABCC6','water':'#B9D5D9','green':'#94AF8B','leaf':'#698B67','purple':'#B1A6C7','wood':'#BD9479','brown':'#795F53','white':'#FFFFFF','pale':'#E5DACA','night':'#57657A'}
COLORS=[(0,0,0)]+[tuple(bytes.fromhex(v[1:])) for v in C.values()]
PALETTE=[v for c in COLORS for v in c]+[0]*(768-3*len(COLORS));INDEX={v:i for i,v in enumerate(COLORS)}
class Pen:
 def __init__(self,im): self.d=ImageDraw.Draw(im)
 def r(self,x,y,w,h,c):
  x,y,w,h=map(round,(x,y,w,h))
  if w>0 and h>0:self.d.rectangle((x,y,x+w-1,y+h-1),fill=C.get(c,c))
 def line(self,pts,c='brown',width=1):self.d.line([(round(x),round(y)) for x,y in pts],fill=C[c],width=width)
 def ellipse(self,x,y,w,h,c):self.d.ellipse((round(x),round(y),round(x+w-1),round(y+h-1)),fill=C[c])
 def ring(self,x,y,r,c='water'):
  # Deliberate stepped circle instead of antialiased edges.
  self.line([(x-r+2,y-r),(x+r-2,y-r),(x+r,y-r+2),(x+r,y+r-2),(x+r-2,y+r),(x-r+2,y+r),(x-r,y+r-2),(x-r,y-r+2),(x-r+2,y-r)],c)
def heart(d,x,y,s=1):
 for j,row in enumerate(['.##.##.','#######','#######','.#####.','..###..','...#...']):
  for i,v in enumerate(row):
   if v=='#':d.r(x+i*s,y+j*s,s,s,'pink')
def star(d,x,y,s=2,c='yellow'):
 d.r(x-s,y,2*s+1,1,c);d.r(x,y-s,1,2*s+1,c)
def closed(d,x,y):d.line([(x,y+2),(x+2,y),(x+4,y+2)],'ink',2)
def crab(d,x,y,t,mood='normal',arms='normal'):
 # Reference-inspired flat rectangle, four skinny feet, simple eyes; no shell or outline.
 d.r(x,y,36,27,'orange')
 for i in (0,9,24,33):d.r(x+i,y+26,3,9,'orange')
 lift=round(3*math.sin(t))
 d.r(x-8,y+12-(lift if arms=='open' else 0),8,5,'orange')
 d.r(x+36,y+12-(5+lift if arms=='wave' else lift if arms=='open' else 0),8,5,'orange')
 if mood in ('happy','sleep'):
  for xx in (x+6,x+26):
   if mood=='sleep':d.r(xx,y+10,5,2,'dark')
   else:closed(d,xx,y+8)
 elif mood=='love':
  heart(d,x+4,y+7);heart(d,x+25,y+7)
 elif mood=='sad':
  for xx in (x+6,x+26):
   d.r(xx,y+6,4,8,'ink');d.r(xx+1,y+7,1,2,'white');d.r(xx,y+13,4,4,'water')
 elif mood=='wow':
  for xx in (x+6,x+26):d.r(xx,y+6,4,8,'ink')
  d.r(x+16,y+18,4,5,'dark')
 else:
  blink=math.cos(t)>.985
  for xx in (x+6,x+26):d.r(xx,y+8,4,1 if blink else 4,'ink')
  if mood=='angry':
   d.line([(x+5,y+4),(x+11,y+7)],'dark',2);d.line([(x+25,y+7),(x+31,y+4)],'dark',2)
 if mood in ('happy','sad','love'):
  d.r(x+3,y+18,4,2,'cheek');d.r(x+29,y+18,4,2,'cheek')
 if mood=='happy':d.line([(x+15,y+18),(x+15,y+21),(x+20,y+21),(x+20,y+18)],'dark')
def plant(d,x,y,flower=False):
 d.r(x,y,12,10,'wood');d.r(x-1,y,14,3,'brown');d.r(x+5,y-17,2,17,'leaf')
 d.r(x,y-10,6,4,'green');d.r(x+7,y-15,6,4,'green')
 if flower:
  d.r(x+2,y-23,8,10,'pink');d.r(x,y-21,12,6,'pink');d.r(x+4,y-20,4,4,'yellow')
def mug(d,x,y):
 d.r(x,y,13,13,'cream');d.r(x+13,y+3,5,7,'cream');d.r(x+13,y+5,3,3,'brown');d.r(x+2,y,9,2,'brown');heart(d,x+3,y+5)
def frame(slug,k):
 t=math.tau*k/FRAMES;s=math.sin(t);c=math.cos(t);im=Image.new('RGBA',(W,W));d=Pen(im)
 x,y=46,53+round(s)
 happy=slug in ('yay','dance','hug','bubbles','gift','garden','kite','toast','camp','paint','scooter','bath')
 mood='happy' if happy else {'cry':'sad','love':'love','angry':'angry','wow':'wow','sleep':'sleep'}.get(slug,'normal')
 if slug=='yay':y-=round(6*(1-c))
 if slug=='dance':x+=round(4*s);y-=round(2*(1-math.cos(2*t)))
 if slug=='wow':x+=round(3*(1-c))
 # Scenery behind the actor. Keep empty space transparent, even in scene stickers.
 if slug in ('typing','coffee','noodles','toast','paint','read'):
  d.r(22,94,85,4,'wood');d.r(28,98,3,15,'wood');d.r(99,98,3,15,'wood')
 if slug=='typing':
  d.r(92,21,15,14,'night');d.r(94,23,11,10,'cream');d.r(99,25,1,5,'brown');d.r(99,29,4,1,'brown')
  plant(d,18,84)
 if slug=='sleep':
  d.r(20,81,90,20,'wood');d.r(20,62,4,44,'wood');d.r(106,75,4,31,'wood');d.r(24,77,82,8,'cream');d.r(28,65,24,13,'cream')
  x,y=47,49+round(s)
 if slug=='rain':
  d.r(19,103,88,2,'water')
  for i in range(9):
   xx=18+i*11;yy=24+((k/FRAMES*66+i*13)%66);d.r(xx,yy,1,4,'blue')
 if slug=='garden':plant(d,89,90,True);d.r(15,105,96,2,'green');x=31
 if slug=='kite':
  x=35;d.line([(75,67),(89+3*s,41),(94+3*s,24)],'pale');d.line([(94+3*s,24),(91+3*s,34),(98+3*s,40),(95+3*s,47)],'pink')
  d.line([(84+3*s,19),(94+3*s,9),(104+3*s,19),(94+3*s,29),(84+3*s,19)],'yellow',2);d.r(91+3*s,15,7,9,'yellow')
  for i in range(3):d.line([(13,25+i*12),(25,25+i*12)],'water')
 if slug=='camp':
  d.line([(15,95),(36,48),(58,95),(15,95)],'green',3);d.line([(26,94),(36,69),(47,94)],'cream',2)
  x=66;y=64+round(s)
  for xx,yy in [(20,22),(48,16),(80,25),(107,17)]:star(d,xx,yy,1 if s>0 else 2,'yellow')
  d.r(93,30,10,10,'cream');d.r(97,28,8,8,(0,0,0,0))
 if slug=='scooter':x+=round(3*s);y=49+round(math.sin(2*t));d.r(21,105,85,1,'pale')
 if slug=='bath':
  for i in range(4):d.r(35+i*16,27+round(3*math.sin(t+i)),2,7,'water')
 crab(d,x,y,t,mood,'wave' if slug=='wave' else 'open' if slug in ('yay','hug') else 'normal')
 if slug=='wave':
  for i in range(2):d.line([(93+i*6,48),(95+i*6,43),(94+i*6,38)],'yellow')
 if slug=='yay':
  for i in range(8):
   a=i*math.tau/8;rr=25+4*s;star(d,64+rr*math.cos(a),54+rr*math.sin(a),1,'yellow' if i%2 else 'pink')
 if slug=='love':
  for i in range(3):heart(d,30+i*30,29+round(3*math.sin(t+i)))
 if slug=='typing':
  d.r(35,73,51,22,'night');d.r(38,76,45,15,'blue');d.r(31,95,59,3,'brown')
  for i in range(3):d.r(42,79+i*4,10+round(4*(1+math.sin(t+i))),1,'cream')
  for xx in (31,86):d.r(xx,77+round(2*math.sin(3*t+(xx%2))),6,4,'orange')
 if slug=='think':
  d.r(86,37,2,2,'pale');d.r(90,31,3,3,'pale');d.r(94,15+round(s),10,11,'yellow');d.r(97,26+round(s),4,3,'brown')
  for xx,yy in [(89,17),(108,17),(99,9)]:star(d,xx,yy,1)
 if slug=='sleep':
  d.r(40,72+round(s),62,13,'purple');d.r(40,84,62,12,'purple')
  for i in range(3):
   xx=77+9*i;yy=41-10*i+round(2*math.sin(t+i));d.line([(xx,yy),(xx+5,yy),(xx,yy+5),(xx+5,yy+5)],'blue')
 if slug=='cry':
  d.ellipse(35,91,57,5,'water')
  for xx in (x+6,x+26):
   d.r(xx,y+17,3,12,'water');d.r(xx,87+round(2*math.sin(2*t)),3,3,'blue')
 if slug=='angry':
  for i in range(3):
   xx=45+i*16;yy=31+round(3*math.sin(t+i));d.r(xx,yy,6,4,'pale');d.r(xx+2,yy-4,6,4,'pale')
 if slug=='wow':
  for xx in (28,100):d.r(xx,43,2,10,'yellow');d.r(xx,57,2,2,'yellow')
 if slug=='coffee':
  mug(d,77,77);d.r(71,81,8,4,'orange');d.r(30,91,23,2,'cream')
  for i in range(2):d.line([(83+i*6,71),(81+i*6+round(s),66),(83+i*6,61)],'pale')
 if slug=='dance':
  d.r(x+3,y-5,30,3,'purple');d.r(x,y-2,4,15,'purple');d.r(x+32,y-2,4,15,'purple')
  for i in range(2):
   xx=22+i*78;yy=38+round(4*math.sin(t+i));d.r(xx,yy,5,3,'blue');d.r(xx+4,yy-10,2,12,'blue');d.r(xx+5,yy-10,5,2,'blue')
 if slug=='hug':
  heart(d,53,72+round(s),3);d.r(49,77+round(s),7,4,'orange');d.r(74,77+round(s),7,4,'orange')
 if slug=='bubbles':
  d.r(82,66,12,2,'brown');d.r(92,62,2,10,'brown');d.r(94,60,5,2,'brown');d.r(94,72,5,2,'brown');d.r(99,62,2,10,'brown')
  for i in range(3):
   phase=(k/FRAMES+i/3)%1;xx=90+15*phase;yy=51-32*phase;rr=3+round(phase*3)
   d.ring(xx,yy,rr);d.r(xx-rr+2,yy-rr+2,2,1,'white')
 if slug=='rain':
  # Umbrella moves with the actor; rain is occluded by the canopy.
  d.r(37,34,57,3,'purple');d.r(42,29,47,5,'purple');d.r(49,25,33,4,'purple');d.r(60,22,12,3,'purple')
  d.r(65,37,2,26,'brown');d.line([(65,63),(65,69),(70,69),(70,66)],'brown',2)
 if slug=='gift':
  d.r(47,77,34,23,'pink');d.r(44,73+round(2*s),40,6,'pink');d.r(62,74,5,26,'cream')
  d.line([(64,73),(54,66),(53,71),(64,73),(73,65),(76,70),(64,73)],'cream',2)
  star(d,32,50,2);star(d,95,57,2)
 if slug=='garden':
  d.r(65,74,17,11,'blue');d.r(79,71,10,3,'blue');d.r(87,69,3,5,'blue');d.ring(66,75,5,'blue')
  for i in range(3):d.r(88+i*3,77+((k/FRAMES*12+i*4)%12),1,2,'water')
 if slug=='noodles':
  d.r(44,86,40,5,'cream');d.r(48,91,32,7,'cream');d.r(54,98,20,3,'blue');d.r(46,85,36,2,'yellow')
  d.line([(83,69),(91,83)],'wood',2);d.line([(79,70),(87,84)],'wood',2)
  for i in range(3):d.line([(66+i*2,78+2*s),(65+i*2,82),(66+i*2,86)],'yellow')
 if slug=='read':
  d.line([(38,78),(63,84),(63,103),(38,96),(38,78)],'green',2);d.line([(63,84),(89,78),(89,96),(63,103)],'green',2)
  for i in range(3):d.line([(43,84+i*4),(57,88+i*4)],'cream');d.line([(69,88+i*4),(83,84+i*4)],'cream')
  d.line([(64,84),(67+8*(1-c)/2,78),(67+8*(1-c)/2,94),(64,101)],'cream')
 if slug=='toast':
  d.r(76,80,23,15,'blue');d.r(74,94,27,3,'brown');yy=73-round(5*(1-c)/2)
  d.r(79,yy,16,12,'wood');d.r(81,yy+2,12,8,'cream');d.r(83,yy+4,5,4,'yellow');d.r(78,88,19,2,'night')
 if slug=='camp':
  d.line([(55,104),(74,108),(55,108),(74,104)],'brown',2)
  d.r(61,97,7,9,'yellow');d.r(63,91+round(2*s),4,10,'orange');d.r(64,100,3,6,'cream')
  d.line([(83,78),(71,93)],'wood');d.r(71,87,5,5,'cream')
 if slug=='paint':
  d.r(83,60,23,31,'cream');d.line([(86,91),(83,108),(103,108),(100,91)],'wood',2)
  d.r(94,74,1,12,'leaf');heart(d,91,68);d.r(89,78,5,2,'green')
  d.line([(77,78+2*s),(92,71+2*s)],'brown',2);d.r(90,70+2*s,3,3,'pink');d.ellipse(24,88,16,5,'wood')
 if slug=='scooter':
  d.r(34+3*s,87,60,3,'purple');d.ellipse(42+3*s,90,7,7,'ink');d.ellipse(80+3*s,90,7,7,'ink')
  for i in range(3):d.r(17+i*3,69+i*10,9,1,'pale')
 if slug=='bath':
  d.r(27,78,76,5,'cream');d.r(31,83,68,19,'blue');d.r(38,102,5,4,'wood');d.r(86,102,5,4,'wood')
  for i in range(10):d.r(32+i*7,75+round(2*math.sin(t+i)),6,5,'cream')
  d.r(88,70+round(s),10,7,'yellow');d.r(94,66+round(s),5,5,'yellow');d.r(98,69+round(s),3,2,'orange');d.r(96,67+round(s),1,1,'ink')
 p=Image.new('P',(W,W));p.putpalette(PALETTE);p.putdata([INDEX.get(rgb[:3],0) if rgb[3] else 0 for rgb in im.getdata()]);p.info['transparency']=0
 return p

def render_set():
 for folder in ('gifs','png','preview'):(ROOT/folder).mkdir(exist_ok=True)
 previews=[]
 for slug,en,zh in SETS:
  frames=[frame(slug,k) for k in range(FRAMES)]
  frames[0].save(ROOT/'gifs'/f'{slug}.gif',save_all=True,append_images=frames[1:],duration=MS,loop=0,transparency=0,disposal=2,optimize=False)
  poster=frames[12].convert('RGBA').resize((W*SCALE,W*SCALE),Image.Resampling.NEAREST);poster.save(ROOT/'png'/f'{slug}.png',optimize=True);previews.append((slug,poster))
  print(slug)
 cell=256;sheet=Image.new('RGB',(cell*6,cell*4),'#faf7f2');d=ImageDraw.Draw(sheet)
 for i,(slug,poster) in enumerate(previews):
  x=i%6*cell;y=i//6*cell;d.rounded_rectangle((x+6,y+6,x+250,y+250),12,fill='#f0ece5')
  piece=poster.resize((240,240),Image.Resampling.NEAREST);sheet.paste(piece,(x+8,y-4),piece);d.text((x+16,y+230),slug.upper(),fill='#795f53')
 sheet.save(ROOT/'preview/contact-sheet.png')
if __name__=='__main__':render_set()
