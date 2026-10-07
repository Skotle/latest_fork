"""Code-native, articulated vanilla boss models. No client mod or shader required.

Geometry uses separate item displays per joint; all locations are relative to the
carrier's feet, never passenger offsets. The original resource pack is an input,
not an output. Only the ida_boss namespace is supplied by this overlay.
"""
import json
import math
import struct
import zlib
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
RESOURCE = BASE / 'boss_resources'
OUTPUT = BASE / 'output'
PALETTES = {
 'abandoned_temple': ('19292d','456052','899575','65e4a5'),
 'aviary': ('173747','367e96','b8dfe2','73f4ff'),
 'bandit_towers': ('30242c','914541','d8b591','ff7660'),
 'bandit_village': ('382025','97353a','d3a873','ffbe52'),
 'bathhouse': ('1b3540','368c91','a1d7cd','65ffe1'),
 'ceryneian_hind': ('513923','ad8050','f1d79b','ffe287'),
 'desert_hall': ('3e302b','b48639','f8d982','ffeb6d'),
 'foundry': ('26242c','575665','ae8f77','ff862d'),
 'heavenly_challenger': ('302b4f','6964a3','ddd7fa','96f7ff'),
 'heavenly_conqueror': ('221d36','584377','a494bf','cf79ff'),
 'heavenly_rider': ('252c52','626faa','e0d4f2','bcf1ff'),
 'illager_campsite': ('293327','67754c','cbbb91','e6ed75'),
 'infested_temple': ('20394b','537d99','d2f3f6','82e9ff'),
 'keep_kayra': ('233b34','56745b','b1ad8b','88efb1'),
 'kisegi_sanctuary': ('302038','795277','ddd1d0','fa8ce0'),
 'mechanical_nest': ('25323e','667a89','d3bb78','75eaff'),
 'mining_complex': ('322c27','856642','d5aa62','ffb04b'),
 'plague_asylum': ('242b2d','657b70','c9c29f','b0ff72'),
 'scorched_mines': ('29242b','72515a','d2b29c','ff684b'),
 'small_blimp': ('313040','796b82','dbc6a4','92e3ff'),
 'thornborn_towers': ('262f24','5e714b','b2a076','c9f27a'),
 'typhon': ('192b43','35667e','7eb9bd','6bfaff'),
}

def write_json(path, value):
 path.parent.mkdir(parents=True, exist_ok=True)
 path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def png(path, width, height, pixels):
 def chunk(kind, data):
  return struct.pack('>I', len(data))+kind+data+struct.pack('>I', zlib.crc32(kind+data)&0xffffffff)
 raw=b''.join(b'\0'+bytes(pixels[y*width*4:(y+1)*width*4]) for y in range(height))
 path.parent.mkdir(parents=True, exist_ok=True)
 path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))

def texture(ident):
 pixels=[]
 for y in range(16):
  for x in range(64):
   material=x//16
   rgb=tuple(bytes.fromhex(PALETTES[ident][material]))
   # Edges, mottling, and small rivets remain legible on Minecraft-size models.
   delta=(-24 if x%16 in (0,15) or y in (0,15) else
          17 if (x%16,y) in [(3,3),(12,3),(3,12),(12,12)] else
          ((x*13+y*7+material*11)%9-4)*2)
   if material==3: delta=7 if (x+y)%5==0 else 0
   pixels.extend([max(0,min(255,c+delta)) for c in rgb]+[255])
 png(RESOURCE/f'assets/ida_boss/textures/boss/{ident}.png',64,16,pixels)

class Rig:
 def __init__(self, ident):
  self.ident=ident;self.parts=[]
 def part(self, name, pos, cubes, motion='still', sign=1, rotation=(0,0,0), glow=False):
  self.parts.append(dict(name=name,pos=list(pos),cubes=cubes,motion=motion,sign=sign,rotation=list(rotation),glow=glow))
 def cube(self, center, size, material=1):
  return dict(center=list(center),size=list(size),material=material)
 def ring(self, name, pos, radius=.8, motion='ring', axis='z'):
  cubes=[]
  for i in range(12):
   a=i*math.tau/12
   c=(math.cos(a)*radius,math.sin(a)*radius,0) if axis=='z' else (math.cos(a)*radius,0,math.sin(a)*radius)
   cubes.append(self.cube(c,(.17,.17,.17),3 if i%3==0 else 2))
  self.part(name,pos,cubes,motion,glow=True)

def humanoid(r, kind):
 c=r.cube
 r.part('body',(0,1.35,0),[c((0,0,0),(.76,.86,.42)),c((0,.2,-.235),(.32,.38,.07),2),c((0,.18,-.28),(.13,.16,.05),3)])
 head=[c((0,0,0),(.52,.55,.5)),c((-.13,.04,-.26),(.1,.06,.035),3),c((.13,.04,-.26),(.1,.06,.035),3)]
 if kind in ['desert_hall','ceryneian_hind']:
  head += [c((s*.34,0,0),(.13,.72,.5),2) for s in [-1,1]]
  head += [c((0,.35,0),(.16,.25,.2),2)]
 elif kind in ['plague_asylum','infested_temple']:
  head += [c((0,-.14,-.34),(.3,.2,.36),2),c((0,.3,0),(.7,.1,.65),0)]
 elif kind in ['bandit_towers','small_blimp']:
  head += [c((0,.27,0),(.85,.12,.73),0),c((0,.38,0),(.46,.2,.43),0)]
 else:
  head += [c((s*.26,.32,0),(.12,.4,.13),2) for s in [-1,1]]
 r.part('head',(0,2.08,-.015),head,'head')
 for s in [-1,1]:
  arm=[c((0,-.3,0),(.25,.68,.28)),c((0,.03,0),(.39,.3,.4),2)]
  if s==1:
   if kind in ['bandit_towers','small_blimp','mechanical_nest']:
    arm += [c((0,-.66,-.3),(.2,.24,.75),0),c((0,-.65,-.47),(.83,.12,.16),2),c((0,-.65,-.8),(.13,.14,.16),3)]
   elif kind=='mining_complex':
    arm += [c((0,-.85,-.05),(.46,.62,.46),0),c((0,-1.17,-.05),(.3,.17,.3),2),c((0,-1.3,-.05),(.13,.1,.13),3)]
   elif kind in ['plague_asylum','infested_temple','desert_hall']:
    arm += [c((0,-.63,0),(.1,1.4,.1),2),c((0,.19,0),(.32,.32,.32),3)]
   else:
    arm += [c((0,-.85,0),(.09,1.05,.13),2),c((0,-1.27,-.02),(.45,.34,.17),2)]
  r.part('arm_'+str(s),(s*.56,1.76,0),arm,'arm',s)
  r.part('leg_'+str(s),(s*.22,.9,0),[c((0,-.33,0),(.27,.69,.3),0),c((0,-.68,-.09),(.34,.18,.5),2)],'leg',s)
 # The shape-defining equipment is part of the rig, not vanilla worn armor.
 if kind=='desert_hall':r.ring('sun',(0,2.25,.25),.88)
 elif kind=='ceryneian_hind':
  for s in [-1,1]:
   r.part('antler_'+str(s),(s*.28,2.35,0),[c((s*.18,.3,0),(.12,.75,.13),2),c((s*.31,.52,0),(.4,.12,.12),2),c((s*.44,.7,0),(.1,.36,.12),2)])
 elif kind=='plague_asylum':
  r.part('vats',(0,1.4,.4),[c((s*.36,0,0),(.3,.9,.32),0) for s in [-1,1]]+[c((s*.36,.2,-.18),(.17,.42,.04),3) for s in [-1,1]],glow=True)
 elif kind=='infested_temple':
  r.part('ice_crown',(0,2.5,0),[c((s*.3,.17,0),(.16,.5,.16),3) for s in [-1,0,1]],glow=True)
 elif kind=='small_blimp':r.ring('propeller',(0,1.63,.5),.48,axis='z')
 elif kind=='bandit_towers':
  r.part('cloak',(0,1.45,.31),[c((0,-.15,0),(.95,1.05,.09),0),c((-.36,-.65,0),(.2,.3,.09),1)])
 elif kind=='bandit_village':
  r.part('banner',(0,2,.45),[c((0,0,0),(.08,1.55,.08),2),c((.28,.37,0),(.5,.55,.07),1)],'banner')
 elif kind=='illager_campsite':
  r.part('shield',(-.72,1.05,-.18),[c((0,0,0),(.65,.95,.14),0),c((0,0,-.09),(.41,.7,.04),2)],'arm',-1)
 elif kind=='keep_kayra':
  r.part('shield',(-.76,1.2,-.2),[c((0,0,0),(.79,1.35,.2),0),c((0,0,-.13),(.52,1.05,.04),1),c((0,.2,-.17),(.24,.28,.04),3)],'arm',-1)
  r.part('reeds',(0,1.75,.4),[c((s*.38,.16,0),(.12,.85,.13),1) for s in [-1,1]])
 elif kind=='bathhouse':
  r.ring('valve',(0,1.4,.45),.55)
  r.part('pipe',(.4,2.27,.12),[c((0,0,0),(.23,.5,.23),2),c((.15,.16,0),(.5,.17,.23),2)])
 elif kind=='foundry':
  r.part('anvil',(0,1.82,.39),[c((0,0,0),(1.3,.22,.5),0),c((0,-.24,0),(.5,.38,.4),0)])
  r.part('furnace',(0,1.32,-.28),[c((0,0,0),(.62,.53,.11),0)]+[c((i*.14,0,-.07),(.08,.33,.025),3) for i in [-1,0,1]],glow=True)
 elif kind=='scorched_mines':
  r.part('blades',(0,1.55,.4),[c((s*.25,.07,0),(.14,1.3,.1),2) for s in [-1,1]],rotation=(0,0,30))
 elif kind=='mining_complex':
  r.part('tank',(0,1.25,.43),[c((0,0,0),(.7,.9,.45),0),c((0,.1,.24),(.48,.42,.04),3)],glow=True)
 elif kind=='mechanical_nest':
  r.ring('dynamo',(0,1.38,.48),.64)
  for s in [-1,1]:r.part('coil_'+str(s),(s*.68,1.98,0),[c((0,0,0),(.32,.65,.35),0)]+[c((0,y,0),(.45,.08,.46),2) for y in [-.25,0,.25]])
 # Dedicated bodywork and masks distinguish the armored humanoid silhouettes.
 if kind in ['foundry','mining_complex','mechanical_nest','keep_kayra','bandit_village']:
  body=next(p for p in r.parts if p['name']=='body')
  body['cubes'][0]['size']=[1.03,.93,.55]
  for p in r.parts:
   if p['name'].startswith('arm_'):
    p['pos'][0]*=1.18
    p['cubes'][0]['size'][0]=.34
 if kind=='foundry':
  next(p for p in r.parts if p['name']=='head')['cubes']=[c((0,0,0),(.62,.58,.53),0),c((0,.03,-.29),(.48,.09,.06),3),c((0,-.13,-.29),(.48,.1,.06),2)]
  arm=next(p for p in r.parts if p['name']=='arm_1')
  arm['cubes']=arm['cubes'][:2]+[c((0,-.73,0),(.13,1.03,.13),2),c((0,-1.15,0),(.9,.38,.54),0),c((0,-1.15,-.29),(.5,.16,.04),3)]
 elif kind=='mining_complex':
  next(p for p in r.parts if p['name']=='head')['cubes']=[c((0,0,0),(.53,.5,.52),0),c((0,.25,0),(.7,.12,.69),2),c((0,.19,-.32),(.18,.18,.12),3)]
 elif kind=='mechanical_nest':
  next(p for p in r.parts if p['name']=='head')['cubes']=[c((0,0,0),(.61,.43,.49),2),c((0,0,-.27),(.45,.13,.07),0),c((0,0,-.32),(.32,.07,.04),3),c((-.33,.31,0),(.07,.5,.08),2)]
 elif kind=='bathhouse':
  next(p for p in r.parts if p['name']=='head')['cubes']=[c((0,0,0),(.64,.58,.59),2),c((0,.02,-.33),(.45,.35,.08),0),c((0,.02,-.38),(.31,.23,.03),3)]
 if kind in ['plague_asylum','infested_temple']:
  r.part('robe',(0,.82,.04),[c((0,0,0),(.7,.82,.49),0)]+[c((s*.22,-.46,0),(.2,.24,.49),1) for s in [-1,1]])

def spider(r, queen):
 c=r.cube
 r.part('abdomen',(0,.76,.47),[c((0,0,0),(1.15,.78,1.2),0),c((0,.37,.15),(.7,.13,.7),1),c((0,.46,.2),(.3,.09,.34),3)],'body',glow=False)
 r.part('body',(0,.92,-.35),[c((0,0,0),(.78,.48,.7)),c((0,.12,-.36),(.45,.15,.08),3)],'body')
 for s in [-1,1]:
  for i in range(4):
   r.part(f'leg_{s}_{i}',(s*.42,.83,.52-i*.32),[c((s*.36,-.05,0),(.83,.14,.16)),c((s*.74,-.34,0),(.13,.64,.15),0),c((s*.79,-.67,-.08),(.24,.1,.29),2)],'spider',s if i%2 else -s,rotation=(0,(i-1.5)*18,0))
  r.part('fang_'+str(s),(s*.24,.8,-.8),[c((0,-.13,0),(.12,.38,.14),2),c((-s*.055,-.31,-.05),(.19,.11,.24),3)],'fang',s,glow=True)
 if queen:
  r.part('torso',(0,1.4,-.38),[c((0,0,0),(.5,.7,.36)),c((0,.25,-.22),(.23,.25,.07),3)])
  r.part('head',(0,1.99,-.4),[c((0,0,0),(.48,.48,.45),2),c((0,.3,0),(.6,.12,.5),1)]+[c((s*.2,.41,0),(.08,.3,.08),3) for s in [-1,0,1]],'head')
  for s in [-1,1]:r.part('arm_'+str(s),(s*.35,1.65,-.38),[c((s*.13,-.2,0),(.16,.6,.18)),c((s*.2,-.46,-.16),(.15,.16,.38),2)],'arm',s)
 else:
  r.part('head',(0,.91,-.87),[c((0,0,0),(.65,.43,.37),0)]+[c((x,.05,-.21),(.08,.08,.05),3) for x in [-.23,-.08,.08,.23]],'head')
  r.part('obelisk',(0,1.14,.54),[c((0,0,0),(.38,.6,.42),1),c((0,.39,0),(.23,.2,.25),2)])

def winged(r, rider):
 c=r.cube
 r.part('body',(0,1.25,0),[c((0,0,0),(.7,.55,1.05)),c((0,.26,-.25),(.46,.16,.45),2)],'body')
 r.part('head',(0,1.47,-.65),[c((0,0,0),(.48,.4,.53),0),c((0,-.07,-.35),(.18,.14,.3),2),c((-.2,.06,-.25),(.07,.07,.08),3),c((.2,.06,-.25),(.07,.07,.08),3)],'head')
 for s in [-1,1]:
  cubes=[c((s*.56,0,.17),(1.12,.12,.8)),c((s*1.15,-.04,.35),(.42,.1,.7),2)]
  cubes += [c((s*(.3+i*.21),-.1,.55+i*.06),(.16,.13,.72),1) for i in range(5)]
  r.part('wing_'+str(s),(s*.3,1.37,0),cubes,'wing',s)
 r.part('tail',(0,1.17,.83),[c((0,0,.17),(.4,.12,.54),2),c((0,0,.55),(.23,.1,.33),3)],'tail')
 if rider:
  r.part('rider',(0,1.9,.12),[c((0,0,0),(.43,.55,.3),0),c((0,.46,0),(.38,.35,.35),2),c((0,.47,-.2),(.27,.06,.04),3)])
  r.part('lance',(.42,1.94,-.35),[c((0,0,0),(.08,1.48,.08),2),c((0,.9,0),(.16,.31,.16),3)],'arm',1,rotation=(25,0,-15))
 else:
  r.part('cage',(0,1.3,.08),[c((s*.36,0,0),(.09,.82,.1),2) for s in [-1,1]]+[c((0,.4,0),(.78,.1,.68),2)])

def construct(r, kind):
 c=r.cube
 if kind=='heavenly_challenger':
  r.part('core',(0,1.45,0),[c((0,0,0),(.7,.7,.7),0),c((0,0,-.37),(.38,.38,.04),3)],'core',glow=True)
  for s in [-1,1]:
   r.part('shell_'+str(s),(0,1.45+s*.55,0),[c((0,0,0),(1.3,.35,1.3),1),c((0,s*.23,0),(.85,.18,.85),2)],'shell',s)
  r.ring('orbit',(0,1.45,0),1,'ring',axis='y')
 elif kind=='heavenly_conqueror':
  r.part('body',(0,1.33,0),[c((0,0,0),(.68,1.0,.39),0),c((0,.16,-.24),(.25,.3,.1),3)],'body')
  r.part('head',(0,2.12,0),[])
  # Crown blades float clear of the mask.
  r.parts[-1]['cubes']=[c((0,0,0),(.48,.48,.45),1),c((0,.05,-.25),(.29,.07,.04),3)]+[c((s*.32,.32,0),(.13,.65,.15),2) for s in [-1,1]]
  for s in [-1,1]:
   r.part('blade_'+str(s),(s*.8,1.45,0),[c((0,0,0),(.17,1.32,.22),2),c((0,.8,0),(.12,.25,.14),3)],'blade',s,glow=True)
   r.part('mantle_'+str(s),(s*.35,1.25,.22),[c((s*.12,-.1,0),(.4,1.1,.1),0),c((s*.2,-.7,0),(.19,.36,.1),1)],'banner',s)
  r.ring('halo',(0,2.08,.31),.84)
 elif kind=='thornborn_towers':
  r.part('body',(0,1.1,0),[c((0,0,0),(1.05,1.16,.72),0),c((0,.13,-.39),(.43,.56,.06),3)],'body')
  r.part('head',(0,1.99,0),[c((0,0,0),(.64,.62,.55)),c((0,.02,-.3),(.4,.08,.06),3),c((0,-.21,-.33),(.29,.08,.08),0)],'head')
  for s in [-1,1]:
   r.part('arm_'+str(s),(s*.69,1.52,0),[c((s*.08,-.28,0),(.38,.91,.43),0),c((s*.24,-.65,-.05),(.45,.24,.5),2)],'arm',s)
   r.part('root_'+str(s),(s*.3,.62,0),[c((s*.1,-.2,0),(.38,.6,.4),0),c((s*.22,-.47,-.25),(.5,.18,.79),0)],'leg',s)
   r.part('branch_'+str(s),(s*.36,2.18,0),[c((s*.2,.2,0),(.13,.73,.14),0),c((s*.41,.31,0),(.51,.13,.14),0),c((s*.6,.48,0),(.12,.33,.14),2)])
 elif kind=='typhon':
  r.part('body',(0,1.2,0),[c((0,0,0),(1.1,.9,.7)),c((0,.22,-.36),(.7,.2,.08),2)],'body')
  r.part('head',(0,1.94,-.08),[c((0,0,0),(.78,.7,.59),0),c((0,.06,-.33),(.58,.09,.06),3),c((0,-.23,-.36),(.48,.15,.12),2)],'head')
  for s in [-1,1]:
   for i in range(3):
    r.part(f'tentacle_{s}_{i}',(s*.42,.82,.4-i*.4),[c((s*.26,-.12,0),(.65,.28,.29)),c((s*.62,-.32,-.07),(.32,.38,.28)),c((s*.86,-.49,-.17),(.3,.14,.48),2)],'tentacle',s if i%2 else -s)
   r.part('fin_'+str(s),(s*.48,1.85,.1),[c((s*.16,0,0),(.37,.5,.13),2),c((s*.35,.15,0),(.16,.5,.13),3)],'wing',s)
  r.ring('crest',(0,2.35,.13),.68)

def make_rig(ident):
 r=Rig(ident)
 if ident in ['abandoned_temple','kisegi_sanctuary']:spider(r,ident=='kisegi_sanctuary')
 elif ident in ['aviary','heavenly_rider']:winged(r,ident=='heavenly_rider')
 elif ident in ['heavenly_challenger','heavenly_conqueror','thornborn_towers','typhon']:construct(r,ident)
 else:humanoid(r,ident)
 # Flying carriers and shulkers have short native hitboxes at their feet.
 # Bring the visible body into that box instead of making a floating fake target.
 offset=-.85 if ident in ['aviary','heavenly_rider'] else -.65 if ident=='heavenly_challenger' else 0
 for part in r.parts:part['pos'][1]+=offset
 return r

def quaternion(degrees):
 x,y,z=[math.radians(v)/2 for v in degrees]
 cx,cy,cz=math.cos(x),math.cos(y),math.cos(z);sx,sy,sz=math.sin(x),math.sin(y),math.sin(z)
 return [round(sx*cy*cz-cx*sy*sz,6),round(cx*sy*cz+sx*cy*sz,6),round(cx*cy*sz-sx*sy*cz,6),round(cx*cy*cz+sx*sy*sz,6)]

def transform(part, frame=0, pose='idle', phase=1):
 t=list(part['pos']);rot=list(part['rotation']);m=part['motion'];s=part['sign']
 wave=math.sin(frame*math.pi/2);bob=wave*.035
 t[1]+=bob
 if m=='wing':rot[2]+=s*(wave*18+(38 if pose=='wind' else -25 if pose=='recover' else 0))
 elif m in ['leg','spider','tentacle']:
  rot[0]+=s*wave*(14 if pose=='walk' else 5)
  if pose=='wind':rot[2]+=s*12
 elif m in ['arm','blade','fang']:
  rot[0]+=s*wave*5
  if pose=='wind':rot[0]+=65;rot[2]+=s*18
  elif pose=='recover':rot[0]-=35
 elif m=='head':rot[0]+=wave*3+(12 if pose=='recover' else -10 if pose=='wind' else 0)
 elif m=='ring':rot[2]+=frame*90+(45 if phase==2 else 0)
 elif m=='shell':t[1]+=s*(.25 if pose=='wind' else .08+.04*wave)
 elif m=='banner':rot[0]+=wave*5
 elif m=='tail':rot[1]+=wave*12
 elif m=='core':rot[1]+=frame*90
 if pose=='recover':t[1]-=.08
 scale=1.08 if phase==2 and m in ['ring','core','blade'] else 1
 return {'translation':[round(v,4) for v in t],'left_rotation':quaternion(rot),'scale':[scale]*3,'right_rotation':[0,0,0,1]}

def resource_model(rig, part):
 elements=[]
 for cube in part['cubes']:
  c,size=cube['center'],cube['size'];mat=cube['material'];uv=[mat*4,0,mat*4+4,16]
  # Minecraft JSON model geometry is centered at (8,8,8); units are 1/16 block.
  start=[round(8+(v-d/2)*16,3) for v,d in zip(c,size)]
  end=[round(8+(v+d/2)*16,3) for v,d in zip(c,size)]
  assert all(-16<=v<=32 for v in start+end),(rig.ident,part['name'],start,end)
  elements.append({'from':start,'to':end,'faces':{f:{'uv':uv,'texture':'#atlas'} for f in ['north','south','east','west','up','down']}})
 return {'textures':{'atlas':f'ida_boss:boss/{rig.ident}','particle':f'ida_boss:boss/{rig.ident}'},'gui_light':'front','display':{'fixed':{'rotation':[0,0,0],'translation':[0,0,0],'scale':[1,1,1]}},'elements':elements}

def write_atlas():
 # The client only stitches registered sprites. textures/boss is outside the
 # vanilla item directory; model references alone do not register these PNGs.
 write_json(RESOURCE/'assets/minecraft/atlases/items.json',{'sources':[
  {'type':'minecraft:single','resource':f'ida_boss:boss/{ident}','sprite':f'ida_boss:boss/{ident}'} for ident in PALETTES]})

def build(bosses, fn, snbt):
 write_atlas()
 write_json(RESOURCE/'pack.mcmeta',{'pack':{'min_format':[97,1],'max_format':[97,1],'description':'IDA 26.3 — Articulated Boss Models (place ABOVE Integrated RP)'}})
 write_json(RESOURCE/'assets/ida_boss/items/hidden.json',{'model':{'type':'minecraft:empty'}})
 write_json(RESOURCE/'assets/ida_boss/equipment/hidden.json',{'layers':{}})
 roster=[]
 for b in bosses:
  ident=b['id'];rig=make_rig(ident);texture(ident)
  spawn=[]
  for part in rig.parts:
   name=part['name'];model=f'ida_boss:boss/{ident}/{name}'
   write_json(RESOURCE/f'assets/ida_boss/models/boss/{ident}/{name}.json',resource_model(rig,part))
   write_json(RESOURCE/f'assets/ida_boss/items/boss/{ident}/{name}.json',{'model':{'type':'minecraft:model','model':model}})
   payload={'Tags':['ida.visual','ida.visual_new',f'ida.part.{name}'], 'data':{'id':'ID_TOKEN'},
     'item':{'id':'minecraft:paper','count':1,'components':{'minecraft:item_model':model}},
     'item_display':'fixed','billboard':'fixed','width':5.0,'height':5.0,'view_range':1.0,
     'teleport_duration':1,'interpolation_duration':5,'Invulnerable':True,'transformation':transform(part)}
   if part['glow']:payload['brightness']={'block':15,'sky':15}
   spawn += ['$summon minecraft:item_display ~ ~ ~ '+snbt(payload).replace('"ID_TOKEN"','$(id)'),
     'execute as @e[tag=ida.visual_new,limit=1] store result score @s ida.sid run data get entity @s data.id',
     'tag @e[tag=ida.visual_new] remove ida.visual_new']
  fn('visual/'+ident+'/spawn',spawn+['$tp @e[type=minecraft:item_display,tag=ida.visual,scores={ida.sid=$(id)}] ~ ~ ~ ~180 0'])
  for phase in [1,2]:
   for pose in ['idle','walk','wind','recover']:
    for frame in range(4):
     lines=[]
     for part in rig.parts:
      data={'start_interpolation':0,'transformation':transform(part,frame,pose,phase)}
      lines.append(f'$execute as @e[type=minecraft:item_display,tag=ida.visual,tag=ida.part.{part["name"]},scores={{ida.sid=$(id)}}] run data merge entity @s '+snbt(data))
     fn(f'visual/{ident}/{phase}_{pose}_{frame}',lines)
  roster.append({'id':ident,'name':b['name'],'parts':rig.parts,'palette':PALETTES[ident]})
 fn('visual/setup',[
  '$kill @e[tag=ida.visual,scores={ida.sid=$(id)}]',
  'effect give @s minecraft:invisibility infinite 0 true',
  # Keep armor modifiers and the helmet's daylight protection; hide its layers.
  'execute if data entity @s equipment.head run data modify entity @s equipment.head.components."minecraft:equippable" set value {slot:"head",asset_id:"ida_boss:hidden"}',
  'execute if data entity @s equipment.chest run data modify entity @s equipment.chest.components."minecraft:equippable" set value {slot:"chest",asset_id:"ida_boss:hidden"}',
  'execute if data entity @s equipment.legs run data modify entity @s equipment.legs.components."minecraft:equippable" set value {slot:"legs",asset_id:"ida_boss:hidden"}',
  'execute if data entity @s equipment.feet run data modify entity @s equipment.feet.components."minecraft:equippable" set value {slot:"feet",asset_id:"ida_boss:hidden"}',
  'execute if data entity @s equipment.offhand run data modify entity @s equipment.offhand.components."minecraft:item_model" set value "ida_boss:hidden"',
  'execute if data entity @s equipment.mainhand run data modify entity @s equipment.mainhand.components."minecraft:item_model" set value "ida_boss:hidden"',
  'data modify entity @s CustomNameVisible set value 0b',
  'data modify entity @s data.visual_version set value 1',
  '$function dungeons_arise:boss/visual/$(kind)/spawn with entity @s data'])
 fn('visual/tick',[
  'execute store result score @s ida.hp run data get entity @s Health 100',
  'execute if score @s ida.hp matches ..0 run function dungeons_arise:boss/visual/dead with entity @s data',
  'execute if score @s ida.hp matches ..0 run return 0',
  '$execute unless entity @e[type=minecraft:item_display,tag=ida.visual,scores={ida.sid=$(id)},limit=1] run function dungeons_arise:boss/visual/setup with entity @s data',
  '$tp @e[type=minecraft:item_display,tag=ida.visual,scores={ida.sid=$(id)}] ~ ~ ~ ~180 0',
  'execute if score #clock ida.tick matches 5 run function dungeons_arise:boss/visual/animate with entity @s data',
  'execute if score #clock ida.tick matches 10 run function dungeons_arise:boss/visual/animate with entity @s data',
  'execute if score #clock ida.tick matches 15 run function dungeons_arise:boss/visual/animate with entity @s data',
  'execute if score #clock ida.tick matches 20 run function dungeons_arise:boss/visual/animate with entity @s data'])
 fn('visual/animate',[
  'scoreboard players operation #frame ida.tmp = #clock ida.tick',
  'scoreboard players set #five ida.tmp 5','scoreboard players operation #frame ida.tmp /= #five ida.tmp',
  'scoreboard players remove #frame ida.tmp 1',
  'execute if score #frame ida.tmp matches ..-1 run scoreboard players set #frame ida.tmp 0',
  'execute store result entity @s data.frame int 1 run scoreboard players get #frame ida.tmp',
  'execute store result entity @s data.visual_phase int 1 run scoreboard players get @s ida.phase',
  'data modify entity @s data.pose set value "idle"',
  'execute store result score #vx ida.tmp run data get entity @s Motion[0] 1000',
  'execute store result score #vz ida.tmp run data get entity @s Motion[2] 1000',
  'execute unless score #vx ida.tmp matches -5..5 run data modify entity @s data.pose set value "walk"',
  'execute unless score #vz ida.tmp matches -5..5 run data modify entity @s data.pose set value "walk"',
  'execute if score @s ida.stage matches 1 run data modify entity @s data.pose set value "wind"',
  'execute if score @s ida.stage matches 2 run data modify entity @s data.pose set value "recover"',
  'function dungeons_arise:boss/visual/pose with entity @s data'])
 fn('visual/pose',['$function dungeons_arise:boss/visual/$(kind)/$(visual_phase)_$(pose)_$(frame) with entity @s data'])
 # Orphans can result from external /kill commands or unloading different chunks.
 fn('visual/orphan',['$execute unless entity @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1] run kill @s'])
 fn('visual/dead',['$kill @e[tag=ida.visual,scores={ida.sid=$(id)}]'])
 write_json(OUTPUT/'boss-model-roster.json',{'bosses':roster,'animation_hz':4,'interpolation_ticks':5,'resource_format':[97,1]})
 with zipfile.ZipFile(OUTPUT/'IDA-Boss-Models-26.3.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(RESOURCE.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(RESOURCE).as_posix())
 return roster
