"""Render the generated cuboid geometry, not concept art or game screenshots."""
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from boss_visuals import transform, BASE, RESOURCE, OUTPUT

ROSTER=json.loads((OUTPUT/'boss-model-roster.json').read_text(encoding='utf-8'))['bosses']
FONT_PATH='C:/Windows/Fonts/malgun.ttf'
def font(size):return ImageFont.truetype(FONT_PATH,size)
def rotate(p,q):
 x,y,z,w=q
 return [
  (1-2*y*y-2*z*z)*p[0]+(2*x*y-2*z*w)*p[1]+(2*x*z+2*y*w)*p[2],
  (2*x*y+2*z*w)*p[0]+(1-2*x*x-2*z*z)*p[1]+(2*y*z-2*x*w)*p[2],
  (2*x*z-2*y*w)*p[0]+(2*y*z+2*x*w)*p[1]+(1-2*x*x-2*y*y)*p[2]]
FACES=[((0,0,-1),(0,3,2,1)),((0,0,1),(4,5,6,7)),((-1,0,0),(0,4,7,3)),((1,0,0),(1,2,6,5)),((0,-1,0),(0,1,5,4)),((0,1,0),(3,7,6,2))]
CAM=[.548,.329,-.768]
LIGHT=[-.2,.8,-.55]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def render(boss,width,height,pose='idle',frame=0,phase=1):
 image=Image.new('RGB',(width,height),'#111d2a');draw=ImageDraw.Draw(image)
 polygons=[]
 atlas=Image.open(RESOURCE/f'assets/ida_boss/textures/boss/{boss["id"]}.png').convert('RGB')
 for part in boss['parts']:
  tr=transform(part,frame,pose,phase);q=tr['left_rotation']
  for cube in part['cubes']:
   c,size=cube['center'],cube['size'];xs=[c[0]-size[0]/2,c[0]+size[0]/2];ys=[c[1]-size[1]/2,c[1]+size[1]/2];zs=[c[2]-size[2]/2,c[2]+size[2]/2]
   vertices=[(xs[0],ys[0],zs[0]),(xs[1],ys[0],zs[0]),(xs[1],ys[1],zs[0]),(xs[0],ys[1],zs[0]),(xs[0],ys[0],zs[1]),(xs[1],ys[0],zs[1]),(xs[1],ys[1],zs[1]),(xs[0],ys[1],zs[1])]
   vertices=[[v+t for v,t in zip(rotate([a*s for a,s in zip(v,tr['scale'])],q),tr['translation'])] for v in vertices]
   for normal,indices in FACES:
    n=rotate(normal,q)
    if dot(n,CAM)<=0:continue
    face=[vertices[i] for i in indices]
    shade=.78+max(0,dot(n,LIGHT))*.23
    if cube['material']==3:shade=1.06
    depth=sum(dot(p,CAM) for p in face)/4
    polygons.append((depth,face,cube['material'],shade))
 # Match a common world scale across silhouettes, allowing oversized wings.
 scale=min(width/4.4,height/3.65)
 ox=width/2;oy=height*.85
 def project(p):return (ox+(p[0]*.814+p[2]*.581)*scale,oy+(p[0]*.198-p[1]*.923-p[2]*.277)*scale)
 draw.ellipse((ox-scale*.85,oy-8,ox+scale*.85,oy+15),fill='#0a121b')
 for depth,face,mat,shade in sorted(polygons,key=lambda p:p[0]):
  # Texture samples on each face show the real palette/atlas pixel detail.
  for v in range(4):
   for u in range(4):
    points=[]
    for a,b in [(u/4,v/4),((u+1)/4,v/4),((u+1)/4,(v+1)/4),(u/4,(v+1)/4)]:
     p=[face[0][i]*(1-a)*(1-b)+face[1][i]*a*(1-b)+face[2][i]*a*b+face[3][i]*(1-a)*b for i in range(3)]
     points.append(project(p))
    color=atlas.getpixel((mat*16+u*4+2,v*4+2))
    color=tuple(min(255,int(c*shade)) for c in color)
    draw.polygon(points,fill=color)
 return image

def sheet(bosses,cols,tile_w,tile_h,title,subtitle,path):
 rows=math.ceil(len(bosses)/cols)
 image=Image.new('RGB',(cols*tile_w+48,rows*tile_h+150),'#0c1521');d=ImageDraw.Draw(image)
 d.text((28,22),title,font=font(30),fill='#eef5fc')
 d.text((28,70),subtitle,font=font(17),fill='#a6bacb')
 for i,b in enumerate(bosses):
  x=24+i%cols*tile_w;y=122+i//cols*tile_h
  model=render(b,tile_w-12,tile_h-62)
  image.paste(model,(x,y))
  d.text((x+12,y+tile_h-54),b['name'],font=font(17),fill='#e5edf3')
  d.text((x+12,y+tile_h-29),b['id']+'  ·  '+str(len(b['parts']))+' parts',font=font(12),fill='#7f9db4')
 image.save(path)

sheet(ROSTER,4,342,344,'IDA — 보스 전용 모델 22종','생성된 실제 모델 형상의 미리보기 · Minecraft 게임 화면은 아닙니다',OUTPUT/'boss-models-all.png')
featured=[next(b for b in ROSTER if b['id']==ident) for ident in ['kisegi_sanctuary','desert_hall','foundry','typhon']]
sheet(featured,4,360,390,'IDA — 보스 외형 개편','리소스팩 모델 + 데이터팩 관절 애니메이션 · 모드 / 플러그인 불필요',OUTPUT/'boss-models-preview.png')
frames=[]
for phase in [1,2]:
 for pose in ['idle','walk','wind','recover']:
  for frame in range(4):
   image=Image.new('RGB',(1000,370),'#0c1521');d=ImageDraw.Draw(image)
   for i,b in enumerate(featured):image.paste(render(b,250,305,pose,frame,phase),(i*250,35))
   d.text((20,7),f'관절 애니메이션 미리보기 · {phase}페이즈 · '+{'idle':'대기','walk':'이동','wind':'공격 준비','recover':'공격 후 빈틈'}[pose],font=font(17),fill='#e5edf3')
   for i,b in enumerate(featured):d.text((i*250+12,345),b['name'],font=font(14),fill='#a6bacb')
   frames.append(image)
frames[0].save(OUTPUT/'boss-model-animation.gif',save_all=True,append_images=frames[1:],duration=180,loop=0)
print('Rendered 22 models and 32 animation frames')
