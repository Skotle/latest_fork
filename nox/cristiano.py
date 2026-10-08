"""Second independent encounter: desert football boss and Bernabeu-inspired stadium."""
import json,math,gzip
from build import DP,RP,OUT,js
from worldgen import Tag,nbt
from cristiano_art import assets as human_assets, motion as human_motion, PARTS as HUMAN_PARTS
N='desert_ball'
def fn(name,lines):
 p=DP/f'data/{N}/function/{name}.mcfunction';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
def call(name):return f'function {N}:{name}'
def say(s):return 'tellraw @a[tag=db.member] '+json.dumps({'text':s,'color':'gold'},ensure_ascii=False)
def append(namespace,name,lines):
 p=DP/f'data/{namespace}/function/{name}.mcfunction';p.write_text(p.read_text(encoding='utf-8')+'\n'.join(lines)+'\n',encoding='utf-8')
def visual(model,pos,tags):
 return 'summon minecraft:item_display ~ ~ ~ '+json.dumps({'Tags':['db.owned','db.visual',*tags],'Invulnerable':True,'width':0.,'height':0.,'item':{'id':'minecraft:paper','count':1,'components':{'minecraft:item_model':f'{N}:{model}'}},'item_display':'fixed','teleport_duration':1,'interpolation_duration':2,'transformation':{'translation':list(pos),'scale':[1.15]*3,'left_rotation':[0,0,0,1],'right_rotation':[0,0,0,1]}},separators=(',',':'))
def stadium():
 blocks={}
 for x in range(-32,33):
  for z in range(-45,46):
   r=math.hypot(x/32,z/45)
   if r>1.01:continue
   h=max(1,min(14,int((r-.65)*38)))
   for y in range(-2,19):
    b='minecraft:air'
    if y==-2:b='minecraft:smooth_sandstone'
    if y==-1:b='minecraft:green_concrete' if abs(x)<=19 and abs(z)<=29 else 'minecraft:smooth_sandstone'
    if y==-1 and abs(x)<=19 and abs(z)<=29 and (abs(x)==19 or abs(z)==29 or z==0 or abs(math.hypot(x,z)-6)<.45 or (abs(x)<=9 and abs(z) in (20,28))):b='minecraft:white_concrete'
    if r>=.68 and 0<=y<=h:b='minecraft:blue_concrete' if y==h else 'minecraft:smooth_quartz'
    if r>=.96 and y>=0:b='minecraft:iron_block' if y%3==0 else 'minecraft:polished_andesite'
    if .65<r<.72 and y==14:b='minecraft:sea_lantern' if (x+z)%4==0 else 'minecraft:blue_stained_glass'
    if .72<=r<=1 and y==17:b='minecraft:smooth_quartz'
    if .94<r and y==18:b='minecraft:iron_block'
    if abs(x)<=3 and 29<=z<=45 and 0<=y<=4:b='minecraft:air'
    blocks[(x+32,y+2,z+45)]=b
 # Goals, columns for shot cover, dugout arches.
 for z in [-28,28]:
  for x in range(-5,6):
   for y in range(0,5):
    if abs(x)==5 or y==4:blocks[(x+32,y+2,z+45)]='minecraft:white_concrete'
 for x,z in [(-15,-14),(15,14),(-15,14),(15,-14)]:
  for y in range(3):blocks[(x+32,y+2,z+45)]='minecraft:cut_sandstone'
 palette=sorted(set(blocks.values()));ids={s:i for i,s in enumerate(palette)}
 seed={'id':Tag(8,'minecraft:marker'),'Tags':Tag(9,(8,['db.owned','db.seed']))}
 root={'DataVersion':Tag(3,5023),'size':Tag(9,(3,[65,21,91])),'palette':Tag(9,(10,[{'id':Tag(8,s)} for s in palette])),
       'blocks':Tag(9,(10,[{'pos':Tag(9,(3,list(pos))),'state':Tag(3,ids[b])} for pos,b in sorted(blocks.items())])),
       'entities':Tag(9,(10,[{'pos':Tag(9,(6,[32.,2.,45.])), 'blockPos':Tag(9,(3,[32,2,45])), 'nbt':Tag(10,seed)}]))}
 p=DP/f'data/{N}/structure/bernabeu.nbt';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(gzip.compress(nbt(root),mtime=0))
 js(DP/f'data/{N}/worldgen/structure/bernabeu.json',{'type':'minecraft:jigsaw','biomes':'minecraft:desert','step':'surface_structures','spawn_overrides':{'monster':{'bounding_box':'piece','spawns':[]}},'terrain_adaptation':'beard_thin','start_pool':f'{N}:bernabeu','size':1,'start_height':{'absolute':0},'project_start_to_heightmap':'WORLD_SURFACE_WG','max_distance_from_center':100,'use_expansion_hack':False})
 js(DP/f'data/{N}/worldgen/template_pool/bernabeu.json',{'name':f'{N}:bernabeu','fallback':'minecraft:empty','elements':[{'weight':1,'element':{'element_type':'minecraft:single_pool_element','location':f'{N}:bernabeu','processors':'minecraft:empty','projection':'rigid'}}]})
 js(DP/f'data/{N}/worldgen/structure_set/stadiums.json',{'structures':[{'structure':f'{N}:bernabeu','weight':1}],'placement':{'type':'minecraft:random_spread','spacing':40,'separation':20,'salt':73102672}})

 return blocks

PARTS=HUMAN_PARTS
def generate():
 # Remove the previous unlinked 16-frame animation functions from generated output.
 obsolete=DP/f'data/{N}/function/visual/pose'
 for p in obsolete.glob('*.mcfunction'):p.unlink()
 (DP/f'data/{N}/function/visual/jump_frame.mcfunction').unlink(missing_ok=True)
 (RP/f'assets/{N}/textures/entity/player.png').unlink(missing_ok=True)
 stadium();human_assets();js(DP/f'data/{N}/tags/block/pitch.json',{'values':['minecraft:green_concrete','minecraft:white_concrete']})
 append('eclipse_nox','load',[call('load')]);append('eclipse_nox','tick',[f'execute in minecraft:overworld run {call("tick")}',f'execute as @a[scores={{db.debt=1}}] at @s if score #state db.state matches 0 run {call("theft/return")}'])
 p=DP/'data/eclipse_nox/function/fight/start.mcfunction';original=p.read_text();(p.parent/'start_nox.mcfunction').write_text(original);p.write_text(f'execute if score #state db.state matches 0 run function eclipse_nox:fight/start_nox\nexecute if score #state db.state matches 1 run data remove entity @s interaction\n')
 fn('load',[f'scoreboard objectives add db.{o} dummy' for o in ['state','time','cast','skill','safe','hp','max','next','tmp','owner','debt','motion','idle','olddeath','oldleave','cycle','anim']]+[
  f'bossbar add {N}:health {{text:"사막의 볼, 크리스티아누",color:"gold"}}',f'bossbar set {N}:health color yellow',
  'execute unless score #serial db.owner matches 0.. run scoreboard players set #serial db.owner 0',
  'execute unless data storage desert_ball:vault accounts run data modify storage desert_ball:vault accounts set value {}','scoreboard players set #state db.state 0',call('cleanup'),say('크리스티아누 추가 — /locate structure desert_ball:bernabeu')])
 fn('admin/install',['execute if dimension minecraft:overworld if score #state db.state matches 0 run place template desert_ball:bernabeu ~-32 ~-2 ~-45',
  'execute as @e[tag=db.seed,distance=..3] at @s run '+call('site/init')])
 fn('site/init',['tag @s remove db.seed','tag @s add db.anchor',call('site/setup')])
 fn('site/setup',['kill @e[type=minecraft:interaction,tag=db.start,distance=..38]',
  'kill @e[type=minecraft:text_display,tag=db.owned,distance=..40]',
  'setblock ~ ~-1 ~ minecraft:gold_block',
  'summon minecraft:interaction ~ ~ ~ {Tags:["db.owned","db.start"],width:2f,height:2f,response:1b}',
  'summon minecraft:text_display ~ ~3 ~ {Tags:["db.owned","db.sign"],billboard:"center",text:{text:"크리스티아누 소환대\\n금색 블록 바로 위를 우클릭\\n활·석궁 권장",color:"gold"}}',
  'tag @s add db.ready'])
 fn('admin/summon',['execute if dimension minecraft:overworld if score #state nx.state matches 0 if score #state db.state matches 0 as @e[tag=db.anchor,distance=..100,sort=nearest,limit=1] at @s run '+call('begin')])
 fn('tick',['execute as @e[tag=db.seed] at @s if entity @a[distance=..100] run '+call('site/init'),
  'execute as @e[tag=db.anchor,tag=!db.ready] at @s run '+call('site/setup'),
  'execute as @e[tag=db.anchor,tag=db.ready] at @s if score #state db.state matches 0 unless entity @e[tag=db.start,distance=..3] run '+call('site/setup'),
  'execute if score #state db.state matches 0 as @e[tag=db.start] at @s run particle minecraft:end_rod ~ ~.8 ~ .3 .4 .3 0 2 normal @a[distance=..32]',
  'execute if score #state db.state matches 0 as @e[tag=db.start] at @s if data entity @s interaction run '+call('start'),
  'execute if score #state db.state matches 1 as @e[tag=db.anchor,tag=db.current,limit=1] at @s run '+call('fight/tick'),
  'execute if score #state db.state matches 1 unless entity @e[tag=db.anchor,tag=db.current] run '+call('abort')])
 fn('start',['data remove entity @s interaction','execute if score #state nx.state matches 0 if score #state db.state matches 0 as @e[tag=db.anchor,distance=..38,sort=nearest,limit=1] at @s run '+call('begin')])
 fn('begin',['tag @s add db.current','tag @a[distance=..38,gamemode=!spectator,tag=!nox.member] add db.member',
  'execute unless entity @a[tag=db.member] run tag @s remove db.current','execute if entity @a[tag=db.member] run '+call('fight/spawn')])
 fn('fight/spawn',['scoreboard players set #follow db.anim 0','scoreboard players set #moving db.anim 0','scoreboard players set #pending db.tmp 0','scoreboard players set #skill db.skill 1','scoreboard players set #state db.state 1','scoreboard players set #time db.time 0','scoreboard players set #cycle db.cycle 0','scoreboard players set #idle db.idle 0','scoreboard players set #safe db.safe 0','scoreboard players set #cast db.cast 0','scoreboard players set #next db.next 40',
  'scoreboard players set #max db.max 500','execute as @a[tag=db.member] run scoreboard players add #max db.max 250','execute if score #max db.max matches 1251.. run scoreboard players set #max db.max 1250',
  'execute as @a[tag=db.member] run scoreboard players add @s nx.death 0','execute as @a[tag=db.member] run scoreboard players add @s nx.leave 0',
  'execute as @a[tag=db.member] run scoreboard players operation @s db.olddeath = @s nx.death','execute as @a[tag=db.member] run scoreboard players operation @s db.oldleave = @s nx.leave',
  'execute store result storage desert_ball:runtime hp int 1 run scoreboard players get #max db.max',call('fight/carrier')+' with storage desert_ball:runtime',
  *[visual(part,pos,['db.body','db.part.'+part]) for part,pos in PARTS.items()],visual('ball',(0,.45,.65),['db.body','db.carried_ball']),
  f'bossbar set {N}:health players @a[tag=db.member]',f'bossbar set {N}:health visible true',say('베르나베우의 사막 결전! 날강두·젖통닌자·노쇼·꽃게드리블·헤딩골·오버헤드킥')])
 fn('fight/carrier',['$summon minecraft:husk ~ ~ ~ {Tags:["db.owned","db.boss"],NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,CanPickUpLoot:0b,Health:$(hp)f,attributes:[{id:"minecraft:max_health",base:$(hp)},{id:"minecraft:scale",base:1.3},{id:"minecraft:knockback_resistance",base:1.0}],active_effects:[{id:"minecraft:invisibility",duration:2147483647,show_particles:0b}]}'])
 fn('fight/tick',['tag @a remove db.active',
  'execute as @a[tag=db.member,distance=..38,gamemode=!spectator] if score @s nx.death = @s db.olddeath if score @s nx.leave = @s db.oldleave run tag @s add db.active',
  'execute unless entity @a[tag=db.active] run scoreboard players add #idle db.idle 1','execute if entity @a[tag=db.active] run scoreboard players set #idle db.idle 0',
  'execute if score #idle db.idle matches 100.. run '+call('abort'),
  'execute if score #state db.state matches 1 if score #idle db.idle matches ..99 unless entity @e[tag=db.boss] run '+call('victory'),
  'execute if score #state db.state matches 1 if entity @e[tag=db.boss] run '+call('fight/alive')])
 fn('fight/alive',['scoreboard players set #moving db.anim 0','scoreboard players add #time db.time 1','execute store result score #hp db.hp run data get entity @e[tag=db.boss,limit=1] Health 100',
  f'execute store result bossbar {N}:health value run data get entity @e[tag=db.boss,limit=1] Health',f'execute store result bossbar {N}:health max run scoreboard players get #max db.max',
  'execute if score #safe db.safe matches 1.. run scoreboard players remove #safe db.safe 1',
  'execute if score #pending db.tmp matches 1 run '+call('skills/core_tick'),
  'execute if score #cast db.cast matches 1.. run '+call('skills/casting'),
  'execute if score #cast db.cast matches 0 if score #safe db.safe matches 0 run scoreboard players remove #next db.next 1',
  'execute if score #cast db.cast matches 0 if score #safe db.safe matches 0 if score #next db.next matches ..0 if entity @a[tag=db.active] run '+call('skills/begin'),
  'execute if score #time db.time matches 37.. if score #safe db.safe matches 0 if score #skill db.skill matches 1..4 if entity @a[tag=db.active] as @e[tag=db.boss,limit=1] at @s run '+call('fight/move'),
  'execute as @e[tag=db.shot] at @s run '+call('shot/tick'),
  'execute as @e[tag=db.fall] at @s run '+call('shot/fall_tick'),call('visual/tick')])
 fn('fight/move',['execute facing entity @a[tag=db.active,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0',
  'execute if score #skill db.skill matches 4 if score #cast db.cast matches 24.. positioned ^.24 ^ ^ if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air if entity @e[tag=db.anchor,tag=db.current,distance=..28] store success score #moving db.anim run tp @s ~ ~ ~',
  'execute if score #skill db.skill matches 4 if score #cast db.cast matches ..23 positioned ^-.24 ^ ^ if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air if entity @e[tag=db.anchor,tag=db.current,distance=..28] store success score #moving db.anim run tp @s ~ ~ ~',
  'execute unless score #skill db.skill matches 4 if entity @a[tag=db.active,distance=..10] positioned ^ ^ ^-.18 if block ~ ~ ~ minecraft:air if entity @e[tag=db.anchor,tag=db.current,distance=..28] store success score #moving db.anim run tp @s ~ ~ ~'])
 fn('skills/begin',['kill @e[tag=db.core]','kill @e[tag=db.core_visual]','scoreboard players set #pending db.tmp 0','scoreboard players add #cycle db.cycle 1','execute if score #cycle db.cycle matches 7.. run scoreboard players set #cycle db.cycle 1','scoreboard players operation #skill db.skill = #cycle db.cycle',
  'scoreboard players operation #ratio db.tmp = #hp db.hp','scoreboard players operation #ratio db.tmp /= #max db.max',
  'execute if score #ratio db.tmp matches 66.. if score #skill db.skill matches 2 run scoreboard players set #skill db.skill 4','execute if score #ratio db.tmp matches 66.. if score #skill db.skill matches 3 run scoreboard players set #skill db.skill 5','execute if score #ratio db.tmp matches 31.. if score #skill db.skill matches 6 run scoreboard players set #skill db.skill 5',
  'scoreboard players set #cast db.cast 24','scoreboard players set #next db.next 12','execute if score #skill db.skill matches 2 run scoreboard players set #cast db.cast 40','execute if score #skill db.skill matches 3 run scoreboard players set #cast db.cast 40','execute if score #skill db.skill matches 4 run scoreboard players set #cast db.cast 36','execute if score #skill db.skill matches 5..6 run scoreboard players set #cast db.cast 30',
  'execute as @e[tag=db.boss,limit=1] at @s facing entity @a[tag=db.active,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0',
  'kill @e[tag=db.jump_origin]','execute at @e[tag=db.boss,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["db.owned","db.jump_origin"]}',
  'execute if score #skill db.skill matches 1 run '+say('날강두! 소지품을 노린다. 슈팅을 피하고 도주하는 몸통을 사격하세요.'),
  'execute if score #skill db.skill matches 2 run '+say('젖통닌자! 모래 연막 — 재등장 발자국과 가슴 표식을 사격하세요.'),
  'execute if score #skill db.skill matches 3 run '+call('skills/noshow'),
  'execute if score #skill db.skill matches 5 run '+say('헤딩골! 떠오른 공을 맞히면 2초 기절합니다.'),'execute if score #skill db.skill matches 6 run '+say('오버헤드킥! 준비 공을 사격하거나 착탄 예고 밖으로 이동하세요.'),
  'execute if score #skill db.skill matches 5..6 at @e[tag=db.boss,limit=1] run '+call('skills/core_spawn')])
 fn('skills/casting',['scoreboard players remove #cast db.cast 1','execute if score #skill db.skill matches 2 if score #cast db.cast matches 39 at @e[tag=db.boss,limit=1] run '+call('skills/hide'),
  'execute if score #skill db.skill matches 2 if score #cast db.cast matches 14 run '+call('skills/ambush_warn'),
  'execute if score #skill db.skill matches 4 if score #cast db.cast matches 24 run '+call('skills/curve_left'),
  'execute if score #skill db.skill matches 4 if score #cast db.cast matches 12 run '+call('skills/curve_right'),
  'execute if score #skill db.skill matches 1 if score #cast db.cast matches 12 run '+call('skills/shoot'),
  'execute if score #skill db.skill matches 5 if score #cast db.cast matches 10 run '+call('skills/launch_header'),
  'execute if score #skill db.skill matches 6 if score #cast db.cast matches 14 run '+call('skills/launch_overhead'),
  'execute if score #cast db.cast matches 0 run '+call('skills/resolve')])
 fn('skills/launch_header',['scoreboard players set #pending db.tmp 0','kill @e[tag=db.core]','kill @e[tag=db.core_visual]',call('skills/shoot')])
 fn('skills/launch_overhead',['scoreboard players set #pending db.tmp 0','kill @e[tag=db.core]','kill @e[tag=db.core_visual]',call('skills/overhead')])
 fn('skills/hide',['particle minecraft:cloud ~ ~1 ~ .6 1 .6 .08 40 force @a[tag=db.member]','tp @s ~ ~-5 ~'])
 fn('skills/ambush_warn',['kill @e[tag=db.ambush]','kill @e[tag=db.jump_origin]','execute as @a[tag=db.active,sort=random,limit=1] at @s rotated as @s rotated ~ 0 positioned ^ ^ ^-3 run summon minecraft:marker ~ ~ ~ {Tags:["db.owned","db.ambush"]}',
  'execute at @e[tag=db.ambush,limit=1] run particle minecraft:dust{color:[0.9,0.7,0.35],scale:2.0} ~ ~.1 ~ .6 0 .6 0 22 force @a[tag=db.member]',
  'playsound minecraft:entity.villager.celebrate master @a[tag=db.member] ~ ~ ~ .8 .7'])
 fn('skills/noshow',[say('노쇼! 공을 갖고 있는 진짜를 찾아 사격하면 도난품을 되찾습니다.'),
  *[f'execute at @e[tag=db.boss,limit=1] run '+visual(part,pos,['db.decoy']) for part,pos in PARTS.items()],
  'execute as @e[tag=db.boss,limit=1] at @e[tag=db.anchor,tag=db.current,limit=1] run tp @s ~12 ~ ~-18',
  'execute as @a[tag=db.active,sort=random,limit=1] run '+call('theft/attempt')])
 fn('skills/resolve',['execute if score #skill db.skill matches 5..6 as @e[tag=db.boss,limit=1] at @e[tag=db.jump_origin,limit=1] run tp @s ~ ~ ~','scoreboard players set #pending db.tmp 0','kill @e[tag=db.core]','kill @e[tag=db.core_visual]','scoreboard players set #safe db.safe 10',
  'execute if score #skill db.skill matches 2 run '+call('skills/ambush'),
  'execute if score #skill db.skill matches 4 run '+call('skills/shoot')])
 fn('skills/ambush',['scoreboard players set #follow db.anim 12','execute as @e[tag=db.boss,limit=1] at @e[tag=db.ambush,limit=1] run tp @s ~ ~ ~',
  'execute at @e[tag=db.boss,limit=1] as @a[tag=db.active,distance=..4] run damage @s 4 minecraft:mob_attack by @e[tag=db.boss,limit=1]',
  'execute at @e[tag=db.boss,limit=1] as @a[tag=db.active,distance=..4,sort=nearest,limit=1] run '+call('theft/attempt'),
  'execute at @e[tag=db.boss,limit=1] run '+call('skills/core_spawn'),'execute as @e[tag=db.core,limit=1] at @e[tag=db.boss,limit=1] run tp @s ~ ~1.1 ~'])
 fn('skills/core_spawn',['scoreboard players set #pending db.tmp 1','summon minecraft:slime ~ ~2.6 ~ {Tags:["db.owned","db.core"],Size:0,NoAI:1b,NoGravity:1b,Silent:1b,Health:8f,attributes:[{id:"minecraft:max_health",base:8}],active_effects:[{id:"minecraft:invisibility",duration:2147483647,show_particles:0b}]}',visual('ball',(0,0,0),['db.core_visual'])])
 fn('skills/core_tick',['scoreboard players set #core db.tmp 0','execute store result score #core db.tmp run data get entity @e[tag=db.core,limit=1] Health 100',
  'execute as @e[tag=db.core_visual] at @e[tag=db.core,limit=1] run tp @s ~ ~.25 ~',
  'execute if score #core db.tmp matches ..799 run '+call('skills/counter')])
 fn('skills/counter',['execute if score #skill db.skill matches 5..6 as @e[tag=db.boss,limit=1] at @e[tag=db.jump_origin,limit=1] run tp @s ~ ~ ~','scoreboard players set #pending db.tmp 0','kill @e[tag=db.core]','kill @e[tag=db.core_visual]','scoreboard players set #cast db.cast 0','scoreboard players set #safe db.safe 40','scoreboard players set #next db.next 4',
  'execute as @a[scores={db.debt=1}] at @s run '+call('theft/return'),say('공을 맞혔다! 2초 기절 — 도난품 반환!')])
 fn('skills/shoot',['execute as @e[tag=db.boss,limit=1] at @s facing entity @a[tag=db.active,sort=nearest,limit=1] eyes run tp @s ~ ~ ~ ~ 0',
  'execute at @e[tag=db.boss,limit=1] rotated as @e[tag=db.boss,limit=1] positioned ~ ~1.1 ~ run summon minecraft:marker ~ ~ ~ {Tags:["db.owned","db.shot","db.newshot"]}',
  'execute if score #skill db.skill matches 5 as @e[tag=db.newshot] at @e[tag=db.boss,limit=1] run tp @s ~ ~2.45 ~',
  'execute if score #skill db.skill matches 6 as @e[tag=db.newshot] at @e[tag=db.boss,limit=1] run tp @s ~ ~1.9 ~',
  'execute as @e[tag=db.newshot] rotated as @e[tag=db.boss,limit=1] run tp @s ~ ~ ~ ~ 0','scoreboard players set @e[tag=db.newshot] db.time 45','scoreboard players operation @e[tag=db.newshot] db.skill = #skill db.skill',
  'execute at @e[tag=db.newshot,limit=1] run '+visual('ball',(0,0,0),['db.shot_visual','db.newvisual']),
  'scoreboard players add #ball db.owner 1','scoreboard players operation @e[tag=db.newshot] db.owner = #ball db.owner','scoreboard players operation @e[tag=db.newvisual] db.owner = #ball db.owner',
  'execute as @e[tag=db.newshot] at @s facing entity @a[tag=db.active,sort=nearest,limit=1] eyes run tp @s ~ ~ ~ ~ ~','tag @e[tag=db.newshot] remove db.newshot','tag @e[tag=db.newvisual] remove db.newvisual'])
 fn('skills/curve_left',[call('skills/shoot'),'tag @e[tag=db.shot,scores={db.time=45},sort=nearest,limit=1] add db.curve_left'])
 fn('skills/curve_right',[call('skills/shoot'),'tag @e[tag=db.shot,scores={db.time=45},sort=nearest,limit=1] add db.curve_right'])
 fn('shot/tick',['scoreboard players remove @s db.time 1','execute if entity @s[tag=db.curve_left] run tp @s ~ ~ ~ ~-3 ~','execute if entity @s[tag=db.curve_right] run tp @s ~ ~ ~ ~3 ~',
  'tp @s ^ ^ ^.85','scoreboard players operation #ballid db.owner = @s db.owner',
  'execute as @e[tag=db.shot_visual] if score @s db.owner = #ballid db.owner run tp @s ~ ~ ~',
  'particle minecraft:crit ~ ~ ~ .1 .1 .1 0 2 force @a[tag=db.member]',
  'execute if entity @a[tag=db.active,distance=..1.2] run '+call('shot/hit'),
  'execute unless block ~ ~ ~ minecraft:air run scoreboard players set @s db.time 0',
  'execute if score @s db.time matches ..0 run '+call('shot/remove')])
 fn('shot/hit',['execute if score @s db.skill matches 1 as @a[tag=db.active,distance=..1.2,sort=nearest,limit=1] run '+call('theft/attempt'),'damage @a[tag=db.active,distance=..1.2,sort=nearest,limit=1] 3 minecraft:magic by @e[tag=db.boss,limit=1]','scoreboard players set @s db.time 0'])
 fn('shot/remove',['scoreboard players operation #ballid db.owner = @s db.owner','execute as @e[tag=db.shot_visual] if score @s db.owner = #ballid db.owner run kill @s','kill @s'])
 fn('skills/overhead',[say('오버헤드킥! 표시된 착탄점 밖으로 이동하거나 준비 공을 사격하세요.'),
  'execute as @a[tag=db.active] at @s run summon minecraft:marker ~ ~ ~ {Tags:["db.owned","db.fall","db.newfall"]}','scoreboard players set @e[tag=db.newfall] db.time 20','tag @e[tag=db.newfall] remove db.newfall',
  'execute at @e[tag=db.boss,limit=1] run '+call('skills/shoot')])
 fn('shot/fall_tick',['scoreboard players remove @s db.time 1','particle minecraft:flame ~ ~.1 ~ 2 0 2 0 14 force @a[tag=db.member]',
  'execute if score @s db.time matches ..0 as @a[tag=db.active,distance=..2.5] run damage @s 4 minecraft:magic by @e[tag=db.boss,limit=1]',
  'execute if score @s db.time matches ..0 run kill @s'])
 # Any actual ranged hit on the boss refunds carried items. The smaller ball is an interrupt target.
 js(DP/f'data/{N}/advancement/internal/hit.json',{'criteria':{'hit':{'trigger':'minecraft:player_hurt_entity','conditions':{'entity':{'type':'minecraft:entity_properties','entity':'this','predicate':{'minecraft:nbt':'{Tags:["db.boss"]}'}},'damage':{'taken':{'min':.001}}}}},'rewards':{'function':f'{N}:hit'}})
 fn('hit',[f'advancement revoke @s only {N}:internal/hit','execute if entity @s[tag=db.active] if score #state db.state matches 1 as @a[scores={db.debt=1}] at @s run '+call('theft/return'),
  'execute if score #skill db.skill matches 3 run kill @e[tag=db.decoy]'])
 fn('victory',[say('사막의 볼을 꺾었다! 도난품을 반환합니다.'),'execute as @a[tag=db.active] run give @s minecraft:golden_boots[minecraft:item_name={text:"크리스티아누의 황금 축구화",color:"gold"}]',call('abort')])
 fn('abort',['scoreboard players set #state db.state 0','execute as @a[scores={db.debt=1}] at @s run '+call('theft/return'),call('cleanup')])
 fn('cleanup',['scoreboard players set #pending db.tmp 0','kill @e[tag=db.boss]','kill @e[tag=db.visual]','kill @e[tag=db.core]','kill @e[tag=db.shot]','kill @e[tag=db.fall]','kill @e[tag=db.ambush]','kill @e[tag=db.jump_origin]',f'bossbar set {N}:health visible false','tag @e[tag=db.current] remove db.current','tag @a remove db.member','tag @a remove db.active','scoreboard players set #cast db.cast 0'])
 theft();human_motion(fn,call)
 js(OUT/'Cristiano-guide.json',{'namespace':N,'arena':'Bernabeu-inspired 65 x 91 surface desert stadium','install':'/function desert_ball:admin/install','locate':'/locate structure desert_ball:bernabeu','abort':'/function desert_ball:abort','boss_health':{'solo':750,'max':1250},'skills':['날강두','젖통닌자','노쇼','꽃게드리블','헤딩골','오버헤드킥'],'theft':'One non-protected item per player; complete components preserved; persistent offline refund ledger','limitations':['No connected-player projectile or theft inventory playtest; server engine checks are separate.']})

def theft():
 js(DP/f'data/{N}/tags/item/protected.json',{'values':['#minecraft:swords','#minecraft:axes','#minecraft:pickaxes','#minecraft:shovels','#minecraft:hoes','minecraft:bow','minecraft:crossbow','minecraft:trident','minecraft:mace','minecraft:shield','minecraft:elytra','#minecraft:head_armor','#minecraft:chest_armor','#minecraft:leg_armor','#minecraft:foot_armor']})
 js(DP/f'data/{N}/item_modifier/take_one.json',{'type':'minecraft:set_count','count':-1,'add':True})
 slots=['weapon.mainhand']+[f'inventory.{i}' for i in range(27)]+[f'hotbar.{i}' for i in range(9)]
 fn('theft/attempt',['execute unless score @s db.debt matches 1 run '+call('theft/choose')])
 fn('theft/choose',['scoreboard players set #captured db.tmp 0',
  'execute unless score @s db.owner matches 1.. run scoreboard players add #serial db.owner 1','execute unless score @s db.owner matches 1.. run scoreboard players operation @s db.owner = #serial db.owner']+
  [f'execute if score #captured db.tmp matches 0 if items entity @s {slot} * unless items entity @s {slot} #{N}:protected run '+call(f'theft/slot/{i}') for i,slot in enumerate(slots)])
 for i,slot in enumerate(slots):
  fn(f'theft/slot/{i}',['summon minecraft:item_display ~ ~ ~ {Tags:["db.capture"],view_range:0f}',
   f'item replace entity @e[tag=db.capture,limit=1] contents from entity @s {slot}',
   'data modify storage desert_ball:capture stack set from entity @e[tag=db.capture,limit=1] item','data modify storage desert_ball:capture stack.count set value 1',
   'data modify storage desert_ball:capture uuid set from entity @s UUID',
   'execute store result storage desert_ball:ctx owner int 1 run scoreboard players get @s db.owner',
   call('theft/save')+' with storage desert_ball:ctx',
   f'item modify entity @s {slot} desert_ball:take_one','scoreboard players set @s db.debt 1','scoreboard players set #captured db.tmp 1','kill @e[tag=db.capture]',
   'tellraw @s {text:"아이템 1개 도난! 보스나 준비 공을 맞히면 반환됩니다. 무기·방어구는 보호됩니다.",color:"red"}'])
 fn('theft/save',['$data modify storage desert_ball:vault accounts.p$(owner) set from storage desert_ball:capture'])
 fn('theft/return',['execute store result storage desert_ball:ctx owner int 1 run scoreboard players get @s db.owner',call('theft/read')+' with storage desert_ball:ctx',
  'execute store success score #returned db.tmp run '+call('theft/drop')+' with storage desert_ball:capture',
  'execute if score #returned db.tmp matches 1 run '+call('theft/delete')+' with storage desert_ball:ctx','execute if score #returned db.tmp matches 1 run scoreboard players set @s db.debt 0'])
 fn('theft/read',['data remove storage desert_ball:capture stack','data remove storage desert_ball:capture uuid','$data modify storage desert_ball:capture stack set from storage desert_ball:vault accounts.p$(owner).stack','$data modify storage desert_ball:capture uuid set from storage desert_ball:vault accounts.p$(owner).uuid'])
 fn('theft/drop',['$summon minecraft:item ~ ~.8 ~ {Item:$(stack),Owner:$(uuid),PickupDelay:0s,Age:-32768s,Invulnerable:1b,Tags:["db.refund"]}'])
 fn('theft/delete',['$data remove storage desert_ball:vault accounts.p$(owner)'])

