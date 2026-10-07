"""Ten articulated parts and interpolated per-action poses, shared with preview."""
import json, math
from build import DP, RP, NS, fn, js, display

PARTS={
 'body':((0,1.65,0),(1.7,1.7,1.7)),
 'head':((0,2.65,0),(1.7,1.7,1.7)),
 'left_arm':((-.83,2.2,0),(1.5,1.5,1.5)),
 'right_arm':((.83,2.2,0),(1.5,1.5,1.5)),
 'left_hand':((-.83,1.48,0),(1.4,1.4,1.4)),
 'bell':((.83,1.25,0),(1.5,1.5,1.5)),
 'left_leg':((-.34,.85,0),(1.6,1.6,1.6)),
 'right_leg':((.34,.85,0),(1.6,1.6,1.6)),
 'core':((0,1.85,-.49),(1.5,1.5,1.5)),
 'crown':((0,3.25,0),(1.6,1.6,1.6))}
MODES=['idle','walk','wind','impact','recover','dash','stagger','ritual']
FRAMES=16

def quaternion(x=0,y=0,z=0):
    x,y,z=[math.radians(v)/2 for v in (x,y,z)]
    sx,cx=math.sin(x),math.cos(x);sy,cy=math.sin(y),math.cos(y);sz,cz=math.sin(z),math.cos(z)
    return [sx*cy*cz-cx*sy*sz,cx*sy*cz+sx*cy*sz,cx*cy*sz-sx*sy*cz,cx*cy*cz+sx*sy*sz]

def poses(mode,frame):
    t=frame/(FRAMES-1);wave=math.sin(t*math.tau);step=math.sin(t*math.tau)
    torso=0;twist=0;bob=.025*wave;leg=0;armL=3*wave;armR=-3*wave;spread=0;lift=0
    if mode=='walk':leg=32*step;armL=-leg*.65;armR=leg*.65;torso=7;bob=.04*abs(step)
    elif mode=='wind':armR=-25-120*t;armL=-12-30*t;torso=-12*t;twist=-20*t;spread=.10*t
    elif mode=='impact':armR=-145+200*t;armL=-42+65*t;torso=-12+40*t;twist=-20+60*t;bob=-.2*math.sin(t*math.pi)
    elif mode=='recover':armR=55*(1-t);armL=23*(1-t);torso=28*(1-t);twist=40*(1-t);bob=-.12*(1-t)
    elif mode=='dash':leg=55*step;armL=-leg*.55;armR=-85;torso=24;bob=.10*abs(step);spread=.08
    elif mode=='stagger':torso=-22+5*wave;twist=8*wave;armL=28;armR=35;bob=-.18;spread=.18
    elif mode=='ritual':armL=-65+8*wave;armR=-80-8*wave;torso=-7;lift=.2+.06*wave;spread=.12
    result={}
    for name,(pos,scale) in PARTS.items():
        p=list(pos);p[1]+=bob+lift;rot=(0,0,0)
        if name=='body':rot=(torso,twist,0)
        elif name=='head':rot=(-torso*.5,-twist*.5,3*wave);p[2]+=.12*math.sin(math.radians(torso))
        elif name in ['left_arm','right_arm','left_hand','bell']:
            right=name in ['right_arm','bell'];angle=armR if right else armL
            rot=(angle,twist,(-1 if right else 1)*8)
            if name in ['left_hand','bell']:
                length=.8 if right else .72
                p[1]=2.2-length*math.cos(math.radians(angle))+bob+lift
                p[2]=-length*math.sin(math.radians(angle))
            p[0]+=(1 if right else -1)*spread
        elif name in ['left_leg','right_leg']:
            rot=(leg if name=='left_leg' else -leg,0,0);p[0]+=(1 if name=='right_leg' else -1)*spread
        elif name=='core':p[2]-=.18 if mode=='stagger' else .02*wave;rot=(torso,twist,0)
        elif name=='crown':rot=(0,0,t*360);p[1]+=.1*wave
        result[name]={'translation':p,'left_rotation':quaternion(*rot),'scale':list(scale),'right_rotation':[0,0,0,1]}
        if name=='core' and mode=='stagger':result[name]['scale']=[2.7,2.7,2.7]
    return result

def snbt(value):
    if isinstance(value,dict):return '{'+','.join(k+':'+snbt(v) for k,v in value.items())+'}'
    return '['+','.join(f'{v:.5f}f' for v in value)+']'

def upgrade_motion():
    def box(center,size,mat=0):return {
        'from':[8+c-s/2 for c,s in zip(center,size)],'to':[8+c+s/2 for c,s in zip(center,size)],
        'faces':{f:{'texture':'#atlas','uv':[mat*4,0,mat*4+4,16]} for f in ['up','down','north','south','east','west']}}
    models={
     'body':[box((0,0,0),(13,13,8)),box((0,-5,0),(15,3,9),1),box((0,5,0),(16,3,10),2)],
     'head':[box((0,0,0),(8,8,8)),box((0,1,-4.3),(6,1,1),3),box((0,5,0),(10,2,10),2)],
     'left_arm':[box((0,-3,0),(5,8,6),1),box((0,0,0),(7,4,8),2)],
     'right_arm':[box((0,-3,0),(5,8,6),1),box((0,0,0),(7,4,8),2)],
     'left_hand':[box((0,-1,0),(5,7,5)),box((0,-4,0),(6,3,6),2)],
     'left_leg':[box((0,-3,0),(5,9,6)),box((0,-7,-1),(6,3,9),1)],
     'right_leg':[box((0,-3,0),(5,9,6)),box((0,-7,-1),(6,3,9),1)]}
    for name,elements in models.items():
        js(RP/f'assets/{NS}/models/{name}.json',{'textures':{'atlas':f'{NS}:entity/nox','particle':f'{NS}:entity/nox'},'elements':elements,'display':{'fixed':{'rotation':[0,0,0],'translation':[0,0,0],'scale':[1,1,1]}}})
        js(RP/f'assets/{NS}/items/{name}.json',{'model':{'type':'minecraft:model','model':f'{NS}:{name}'}})
    summon=(DP/f'data/{NS}/function/fight/summon.mcfunction').read_text(encoding='utf-8').splitlines()[0]
    fn('fight/summon',[summon]+[display(n,p,s,('nox.bodypart','nox.joint.'+n)) for n,(p,s) in PARTS.items()])
    # Interpolation is restarted only on a new pose (10 Hz), not every server tick.
    for mode in MODES:
        for i in range(FRAMES):
            lines=[]
            for name,transform in poses(mode,i).items():
                lines += [f'data merge entity @e[tag=nox.joint.{name},limit=1] {{start_interpolation:0,interpolation_duration:2,transformation:{snbt(transform)}}}']
            fn(f'visual/pose/{mode}/{i}',lines)
    fn('visual/apply',['$function eclipse_nox:visual/pose/$(pose)/$(frame)'])
    tick=['scoreboard players set #anim nx.anim 0',
          'execute if score #moving nx.move matches 1 run scoreboard players set #anim nx.anim 1',
          'execute if score #cast nx.cast matches 1.. run scoreboard players set #anim nx.anim 2',
          'execute if score #cast nx.cast matches 1..18 run scoreboard players set #anim nx.anim 3',
          'execute if score #safe nx.safe matches 1.. run scoreboard players set #anim nx.anim 4',
          'execute if score #dash nx.dash matches 1.. run scoreboard players set #anim nx.anim 5',
          'execute if score #safe nx.safe matches 50.. run scoreboard players set #anim nx.anim 6',
          'execute if score #puzzle nx.puzzle matches 1 run scoreboard players set #anim nx.anim 7',
          'execute if score #skill nx.skill matches 4 if score #cast nx.cast matches 1.. run scoreboard players set #anim nx.anim 7',
          'execute unless score #anim nx.anim = #previous nx.anim run scoreboard players set #animtime nx.anim 0',
          'scoreboard players operation #previous nx.anim = #anim nx.anim',
          'scoreboard players add #animtime nx.anim 1',
          'scoreboard players operation #frame nx.tmp = #animtime nx.anim',
          'scoreboard players set #two nx.tmp 2','scoreboard players set #sixteen nx.tmp 16',
          'scoreboard players operation #frame nx.tmp /= #two nx.tmp',
          'scoreboard players operation #frame nx.tmp %= #sixteen nx.tmp',
          'execute if score #anim nx.anim matches 2 run '+_progress_frame('wind'),
          'execute if score #anim nx.anim matches 3 run '+_progress_frame('impact'),
          'execute if score #anim nx.anim matches 4 run '+_progress_frame('recover'),
          'execute store result storage eclipse_nox:motion frame int 1 run scoreboard players get #frame nx.tmp']
    for i,mode in enumerate(MODES):tick.append(f'execute if score #anim nx.anim matches {i} run data modify storage eclipse_nox:motion pose set value "{mode}"')
    tick+=['scoreboard players operation #fx nx.tmp = #time nx.time','scoreboard players operation #fx nx.tmp %= #two nx.tmp',
           'execute if score #fx nx.tmp matches 0 run function eclipse_nox:visual/apply with storage eclipse_nox:motion']
    fn('visual/tick',tick)
    fn('visual/frame/wind',['scoreboard players operation #frame nx.tmp = #total nx.total','scoreboard players operation #frame nx.tmp -= #cast nx.cast',
                           'scoreboard players set #fifteen nx.tmp 15','scoreboard players operation #frame nx.tmp *= #fifteen nx.tmp',
                           'scoreboard players operation #denom nx.tmp = #total nx.total','scoreboard players remove #denom nx.tmp 18',
                           'execute if score #denom nx.tmp matches ..0 run scoreboard players set #denom nx.tmp 1',
                           'scoreboard players operation #frame nx.tmp /= #denom nx.tmp','execute if score #frame nx.tmp matches 16.. run scoreboard players set #frame nx.tmp 15'])
    fn('visual/frame/impact',['scoreboard players set #frame nx.tmp 18','scoreboard players operation #frame nx.tmp -= #cast nx.cast',
                             'scoreboard players set #fifteen nx.tmp 15','scoreboard players set #eighteen nx.tmp 18',
                             'scoreboard players operation #frame nx.tmp *= #fifteen nx.tmp','scoreboard players operation #frame nx.tmp /= #eighteen nx.tmp'])
    fn('visual/frame/recover',['scoreboard players set #frame nx.tmp 30','scoreboard players operation #frame nx.tmp -= #safe nx.safe',
                              'execute if score #frame nx.tmp matches ..0 run scoreboard players set #frame nx.tmp 0',
                              'scoreboard players set #thirty nx.tmp 30','scoreboard players set #fifteen nx.tmp 15',
                              'scoreboard players operation #frame nx.tmp *= #fifteen nx.tmp','scoreboard players operation #frame nx.tmp /= #thirty nx.tmp',
                              'execute if score #frame nx.tmp matches 16.. run scoreboard players set #frame nx.tmp 15'])
    p=DP/f'data/{NS}/function/load.mcfunction';load=p.read_text(encoding='utf-8').splitlines()
    fn('load',[f'scoreboard objectives add nx.{o} dummy' for o in ['anim','move','dash','total','expose','recover','combo']]+load)
    p=DP/f'data/{NS}/function/fight/alive.mcfunction';lines=p.read_text(encoding='utf-8').splitlines()
    # Remove the static arm/core overrides; poses now own every joint.
    lines=[l for l in lines if 'transformation.translation set value' not in l and 'transformation.scale set value' not in l]
    fn('fight/alive',lines)

def _progress_frame(name):return 'function eclipse_nox:visual/frame/'+name
