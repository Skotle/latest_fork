"""Render articulated source geometry and poses; not a Minecraft screenshot."""
import json, math
from PIL import Image, ImageDraw, ImageFont
from build import RP, OUT, NS
from motion import MODES, FRAMES, poses

FONT='C:/Windows/Fonts/malgun.ttf'
PALETTE=['#242337','#827657','#d7c68b','#95e4ee']
LABELS={'idle':'대기 · 호흡','walk':'추격 · 교차 보행','wind':'종을 들어 공격 준비','impact':'종 내려치기','recover':'공격 후 회복','dash':'직선 돌진','stagger':'균형 붕괴 · 심장 노출','ritual':'봉인 의식 · 개기일식'}
def text(draw,x,y,s,size=22,color='#d9e0eb'):draw.text((x,y),s,font=ImageFont.truetype(FONT,size),fill=color)
def rotate(v,q):
    x,y,z,w=q;vx,vy,vz=v
    tx=2*(y*vz-z*vy);ty=2*(z*vx-x*vz);tz=2*(x*vy-y*vx)
    return [vx+w*tx+y*tz-z*ty,vy+w*ty+z*tx-x*tz,vz+w*tz+x*ty-y*tx]
MODELS={n:json.loads((RP/f'assets/{NS}/models/{n}.json').read_text()) for n in poses('idle',0)}
def render_boss(draw,mode,frame,cx=350,ground=690,size=115):
    def project(p):
        x,y,z=p;return cx+(x-z*.48)*size,ground-y*size+z*size*.2
    draw.ellipse((cx-125,ground-14,cx+125,ground+22),fill='#131925')
    faces=[]
    for name,tr in poses(mode,frame).items():
        for e in MODELS[name]['elements']:
            lo=[(v-8)/16 for v in e['from']];hi=[(v-8)/16 for v in e['to']]
            x,y,z=lo;X,Y,Z=hi
            quads=[[(x,y,z),(X,y,z),(X,Y,z),(x,Y,z)],[(X,y,z),(X,y,Z),(X,Y,Z),(X,Y,z)],
                   [(x,Y,z),(X,Y,z),(X,Y,Z),(x,Y,Z)],[(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)],
                   [(x,y,z),(x,y,Z),(x,Y,Z),(x,Y,z)],[(x,y,z),(X,y,z),(X,y,Z),(x,y,Z)]]
            material=int(e['faces']['north']['uv'][0]/4)
            for k,verts in enumerate(quads):
                vertices=[]
                for v in verts:
                    p=rotate([a*b for a,b in zip(v,tr['scale'])],tr['left_rotation'])
                    vertices.append([a+b for a,b in zip(p,tr['translation'])])
                depth=sum(p[2]+p[0]*.48 for p in vertices)/4
                rgb=tuple(int(PALETTE[material][i:i+2],16) for i in (1,3,5));shade=[1,.65,1.15,.75,.8,.55][k]
                color=tuple(min(255,int(c*shade)) for c in rgb)
                faces.append((depth,[project(p) for p in vertices],color))
    for _,poly,color in sorted(faces,reverse=True):draw.polygon(poly,fill=color,outline='#101521')
def main():
    OUT.mkdir(exist_ok=True)
    im=Image.new('RGB',(1440,900),'#101521');d=ImageDraw.Draw(im)
    text(d,48,32,'일식의 종지기, 녹스 · v2',38,'#e8d49b')
    text(d,50,86,'생성된 관절 모델·구조물 미리보기 · Minecraft 게임 화면 아님',19,'#95a6be')
    d.rounded_rectangle((40,130,690,800),24,fill='#1c2332');d.rounded_rectangle((710,130,1400,800),24,fill='#1c2332')
    text(d,74,151,'10개 관절 · 종 내려치기 준비',25,'#e8d49b')
    render_boss(d,'wind',12,350,690,105)
    text(d,78,735,'보행 · 2연격 · 돌진 · 휘청임 · 심장 노출',20)
    cx,cy,u=1055,440,7.4
    def point(x,z):return cx+x*u,cy+z*u
    for i in range(4):
        rect=[(-5,23),(5,23),(5,34),(-5,34)]
        for _ in range(i):rect=[(-z,x) for x,z in rect]
        d.polygon([point(x,z) for x,z in rect],fill='#48443a',outline='#d7c68b')
    for r,color in [(25.5,'#645c49'),(23,'#303a4b'),(17,'#263141'),(7,'#3e3e4a')]:
        d.ellipse((cx-r*u,cy-r*u,cx+r*u,cy+r*u),fill=color,outline='#92856d',width=2)
    sector=[(cx,cy)]+[point(math.cos(math.radians(a))*23,math.sin(math.radians(a))*23) for a in range(-22,23,2)]
    d.polygon(sector,fill='#346b70')
    for i,(x,z) in enumerate([(0,-20),(-17,10),(17,10)],1):
        px,py=point(x,z);d.ellipse((px-15,py-15,px+15,py+15),fill='#d7c68b');text(d,px-6,py-12,str(i),18,'#171a22')
    d.ellipse((cx-15,cy-15,cx+15,cy+15),fill='#d7c68b')
    text(d,756,151,'지하 일식 관측소 · 자연 생성',25,'#e8d49b')
    text(d,756,199,'전투장 Y -45 ~ -21 · 새 오버월드 청크',19,'#95a6be')
    text(d,752,745,'지름 49 · 4방향 진입 · 봉인종 1 → 3 → 2',20)
    text(d,50,827,'독립 데이터팩 + 기존 리소스팩 확장 합본 / Java 26.3 / 솔로·파티 공략',22,'#d7c68b')
    im.save(OUT/'Nox-Preview.png')
    frames=[]
    for mode in MODES:
        for i in range(FRAMES):
            frame=Image.new('RGB',(720,760),'#101521');draw=ImageDraw.Draw(frame)
            text(draw,32,24,'녹스 v2 · 관절 모션',28,'#e8d49b')
            text(draw,32,69,LABELS[mode],22,'#95e4ee')
            render_boss(draw,mode,i,360,665,125)
            text(draw,32,708,'생성 모델의 소프트웨어 렌더링 · 게임 화면 아님',17,'#95a6be')
            frames.append(frame)
    frames[0].save(OUT/'Nox-Motion-Preview.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False)
    print('Rendered static preview and 128-frame animated preview.')
if __name__=='__main__':main()
