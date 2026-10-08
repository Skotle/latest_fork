"""Original pixel art and joint-based animation, referenced from Ronaldo photos.

Photos are visual references only; no photograph is embedded in the resource pack.
Geometry uses the item_display fixed origin (8,8,8), so limbs rotate at joints.
"""
import json, math
from PIL import Image, ImageDraw, ImageFont
from build import RP, OUT, js
from motion import quaternion, snbt

FRAMES = 24
MODES = ['idle', 'run', 'shoot', 'ninja', 'noshow', 'crab', 'header',
         'overhead', 'stagger', 'celebrate', 'recover']
SCALE = 1.15
PIXEL = SCALE / 16
PARTS = {
    'torso': (0,1.14,0), 'pelvis': (0,1.14,0), 'neck': (0,1.93,0),
    'head': (0,2.00,0),
    'left_arm': (-.39,1.85,0), 'right_arm': (.39,1.85,0),
    'left_forearm': (-.39,1.85-7.2*PIXEL,0),
    'right_forearm': (.39,1.85-7.2*PIXEL,0),
    'left_leg': (-.185,1.14,0), 'right_leg': (.185,1.14,0),
    'left_shin': (-.185,1.14-7.6*PIXEL,0),
    'right_shin': (.185,1.14-7.6*PIXEL,0),
}
REFERENCES = [
 {'url':'https://www.realmadrid.com/en-US/the-club/history/football-legends/cristiano-ronaldo-dos-santos-aveiro',
  'photos':['Official white-and-teal jersey portrait', 'Ballon d’Or side portrait', 'Knee-slide celebration'],
  'used_for':'Quiff and short sides, brows, face proportions, white kit, athletic shoulders and long legs'},
 {'url':'https://www.ledauphine.com/sport/2018/04/03/le-but-sublime-de-cristiano-ronaldo-en-video',
  'photos':['AFP overhead-kick photograph'],
  'used_for':'Reclined torso, raised striking leg, opposing bent leg, arms balancing the jump'},
]

def font(size): return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',size)

def texture(name,kind,side='left'):
    """Six independent 32-pixel faces: front, right, back, left, top, bottom."""
    colors={'skin':'#c99270','head':'#c99270','shirt':'#f2f2ec','bare':'#c99270',
            'shorts':'#eff0eb','arm':'#c99270','shin':'#f0f1eb','ball':'#f1f0e8'}
    im=Image.new('RGBA',(128,64),(0,0,0,0));d=ImageDraw.Draw(im)
    tiles=[(0,0),(32,0),(64,0),(96,0),(0,32),(32,32)]
    for face,(u,v) in enumerate(tiles):
        c=colors[kind];d.rectangle((u,v,u+31,v+31),fill=c)
        d.rectangle((u,v,u+2,v+31),fill='#b67e5f' if kind in ['skin','head','arm','bare'] else '#cdd6d3')
        d.rectangle((u+28,v,u+31,v+31),fill='#d3a07c' if kind in ['skin','head','arm','bare'] else '#dde3dc')
        if kind=='head':
            if face==0:
                # Short asymmetric quiff; clear forehead, brows, brown eyes and jaw.
                d.rectangle((u,v,u+31,v+5),fill='#211d1c')
                d.polygon([(u,v+6),(u+5,v+5),(u+5,v+8),(u,v+12)],fill='#3c3029')
                d.polygon([(u+27,v+5),(u+31,v+5),(u+31,v+11),(u+27,v+8)],fill='#3c3029')
                for x in [5,19]:
                    d.rectangle((u+x,v+11,u+x+7,v+12),fill='#382921')
                    d.rectangle((u+x,v+14,u+x+7,v+16),fill='#f2e9dc')
                    d.rectangle((u+x+3,v+14,u+x+5,v+16),fill='#4f3928')
                    d.point((u+x+4,v+14),fill='#171614')
                d.line((u+16,v+16,u+16,v+22),fill='#b67b57',width=2)
                d.line((u+14,v+22,u+18,v+22),fill='#a77250')
                d.rectangle((u+10,v+25,u+21,v+26),fill='#a96851')
                d.line((u+12,v+25,u+19,v+25),fill='#dba789')
                d.polygon([(u,v+25),(u+5,v+29),(u+12,v+31),(u,v+31)],fill='#b27b5b')
                d.polygon([(u+31,v+25),(u+26,v+29),(u+20,v+31),(u+31,v+31)],fill='#b27b5b')
            elif face in [1,3]:
                d.rectangle((u,v,u+31,v+7),fill='#39302a')
                d.rectangle((u,v,u+31,v+3),fill='#211d1c')
                for y in range(5,11,2):d.line((u,v+y,u+31,v+y),fill='#77543e')
                d.rectangle((u+11,v+14,u+18,v+23),fill='#dca480')
                d.line((u+14,v+16,u+14,v+21),fill='#ab7456')
                d.rectangle((u+13,v+22,u+15,v+24),fill='#e5e8e5')
            else:
                d.rectangle((u,v,u+31,v+23 if face==2 else v+31),fill='#27211e')
                for y in range(2,24,4):d.line((u+3,v+y,u+28,v+y-2),fill='#40332a')
        elif kind=='shirt':
            d.line((u+3,v,u+3,v+31),fill='#2c94a4',width=2)
            d.line((u+28,v,u+28,v+31),fill='#2c94a4',width=2)
            if face==0:
                d.polygon([(u+8,v),(u+16,v+7),(u+24,v),(u+21,v),(u+16,v+4),(u+11,v)],fill='#217b8d')
                d.polygon([(u+11,v),(u+16,v+4),(u+21,v)],fill='#c99270')
                d.ellipse((u+22,v+8,u+28,v+14),fill='#d5b153',outline='#1e6588')
                d.line((u+6,v+9,u+9,v+9),fill='#278999',width=2)
                d.text((u+7,v+19),'CR7',font=font(9),fill='#286579')
            if face==2:
                d.text((u+1,v+3),'RONALDO',font=font(6),fill='#216277')
                d.text((u+9,v+9),'7',font=font(22),fill='#216277')
        elif kind=='bare':
            if face==0:
                d.line((u+3,v+7,u+14,v+10),fill='#b77857',width=2)
                d.line((u+18,v+10,u+29,v+7),fill='#b77857',width=2)
                d.line((u+16,v+11,u+16,v+29),fill='#b77c5a')
                for y in [17,23,28]:d.line((u+9,v+y,u+23,v+y),fill='#bc805d')
                d.rectangle((u+6,v+11,u+8,v+12),fill='#985f48')
                d.rectangle((u+24,v+11,u+26,v+12),fill='#985f48')
            elif face==2:d.line((u+16,v+4,u+16,v+29),fill='#b87d5c')
        elif kind=='shorts':
            d.line((u,v+3,u+31,v+3),fill='#278999',width=2)
            if face==0:d.text((u+21,v+9),'7',font=font(12),fill='#286579')
        elif kind=='arm':
            # Upper quarter is short sleeve, leaving the elbow and forearm bare.
            d.rectangle((u,v,u+31,v+11),fill='#f2f2ec')
            d.line((u,v+10,u+31,v+10),fill='#2791a2',width=2)
            if side=='left':d.rectangle((u,v+12,u+31,v+17),fill='#235378')
        elif kind=='shin':
            d.rectangle((u,v,u+31,v+9),fill='#c99270')
            d.line((u,v+10,u+31,v+10),fill='#248ca0',width=2)
            d.line((u,v+13,u+31,v+13),fill='#248ca0')
        elif kind=='ball':
            for x,y in [(8,8),(24,24)]:
                d.polygon([(u+x,v+y-5),(u+x+5,v+y-2),(u+x+3,v+y+4),(u+x-3,v+y+4),(u+x-5,v+y-2)],fill='#292c31')
            d.line((u+8,v+12,u+20,v+22),fill='#777c7b')
    p=RP/f'assets/desert_ball/textures/entity/{name}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
    return im

def cube(lo,hi,texture_name,uniform=None):
    # MC south (+Z) is the character front. Other faces get separate UV tiles.
    uv={'south':[0,0,4,8],'east':[4,0,8,8],'north':[8,0,12,8],
        'west':[12,0,16,8],'up':[0,8,4,16],'down':[4,8,8,16]}
    return {'from':[8+v for v in lo],'to':[8+v for v in hi],
            'faces':{f:{'texture':'#'+texture_name,'uv':uniform or rect} for f,rect in uv.items()}}

def assets():
    for name,kind in [('head','head'),('kit','shirt'),('bare','bare'),('skin','skin'),
                      ('shorts','shorts'),('left_arm','arm'),('right_arm','arm'),
                      ('shin','shin'),('ball','ball')]:texture(name,kind,side=name.split('_')[0])
    # Small solid-color texture allows independent hair, lace, boot and sleeve cuboids.
    im=Image.new('RGBA',(16,16));colors=['#241f1c','#f2f2ec','#278999','#4bbb68',
                                       '#e4e4d6','#c99270','#b77a59','#2a3038']
    d=ImageDraw.Draw(im)
    for i,c in enumerate(colors):d.rectangle((i*2,0,i*2+1,15),fill=c)
    im.save(RP/'assets/desert_ball/textures/entity/details.png')
    def solid(lo,hi,mat):return cube(lo,hi,'details',[mat*2,0,mat*2+2,16])
    head=[cube((-3.3,.7,-3.1),(3.3,7.1,3.1),'head'),
          cube((-2.9,0,-2.8),(2.9,1.5,2.8),'skin'),
          solid((-3.4,6.1,-3.15),(3.4,7.55,3.15),0),
          solid((-2.8,7.55,-1.8),(2.7,8.3,2.5),0),
          solid((-2.5,8.3,.1),(1.9,8.65,2.7),0),
          solid((-.55,2.4,3.1),(.55,4.0,3.65),5),
          solid((-3.8,2.5,-.8),(-3.3,4.7,.8),5),solid((3.3,2.5,-.8),(3.8,4.7,.8),5)]
    models={'torso':[cube((-4.6,.4,-2.35),(4.6,10.4,2.35),'kit')],
            'bare':[cube((-4.6,.4,-2.35),(4.6,10.4,2.35),'bare')],
            'pelvis':[cube((-4.25,-2,-2.5),(4.25,.7,2.5),'shorts')],
            'neck':[cube((-1.7,0,-1.7),(1.7,1.5,1.7),'skin')], 'head':head}
    for side in ['left','right']:
        models[side+'_arm']=[cube((-1.65,-7.2,-1.75),(1.65,.3,1.75),side+'_arm')]
        models[side+'_arm_bare']=[cube((-1.65,-7.2,-1.75),(1.65,.3,1.75),'skin')]
        models[side+'_forearm']=[cube((-1.5,-6.0,-1.65),(1.5,.15,1.65),'skin'),
                               solid((-1.55,-6.6,-1.75),(1.55,-5.6,1.75),5)]
        models[side+'_leg']=[cube((-2.0,-7.6,-2.1),(2.0,.1,2.1),'skin'),
                            cube((-2.05,-4.1,-2.2),(2.05,.1,2.2),'shorts')]
        models[side+'_shin']=[cube((-1.65,-7.1,-1.8),(1.65,.15,1.8),'shin'),
                             solid((-1.8,-8.15,-2.2),(1.8,-6.95,4.0),3),
                             solid((-1.85,-8.2,-2.3),(1.85,-7.95,4.05),4),
                             solid((-.6,-6.93,.3),(.6,-6.75,2.7),4)]
    models['ball']=[cube((-3.2,-3.2,-3.2),(3.2,3.2,3.2),'ball'),
                    cube((-2.8,-3.65,-2.8),(2.8,3.65,2.8),'ball'),
                    cube((-3.65,-2.8,-2.8),(3.65,2.8,2.8),'ball')]
    texture_keys=['head','kit','bare','skin','shorts','left_arm','right_arm','shin','ball','details']
    for name,elements in models.items():
        js(RP/f'assets/desert_ball/models/{name}.json',{
            'textures':{k:f'desert_ball:entity/{k}' for k in texture_keys},'elements':elements,
            'display':{'fixed':{'rotation':[0,0,0],'translation':[0,0,0],'scale':[1,1,1]}}})
        js(RP/f'assets/desert_ball/items/{name}.json',{'model':{'type':'minecraft:model','model':f'desert_ball:{name}'}})
    p=RP/'assets/minecraft/atlases/items.json';atlas=json.loads(p.read_text())
    atlas['sources'] += [{'type':'minecraft:single','resource':f'desert_ball:entity/{k}',
                         'sprite':f'desert_ball:entity/{k}'} for k in texture_keys]
    js(p,atlas)
    js(OUT/'Cristiano-photo-references.json',{'references':REFERENCES,
        'original_assets':True,'photographs_embedded':False,
        'style':'Minecraft human proportions with white/teal CR7 kit, short quiff, face on front only'})

def rotate(q,v):
    x,y,z,w=q;vx,vy,vz=v
    tx=2*(y*vz-z*vy);ty=2*(z*vx-x*vz);tz=2*(x*vy-y*vx)
    return [vx+w*tx+y*tz-z*ty,vy+w*ty+z*tx-x*tz,vz+w*tz+x*ty-y*tx]

def mul(a,b):
    x,y,z,w=a;X,Y,Z,W=b
    return [w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z]

def add(a,b):return [x+y for x,y in zip(a,b)]

def keys(t,seq):
    for (a,va),(b,vb) in zip(seq,seq[1:]):
        if a<=t<=b:
            k=(t-a)/(b-a);k=k*k*(3-2*k)
            return {name:va.get(name,0)+(vb.get(name,0)-va.get(name,0))*k for name in set(va)|set(vb)}
    return seq[-1][1]

def poses(mode,frame):
    t=frame/(FRAMES-1);w=math.sin(t*math.tau);params={};lift=0
    if mode=='idle':params={'body':1.5*w,'armL':-4,'armR':-4,'elbowL':-5,'elbowR':-5};lift=.015*w
    elif mode=='run':
        params={'body':9,'hipL':38*w,'hipR':-38*w,'kneeL':max(0,-w)*52,'kneeR':max(0,w)*52,
                'armL':-28*w,'armR':28*w,'elbowL':-38,'elbowR':-38};lift=.035*abs(w)
    elif mode=='shoot':
        params=keys(t,[(0,{}),(.27,{'body':-8,'twist':-18,'hipR':48,'kneeR':65,'armL':-35,'armR':30}),
                      (.52,{'body':18,'twist':20,'hipR':-96,'kneeR':5,'hipL':12,'kneeL':16,'armL':-60,'armR':40}),
                      (.73,{'body':12,'hipR':-50,'kneeR':18,'armL':-25,'armR':18}),(1,{})])
    elif mode=='ninja':
        params=keys(t,[(0,{}),(.18,{'body':28,'hipL':-42,'hipR':-42,'kneeL':78,'kneeR':78,'armL':-50,'armR':-65,'elbowR':-60,'drop':-.30}),
                      (.55,{'body':20,'hipL':-30,'hipR':-30,'kneeL':65,'kneeR':65,'elbowL':-70,'elbowR':-70,'drop':-.26}),
                      (.78,{'body':22,'twist':-25,'hipR':-75,'kneeR':18,'armL':-80,'armR':-20,'spreadL':-35,'drop':-.12}),(1,{})])
    elif mode=='noshow':
        params={'body':-8+3*w,'armL':-15,'armR':-15,'elbowL':-105,'elbowR':-105,'spreadL':-45,'spreadR':45,'headY':25*w}
    elif mode=='crab':
        params={'body':8,'hipL':20*w,'hipR':-20*w,'kneeL':18+12*abs(w),'kneeR':18+12*abs(w),
                'spreadL':-72,'spreadR':72,'elbowL':-60,'elbowR':-60,'legSpreadL':-14,'legSpreadR':14,'drop':-.12}
        for at in [1/3,2/3]:
            k=max(0,1-abs(t-at)/.15);params['hipR']=-75*k+params['hipR']*(1-k)
    elif mode=='header':
        params=keys(t,[(0,{}),(.25,{'body':-18,'hipL':-35,'hipR':-35,'kneeL':70,'kneeR':70,'armL':-65,'armR':-65,'drop':-.18}),
                      (.62,{'body':24,'headX':28,'hipL':15,'hipR':10,'kneeL':25,'kneeR':40,'armL':-100,'armR':-100}),
                      (.83,{'body':10,'hipL':-20,'hipR':-20,'kneeL':40,'kneeR':40}),(1,{})])
        lift=.75*math.sin(math.pi*t)**2
    elif mode=='overhead':
        # A bicycle kick, not a rigid full-body somersault: hips and knees scissor.
        params=keys(t,[(0,{}),(.23,{'body':-22,'hipR':-55,'kneeR':65,'hipL':20,'armL':-45,'armR':-45}),
                      (.52,{'body':-92,'hipR':-85,'kneeR':8,'hipL':45,'kneeL':105,'spreadL':-65,'spreadR':65,'headX':35}),
                      (.68,{'body':-105,'hipR':20,'kneeR':90,'hipL':-65,'kneeL':5,'spreadL':-70,'spreadR':70,'headX':35}),
                      (.85,{'body':-38,'hipR':-30,'hipL':-30,'kneeL':55,'kneeR':55,'armL':-65,'armR':-65}),(1,{})])
        lift=1.05*math.sin(math.pi*t)**2
    elif mode=='stagger':
        params={'body':-18+3*w,'headX':20,'armL':20,'armR':28,'elbowL':-35,'elbowR':-45,'kneeL':18,'kneeR':18,'drop':-.12}
    elif mode=='celebrate':
        params=keys(t,[(0,{}),(.22,{'armL':-155,'armR':-155,'kneeL':30,'kneeR':30}),
                      (.48,{'yaw':175,'armL':-160,'armR':-160,'hipL':15,'hipR':15,'kneeL':40,'kneeR':40}),
                      (.70,{'yaw':360,'spreadL':-38,'spreadR':38,'legSpreadL':-22,'legSpreadR':22,'kneeL':18,'kneeR':18,'body':-8}),
                      (1,{'yaw':360,'spreadL':-32,'spreadR':32,'legSpreadL':-18,'legSpreadR':18})])
        lift=.65*math.sin(math.pi*t/.72)**2 if t<.72 else 0
    elif mode=='recover':params={'body':12*(1-t),'kneeL':28*(1-t),'kneeR':28*(1-t),'armL':-35*(1-t),'armR':-35*(1-t),'drop':-.08*(1-t)}
    lift+=params.get('drop',0)
    root=[0,1.14+lift,0];bodyq=quaternion(params.get('body',0),params.get('twist',0)+params.get('yaw',0),0)
    result={}
    def part(name,p,q):result[name]={'translation':p,'scale':[SCALE]*3,'left_rotation':q,'right_rotation':[0,0,0,1]}
    part('torso',root,bodyq);part('pelvis',root,quaternion(0,params.get('yaw',0),0))
    neck=add(root,rotate(bodyq,[0,.79,0]));head=add(root,rotate(bodyq,[0,.86,0]))
    part('neck',neck,bodyq);part('head',head,mul(bodyq,quaternion(params.get('headX',0),params.get('headY',0),0)))
    for side,sign,letter in [('left',-1,'L'),('right',1,'R')]:
        shoulder=add(root,rotate(bodyq,[sign*.39,.71,0]))
        upperq=mul(bodyq,quaternion(params.get('arm'+letter,0),0,params.get('spread'+letter,sign*5)))
        elbow=add(shoulder,rotate(upperq,[0,-7.2*PIXEL,0]))
        foreq=mul(upperq,quaternion(params.get('elbow'+letter,-8),0,0))
        part(side+'_arm',shoulder,upperq);part(side+'_forearm',elbow,foreq)
        hip=add(root,rotate(bodyq,[sign*.185,0,0]))
        thighq=mul(bodyq,quaternion(params.get('hip'+letter,0),0,params.get('legSpread'+letter,0)))
        knee=add(hip,rotate(thighq,[0,-7.6*PIXEL,0]));shinq=mul(thighq,quaternion(params.get('knee'+letter,0),0,0))
        part(side+'_leg',hip,thighq);part(side+'_shin',knee,shinq)
    # Ball is at the foot while dribbling. Header and overhead use a separate core ball.
    ball=[.25*w,.27+.07*abs(w),.55+.10*math.cos(t*math.tau)]
    if mode=='shoot':ball=[.22,.26,.55+.22*math.sin(math.pi*t)]
    part('ball',ball,quaternion(t*360,0,t*90))
    return result

def motion(fn,call):
    select=['scoreboard players set #mode db.anim 0',
      'execute if score #moving db.anim matches 1 run scoreboard players set #mode db.anim 1',
      'execute if score #safe db.safe matches 1..10 run scoreboard players set #mode db.anim 10',
      'execute if score #safe db.safe matches 11.. run scoreboard players set #mode db.anim 8',
      'scoreboard players operation #frame db.motion = #time db.time',
      f'scoreboard players set #frames db.tmp {FRAMES}',
      'scoreboard players operation #frame db.motion %= #frames db.tmp']
    for skill,mode in [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7)]:
        select.append(f'execute if score #cast db.cast matches 1.. if score #skill db.skill matches {skill} run scoreboard players set #mode db.anim {mode}')
    select += ['execute if score #cast db.cast matches 1.. run '+call('visual/cast_frame'),
      'execute if score #cast db.cast matches 0 if score #safe db.safe matches 1..10 run '+call('visual/recover_frame'),
      'execute if score #follow db.anim matches 1.. if score #skill db.skill matches 2 if score #cast db.cast matches 0 if score #safe db.safe matches ..10 run '+call('visual/ambush_frame'),
      'execute if score #follow db.anim matches 1.. run scoreboard players remove #follow db.anim 1',
      'execute if score #time db.time matches ..36 if score #cast db.cast matches 0 if score #safe db.safe matches 0 run '+call('visual/intro_frame'),
      'execute as @e[tag=db.body] at @e[tag=db.boss,limit=1] run tp @s ~ ~ ~ ~ 0',
      'execute if score #skill db.skill matches 2 run item replace entity @e[tag=db.part.torso,limit=1] contents with minecraft:paper[minecraft:item_model="desert_ball:bare"]',
      'execute unless score #skill db.skill matches 2 run item replace entity @e[tag=db.part.torso,limit=1] contents with minecraft:paper[minecraft:item_model="desert_ball:torso"]']
    for side in ['left','right']:
        select += [f'execute if score #skill db.skill matches 2 run item replace entity @e[tag=db.part.{side}_arm,limit=1] contents with minecraft:paper[minecraft:item_model="desert_ball:{side}_arm_bare"]',
                   f'execute unless score #skill db.skill matches 2 run item replace entity @e[tag=db.part.{side}_arm,limit=1] contents with minecraft:paper[minecraft:item_model="desert_ball:{side}_arm"]']
    select += [f'execute if score #mode db.anim matches {m} run '+call(f'visual/{mode}/dispatch') for m,mode in enumerate(MODES)]
    fn('visual/tick',select)
    fn('visual/cast_frame',['scoreboard players set #length db.tmp 24',
      'execute if score #skill db.skill matches 2..3 run scoreboard players set #length db.tmp 40',
      'execute if score #skill db.skill matches 4 run scoreboard players set #length db.tmp 36',
      'execute if score #skill db.skill matches 5..6 run scoreboard players set #length db.tmp 30',
      'scoreboard players operation #frame db.motion = #length db.tmp',
      'scoreboard players operation #frame db.motion -= #cast db.cast',
      f'scoreboard players set #last db.tmp {FRAMES-1}',
      'scoreboard players operation #frame db.motion *= #last db.tmp',
      'scoreboard players operation #frame db.motion /= #length db.tmp'])
    fn('visual/recover_frame',['scoreboard players set #frame db.motion 10',
       'scoreboard players operation #frame db.motion -= #safe db.safe',
       f'scoreboard players set #last db.tmp {FRAMES-1}',
       'scoreboard players operation #frame db.motion *= #last db.tmp',
       'scoreboard players set #length db.tmp 10','scoreboard players operation #frame db.motion /= #length db.tmp'])
    fn('visual/ambush_frame',['scoreboard players set #mode db.anim 3','scoreboard players set #frame db.motion 12',
       'scoreboard players operation #frame db.motion -= #follow db.anim','scoreboard players set #tail db.tmp 9',
       'scoreboard players operation #frame db.motion *= #tail db.tmp','scoreboard players set #length db.tmp 12',
       'scoreboard players operation #frame db.motion /= #length db.tmp','scoreboard players add #frame db.motion 14'])
    fn('visual/intro_frame',['scoreboard players set #mode db.anim 9',
       'scoreboard players operation #frame db.motion = #time db.time',
       f'scoreboard players set #last db.tmp {FRAMES-1}',
       'scoreboard players operation #frame db.motion *= #last db.tmp',
       'scoreboard players set #length db.tmp 36','scoreboard players operation #frame db.motion /= #length db.tmp'])
    for mode in MODES:
        fn(f'visual/{mode}/dispatch',[f'execute if score #frame db.motion matches {i} run '+call(f'visual/{mode}/{i}') for i in range(FRAMES)])
        for i in range(FRAMES):
            lines=[]
            transforms=poses(mode,i)
            jump=max(0,transforms['torso']['translation'][1]-1.14) if mode in ['header','overhead','celebrate'] else 0
            if mode in ['header','overhead','celebrate']:
                origin='db.anchor,tag=db.current' if mode=='celebrate' else 'db.jump_origin'
                lines += [f'execute as @e[tag=db.boss,limit=1] at @e[tag={origin},limit=1] run tp @s ~ ~{jump:.5f} ~',
                          'execute as @e[tag=db.body] at @e[tag=db.boss,limit=1] run tp @s ~ ~ ~ ~ 0']
            for part,tr in transforms.items():
                tr['translation'][1]-=jump
                tag='db.carried_ball' if part=='ball' else 'db.part.'+part
                if part=='ball' and mode in ['header','overhead','ninja','noshow']:tr['scale']=[0,0,0]
                lines.append(f'data merge entity @e[tag={tag},limit=1] {{start_interpolation:0,interpolation_duration:2,transformation:{snbt(tr)}}}')
            fn(f'visual/{mode}/{i}',lines)
    js(OUT/'Cristiano-animation-guide.json',{'frames':FRAMES,'modes':MODES,
        'body_parts':len(PARTS),'joint_hierarchy':'hips → thighs → knees → shins; torso → shoulders → elbows → forearms; neck → head',
        'cast_synchronized':True,'interpolation_ticks':2,'poses_generated':len(MODES)*FRAMES,
        'root_hitbox':'Carrier follows header, bicycle-kick and celebration jumps; limb extremities remain outside the vanilla box.',
        'references':REFERENCES})
