"""Render the shipped JSON geometry, UV textures and joint transforms (not game footage)."""
import json, math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from build import RP,OUT
from cristiano_art import poses,MODES,FRAMES,rotate

ASSETS=RP/'assets/desert_ball'
LABELS=['대기','달리기','날강두 · 슈팅','젖통닌자 · 기습','노쇼',
        '꽃게 드리블','헤딩골','오버헤드킥','카운터 기절','시우 세리머니','착지·회복']
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',17)
big=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',24)
MODELS={p.stem:json.loads(p.read_text()) for p in (ASSETS/'models').glob('*.json')}
TEXTURES={p.stem:np.asarray(Image.open(p).convert('RGB')) for p in (ASSETS/'textures/entity').glob('*.png')}
FACES={'south':[4,5,6,7],'north':[1,0,3,2],'east':[5,1,2,6],
       'west':[0,4,7,3],'up':[7,6,2,3],'down':[0,1,5,4]}

def render(mode,frame,yaw=22,bare=False,width=340,height=385,scale=89,head_only=False):
    pixels=np.zeros((height,width,3),dtype=np.uint8);pixels[:]=[22,29,40]
    depth=np.full((height,width),-1e9,dtype=np.float64)
    a=math.radians(yaw);rx=np.array([math.cos(a),0,-math.sin(a)])
    cam=np.array([math.sin(a),.18,math.cos(a)]);cam/=np.linalg.norm(cam)
    up=np.cross(cam,rx)
    transforms=poses(mode,frame)
    for part,tr in transforms.items():
        if head_only:
            if part!='head':continue
            tr['translation']=[0,.12,0]
        if part=='ball' and mode in ['header','overhead','ninja']:continue
        name='ball' if part=='ball' else part
        if bare and part=='torso':name='bare'
        if bare and part.endswith('_arm'):name=part+'_bare'
        model=MODELS[name]
        for e in model['elements']:
            lo=np.array(e['from']);hi=np.array(e['to'])
            verts=np.array([[lo[0],lo[1],lo[2]],[hi[0],lo[1],lo[2]],
              [hi[0],hi[1],lo[2]],[lo[0],hi[1],lo[2]],
              [lo[0],lo[1],hi[2]],[hi[0],lo[1],hi[2]],
              [hi[0],hi[1],hi[2]],[lo[0],hi[1],hi[2]]])
            verts=(verts-8)/16*np.array(tr['scale'])
            verts=np.array([rotate(tr['left_rotation'],v) for v in verts])+np.array(tr['translation'])
            screen=np.column_stack([width/2+(verts@rx)*scale,height-28-(verts@up)*scale,verts@cam])
            for face,idx in FACES.items():
                vs=verts[idx];normal=np.cross(vs[1]-vs[0],vs[2]-vs[0]);normal/=np.linalg.norm(normal)
                if normal@cam<=0:continue
                data=e['faces'][face];u0,v0,u1,v1=data['uv']
                # Four UV corners match the face's lower-left to upper-left vertices.
                uv=np.array([[u0,v1],[u1,v1],[u1,v0],[u0,v0]])/16
                texkey=model['textures'][data['texture'][1:]].split('/')[-1]
                tex=TEXTURES[texkey];shade=.64+.36*max(0,normal@np.array([.35,.65,.68]))
                for tri in [(0,1,2),(0,2,3)]:
                    pts=screen[np.array(idx)[list(tri)]];tuv=uv[list(tri)]
                    x0=max(0,int(np.floor(pts[:,0].min())));x1=min(width-1,int(np.ceil(pts[:,0].max())))
                    y0=max(0,int(np.floor(pts[:,1].min())));y1=min(height-1,int(np.ceil(pts[:,1].max())))
                    if x1<x0 or y1<y0:continue
                    yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
                    X,Y=pts[:,0],pts[:,1];den=(Y[1]-Y[2])*(X[0]-X[2])+(X[2]-X[1])*(Y[0]-Y[2])
                    if abs(den)<1e-8:continue
                    b0=((Y[1]-Y[2])*(xx-X[2])+(X[2]-X[1])*(yy-Y[2]))/den
                    b1=((Y[2]-Y[0])*(xx-X[2])+(X[0]-X[2])*(yy-Y[2]))/den;b2=1-b0-b1
                    zz=b0*pts[0,2]+b1*pts[1,2]+b2*pts[2,2]
                    mask=(b0>=-1e-5)&(b1>=-1e-5)&(b2>=-1e-5)&(zz>depth[y0:y1+1,x0:x1+1])
                    U=b0*tuv[0,0]+b1*tuv[1,0]+b2*tuv[2,0];V=b0*tuv[0,1]+b1*tuv[1,1]+b2*tuv[2,1]
                    tx=np.clip((U*tex.shape[1]).astype(int),0,tex.shape[1]-1)
                    ty=np.clip((V*tex.shape[0]).astype(int),0,tex.shape[0]-1)
                    color=np.clip(tex[ty,tx]*shade,0,255).astype(np.uint8)
                    pixels[y0:y1+1,x0:x1+1][mask]=color[mask];depth[y0:y1+1,x0:x1+1][mask]=zz[mask]
    return Image.fromarray(pixels)

def main():
    portrait=Image.new('RGB',(1350,850),(16,22,32));pd=ImageDraw.Draw(portrait)
    pd.text((20,16),'크리스티아누 · 레알 마드리드 홈 유니폼',font=big,fill='#e4d4b5')
    portrait.paste(render('idle',0,0,width=450,height=485,scale=600,head_only=True),(0,90))
    portrait.paste(render('idle',0,15,width=450,height=745,scale=220),(450,90))
    portrait.paste(render('idle',0,165,width=450,height=745,scale=220),(900,90))
    pd.text((20,590),'새 얼굴 텍스처 · 모델 렌더',font=font,fill='#b9c7d7')
    pd.text((20,620),'게임 화면 캡처 아님',font=font,fill='#8da2b7')
    portrait.save(OUT/'Cristiano-RealMadrid-Preview.png')
    sheet=Image.new('RGB',(1360,900),(16,22,32));d=ImageDraw.Draw(sheet)
    d.text((25,18),'크리스티아누 · 사진 참고 인간형 모델',font=big,fill='#e4d4b5')
    d.text((25,55),'실제 리소스 모델·UV·관절 포즈 렌더 / 게임 스크린샷 아님',font=font,fill='#9cacbf')
    cards=[('idle',0,0,False,'정면 · 눈썹 / 턱선 / 짧은 헤어'),
           ('idle',0,155,False,'후면 · RONALDO 7'),('idle',0,25,True,'젖통닌자 · 상의 탈의'),
           ('shoot',12,35,False,'날강두 · 슈팅'),('crab',8,25,False,'꽃게 드리블'),
           ('header',14,25,False,'헤딩 · 도약'),('overhead',12,55,False,'오버헤드킥 · 교차 다리'),
           ('celebrate',18,25,False,'시우 · 착지')]
    for i,(mode,f,yaw,bare,label) in enumerate(cards):
        x=(i%4)*340;y=95+(i//4)*395
        sheet.paste(render(mode,f,yaw,bare), (x,y));d.text((x+12,y+8),label,font=font,fill='#d5dfeb')
    sheet.save(OUT/'Cristiano-Model-Preview.png')
    frames=[]
    for i in range(FRAMES):
        canvas=Image.new('RGB',(1360,1275),(16,22,32));draw=ImageDraw.Draw(canvas)
        draw.text((20,12),'크리스티아누 · 11종 관절 애니메이션',font=big,fill='#e4d4b5')
        for m,mode in enumerate(MODES):
            x=(m%4)*340;y=60+(m//4)*395
            canvas.paste(render(mode,i,40 if mode=='overhead' else 22,mode=='ninja'),(x,y))
            draw.text((x+12,y+10),LABELS[m],font=font,fill='#d5dfeb')
        draw.text((1035,900),'24 프레임 × 11 동작',font=font,fill='#b9c7d7')
        draw.text((1035,930),'공유 포즈 데이터 렌더',font=font,fill='#8da2b7')
        frames.append(canvas)
    frames[0].save(OUT/'Cristiano-Motion-Preview.gif',save_all=True,append_images=frames[1:],duration=80,loop=0,optimize=False)
    print('Rendered actual JSON/UV model and 264 poses.')

if __name__=='__main__':main()
