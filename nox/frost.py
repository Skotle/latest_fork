"""Vanilla visible Stray boss, physical arrows, telegraphed overhead bombardment."""
import gzip,json
from build import DP,OUT,js
from worldgen import Tag,nbt
N='frost_warden'
def fn(name,lines):
 p=DP/f'data/{N}/function/{name}.mcfunction';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
def call(name):return f'function {N}:{name}'
def append(ns,name,lines):
 p=DP/f'data/{ns}/function/{name}.mcfunction';p.write_text(p.read_text()+'\n'.join(lines)+'\n',encoding='utf-8')
def message(s):return 'tellraw @a[tag=fw.member] '+json.dumps({'text':s,'color':'aqua'},ensure_ascii=False)
def arena():
 blocks={}
 for x in range(35):
  for z in range(35):
   for y in range(13):
    b='minecraft:air'
    if y==0:b='minecraft:stone_bricks'
    if y==1:b='minecraft:packed_ice' if 12<=x<=22 and 12<=z<=22 else 'minecraft:stone_bricks'
    if (x in (0,34) or z in (0,34)) and 2<=y<=4:b='minecraft:stone_bricks'
    if z>=30 and 13<=x<=21 and y<=5:b='minecraft:stone_bricks'
    if z>=29 and 13<=x<=21 and y==6:b='minecraft:spruce_planks'
    if 15<=x<=19 and z>=30 and 7<=y<=9 and (x in (15,19) or z==34):b='minecraft:stone_bricks'
    if 15<=x<=19 and z>=30 and y==10:b='minecraft:spruce_planks'
    if (x,z) in [(8,9),(26,9),(8,24),(26,24)] and 2<=y<=5:b='minecraft:stone_bricks'
    if 3<=x<=7 and z in (16,18) and y in (2,3):b='minecraft:stone_bricks'
    if 27<=x<=31 and z in (16,18) and y in (2,3):b='minecraft:stone_bricks'
    if x in range(15,20) and z in (0,1) and 2<=y<=4:b='minecraft:air'
    if x in range(16,19) and 25<=z<=29 and 2<=y<=z-23:b='minecraft:stone_bricks'
    blocks[(x,y,z)]=b
 palette=sorted(set(blocks.values()));ids={b:i for i,b in enumerate(palette)}
 seed={'id':Tag(8,'minecraft:marker'),'Tags':Tag(9,(8,['fw.site_seed']))}
 root={'DataVersion':Tag(3,5023),'size':Tag(9,(3,[35,13,35])),
 'palette':Tag(9,(10,[{'id':Tag(8,b)} for b in palette])),
 'blocks':Tag(9,(10,[{'pos':Tag(9,(3,list(pos))),'state':Tag(3,ids[b])} for pos,b in blocks.items()])),
 'entities':Tag(9,(10,[{'pos':Tag(9,(6,[17.,2.,17.])), 'blockPos':Tag(9,(3,[17,2,17])), 'nbt':Tag(10,seed)}]))}
 p=DP/f'data/{N}/structure/watchtower.nbt';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(gzip.compress(nbt(root),mtime=0))
 js(DP/f'data/{N}/tags/worldgen/biome/sites.json',{'values':['minecraft:snowy_plains','minecraft:snowy_taiga','minecraft:frozen_peaks','minecraft:jagged_peaks','minecraft:snowy_slopes']})
 js(DP/f'data/{N}/worldgen/structure/watchtower.json',{'type':'minecraft:jigsaw','biomes':f'#{N}:sites','step':'surface_structures','spawn_overrides':{},'terrain_adaptation':'beard_thin','start_pool':f'{N}:watchtower','size':1,'start_height':{'absolute':0},'project_start_to_heightmap':'WORLD_SURFACE_WG','max_distance_from_center':80,'use_expansion_hack':False})
 js(DP/f'data/{N}/worldgen/template_pool/watchtower.json',{'name':f'{N}:watchtower','fallback':'minecraft:empty','elements':[{'weight':1,'element':{'element_type':'minecraft:single_pool_element','location':f'{N}:watchtower','processors':'minecraft:empty','projection':'rigid'}}]})
 js(DP/f'data/{N}/worldgen/structure_set/watchtowers.json',{'structures':[{'structure':f'{N}:watchtower','weight':1}],'placement':{'type':'minecraft:random_spread','spacing':32,'separation':12,'salt':73102683}})
def generate():
 arena()
 js(DP/f'data/{N}/enchantment/own_arrow_guard.json',{'description':{'text':'파수꾼 자기 화살 보호'},'supported_items':['minecraft:iron_helmet'],'weight':1,'max_level':1,'min_cost':{'base':1,'per_level_above_first':0},'max_cost':{'base':1,'per_level_above_first':0},'anvil_cost':0,'slots':['head'],'effects':{'minecraft:damage_immunity':[{'effect':{},'requirements':{'type':'minecraft:damage_source_properties','predicate':{'source_entity':{'minecraft:nbt':'{Tags:["fw.boss"]}'}}}}]}})
 js(DP/f'data/{N}/damage_type/burst.json',{'exhaustion':0.1,'message_id':'explosion','scaling':'always'})
 js(DP/'data/minecraft/tags/damage_type/bypasses_shield.json',{'replace':False,'values':[f'{N}:burst']})
 js(DP/'data/minecraft/tags/damage_type/is_explosion.json',{'replace':False,'values':[f'{N}:burst']})
 js(DP/f'data/{N}/tags/block/blast_pass.json',{'values':['minecraft:air','minecraft:cave_air','minecraft:void_air','minecraft:water','minecraft:snow','minecraft:short_grass','minecraft:fern','minecraft:torch','minecraft:soul_torch']})
 append('eclipse_nox','load',[call('load')]);append('eclipse_nox','tick',['execute in minecraft:overworld run '+call('tick')])
 p=DP/'data/eclipse_nox/function/fight/start.mcfunction';s=p.read_text();s=s.replace('if score #state db.state matches 0 run','if score #state db.state matches 0 if score #state fw.state matches 0 run');p.write_text(s)
 p=DP/'data/desert_ball/function/admin/summon.mcfunction';s=p.read_text().replace('if score #state nx.state matches 0','if score #state nx.state matches 0 if score #state fw.state matches 0');p.write_text(s)
 fn('load',[*[f'scoreboard objectives add fw.{x} dummy' for x in ['state','time','cast','next','skill','cycle','phase','hp','max','tmp','id','age','safe','hits','shield','adds','olddeath','oldleave','blink','stun']],
 'team add fw.enemies','team modify fw.enemies friendlyFire false',
 'bossbar add frost_warden:health {text:"서리의 파수꾼",color:"aqua"}','bossbar set frost_warden:health color blue',
 'scoreboard players set #state fw.state 0','execute unless score #serial fw.id matches 0.. run scoreboard players set #serial fw.id 0',call('cleanup')])
 fn('sun/protect',['execute unless entity @s[tag=fw.sunproof] run data merge entity @s {Fire:-1s}',
 'execute unless items entity @s armor.head minecraft:iron_helmet[minecraft:unbreakable] run item replace entity @s armor.head with minecraft:iron_helmet[minecraft:unbreakable={}]',
 'execute if entity @s[tag=fw.boss] unless items entity @s armor.head minecraft:iron_helmet[minecraft:enchantments~[{enchantments:"frost_warden:own_arrow_guard",levels:{min:1}}]] run item replace entity @s armor.head with minecraft:iron_helmet[minecraft:unbreakable={},minecraft:enchantments={"frost_warden:own_arrow_guard":1}]','tag @s add fw.sunproof'])
 fn('admin/install',['execute if dimension minecraft:overworld if score #state fw.state matches 0 run place template frost_warden:watchtower ~-17 ~-2 ~-17','execute as @e[tag=fw.site_seed,distance=..3] at @s run '+call('site/init')])
 fn('site/init',['tag @s remove fw.site_seed','tag @s add fw.anchor',call('site/setup')])
 fn('site/setup',['setblock ~ ~1 ~ minecraft:target','summon minecraft:text_display ~ ~3.5 ~ {Tags:["fw.site_sign"],billboard:"center",text:{text:"서리의 파수꾼\\n표적에 화살을 쏘면 결전 시작\\n폭격 표식을 보면 즉시 이동",color:"aqua"}}','tag @s add fw.ready'])
 fn('admin/summon',['execute if dimension minecraft:overworld as @e[tag=fw.anchor,distance=..40,sort=nearest,limit=1] at @s run '+call('start')])
 fn('tick',['execute as @e[tag=fw.boss] run '+call('sun/protect'),'execute as @e[tag=fw.add] run '+call('sun/protect'),'execute as @e[tag=fw.site_seed] at @s if entity @a[distance=..100] run '+call('site/init'),
 'execute as @e[tag=fw.anchor,tag=!fw.ready] at @s run '+call('site/setup'),
 'execute if score #state fw.state matches 0 as @e[tag=fw.anchor] at @s unless block ~ ~1 ~ minecraft:target[power=0] if block ~ ~1 ~ minecraft:target run '+call('start'),
 'execute if score #state fw.state matches 1 as @e[tag=fw.anchor,tag=fw.current,limit=1] at @s run '+call('fight/tick'),
 'execute if score #state fw.state matches 1 unless entity @e[tag=fw.anchor,tag=fw.current] run '+call('abort')])
 fn('start',['execute if score #state nx.state matches 0 if score #state db.state matches 0 if score #state fw.state matches 0 run '+call('begin')])
 fn('begin',['tag @s add fw.current','tag @a[distance=..25,gamemode=!spectator] add fw.member',
 'execute unless entity @a[tag=fw.member] run tag @s remove fw.current','execute if entity @a[tag=fw.member] run '+call('fight/spawn')])
 fn('fight/spawn',['scoreboard players set #state fw.state 1','scoreboard players set #time fw.time 0','scoreboard players set #idle fw.tmp 0',
 'scoreboard players set #cast fw.cast 0','scoreboard players set #safe fw.safe 0','scoreboard players set #next fw.next 36','scoreboard players set #cycle fw.cycle 0','scoreboard players set #phase fw.phase 1',
 'scoreboard players set #max fw.max 600','execute as @a[tag=fw.member] run scoreboard players add #max fw.max 600','execute if score #max fw.max matches 2401.. run scoreboard players set #max fw.max 2400',
 'execute store result storage frost_warden:ctx hp int 1 run scoreboard players get #max fw.max',call('fight/carrier')+' with storage frost_warden:ctx',
 'scoreboard players operation #pool fw.hp = #max fw.max','scoreboard players set #hundred fw.tmp 100','scoreboard players operation #pool fw.hp *= #hundred fw.tmp', 'scoreboard players set #last fw.hp 100000',
 'execute as @a[tag=fw.member] run scoreboard players add @s nx.death 0','execute as @a[tag=fw.member] run scoreboard players add @s nx.leave 0',
 'execute as @a[tag=fw.member] run scoreboard players operation @s fw.olddeath = @s nx.death','execute as @a[tag=fw.member] run scoreboard players operation @s fw.oldleave = @s nx.leave',
 'scoreboard players set @a[tag=fw.member] fw.hits 0','scoreboard players set @a[tag=fw.member] fw.shield 0','scoreboard players set #adds fw.adds 0',
 'execute as @a[tag=fw.member] run advancement grant @s only frost_warden:root',
 'bossbar set frost_warden:health players @a[tag=fw.member]','bossbar set frost_warden:health visible true',message('서리의 파수꾼! 폭발 화살·머리 위 폭격 — 표식을 보고 이동하고 장전 중 반격하세요.')])
 fn('fight/carrier',['summon minecraft:stray ~ ~ ~6 {Tags:["fw.owned","fw.boss"],PersistenceRequired:1b,CanPickUpLoot:0b,Health:1000f,attributes:[{id:"minecraft:max_health",base:1000},{id:"minecraft:follow_range",base:40},{id:"minecraft:movement_speed",base:0.32},{id:"minecraft:knockback_resistance",base:0.65}],equipment:{mainhand:{id:"minecraft:bow",count:1,components:{"minecraft:enchantments":{"minecraft:piercing":1}}},head:{id:"minecraft:iron_helmet",count:1,components:{"minecraft:unbreakable":{},"minecraft:enchantments":{"frost_warden:own_arrow_guard":1}}}},drop_chances:{mainhand:0.0f,head:0.0f},CustomName:{text:"서리의 파수꾼",color:"aqua"},CustomNameVisible:1b}',
 'team join fw.enemies @e[tag=fw.boss]','data modify storage frost_warden:ctx owner set from entity @e[tag=fw.boss,limit=1] UUID'])
 fn('fight/tick',['tag @a remove fw.active','execute as @a[tag=fw.member,distance=..25,gamemode=!spectator] if score @s nx.death = @s fw.olddeath if score @s nx.leave = @s fw.oldleave run tag @s add fw.active',
 'execute if entity @a[tag=fw.active,gamemode=!creative] run scoreboard players set #idle fw.tmp 0','execute unless entity @a[tag=fw.active,gamemode=!creative] run scoreboard players add #idle fw.tmp 1',
 'execute if score #idle fw.tmp matches 200.. run '+call('abort'),
 'execute if score #state fw.state matches 1 unless entity @e[tag=fw.boss] run '+call('victory'),
 'execute if score #state fw.state matches 1 if entity @e[tag=fw.boss] run '+call('fight/alive')])
 fn('fight/alive',['scoreboard players add #time fw.time 1','execute store result score #hp fw.hp run data get entity @e[tag=fw.boss,limit=1] Health 100',
 'scoreboard players operation #loss fw.hp = #last fw.hp','scoreboard players operation #loss fw.hp -= #hp fw.hp', 'execute if score #loss fw.hp matches 1.. run scoreboard players operation #pool fw.hp -= #loss fw.hp',
 'execute if score #pool fw.hp matches ..0 run return run '+call('victory'),
 'data merge entity @e[tag=fw.boss,limit=1] {Health:1000f}', 'scoreboard players set #last fw.hp 100000','scoreboard players operation #hp fw.hp = #pool fw.hp',
 'scoreboard players operation #ratio fw.tmp = #hp fw.hp','scoreboard players operation #ratio fw.tmp /= #max fw.max',
 'execute if score #phase fw.phase matches 1 if score #ratio fw.tmp matches ..70 run '+call('phase/two'),
 'execute if score #phase fw.phase matches 2 if score #ratio fw.tmp matches ..35 run '+call('phase/three'),
 'scoreboard players operation #bar fw.hp = #pool fw.hp','scoreboard players operation #bar fw.hp /= #hundred fw.tmp','execute store result bossbar frost_warden:health value run scoreboard players get #bar fw.hp','execute store result bossbar frost_warden:health max run scoreboard players get #max fw.max',
 'execute as @e[tag=fw.add,nbt={Health:0.0f}] at @s run '+call('adds/death'),
 'execute if score #safe fw.safe matches 1.. run scoreboard players remove #safe fw.safe 1',
 'execute if score #cast fw.cast matches 1.. run '+call('skills/casting'),
 'execute if score #cast fw.cast matches 0 if score #safe fw.safe matches 0 run scoreboard players remove #next fw.next 1',
 'execute if score #cast fw.cast matches 0 if score #safe fw.safe matches 0 if score #next fw.next matches ..0 if entity @a[tag=fw.active,gamemode=!creative] run '+call('skills/begin'),
 call('arrows/native')+' with storage frost_warden:ctx','execute as @e[tag=fw.arrow] at @s run '+call('arrows/tick'),
 'execute as @e[tag=fw.add] run '+call('arrows/add_scan'),
 'execute as @e[tag=fw.tracker] at @s run '+call('arrows/tracker'),'execute as @e[tag=fw.bomb_mark] at @s run '+call('bomb/tick')])
 fn('phase/two',['scoreboard players set #phase fw.phase 2',call('adds/spawn'),message('눈보라 강화! 머리 위 폭격이 시작됩니다.')])
 fn('phase/three',['scoreboard players set #phase fw.phase 3',call('adds/spawn'),message('최후의 사선! 공격 사이 대기가 0.3초로 줄어듭니다.')])
 fn('adds/spawn',['execute store result score #count fw.tmp run execute if entity @e[tag=fw.add]', 'execute if score #count fw.tmp matches ..1 positioned ~8 ~ ~8 run summon minecraft:stray ~ ~ ~ {Tags:["fw.owned","fw.add"],PersistenceRequired:1b,Health:50f,attributes:[{id:"minecraft:max_health",base:50}],CanPickUpLoot:0b,equipment:{mainhand:{id:"minecraft:bow",count:1},head:{id:"minecraft:iron_helmet",count:1,components:{"minecraft:unbreakable":{}}}},drop_chances:{head:0.0f}}',
 'team join fw.enemies @e[tag=fw.add]'])
 fn('adds/death',['execute as @a[tag=fw.active,distance=..25,sort=nearest,limit=1] run effect give @s minecraft:speed 4 0 true','tag @s remove fw.add'])
 fn('skills/begin',['scoreboard players add #cycle fw.cycle 1','execute if score #cycle fw.cycle matches 8.. run scoreboard players set #cycle fw.cycle 1','scoreboard players operation #skill fw.skill = #cycle fw.cycle',
 'execute if score #phase fw.phase matches 1 if score #skill fw.skill matches 3 run scoreboard players set #skill fw.skill 2',
 'scoreboard players set #cast fw.cast 28','scoreboard players set #next fw.next 12','execute if score #phase fw.phase matches 2 run scoreboard players set #next fw.next 8','execute if score #phase fw.phase matches 3 run scoreboard players set #next fw.next 6',
 'data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}',
 'execute as @e[tag=fw.boss,limit=1] at @s facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes run tp @s ~ ~ ~ ~ ~',
 'execute if score #skill fw.skill matches 2 run '+call('skills/lock'),
 'execute if score #skill fw.skill matches 3 run '+call('bomb/mark'),
 'execute if score #skill fw.skill matches 6 at @e[tag=fw.boss,limit=1] positioned ~ ~2.5 ~ run '+call('skills/ring'),
 'execute if score #skill fw.skill matches 5 run '+message('외벽 사격! 네 벽에서 세 번 들어옵니다. 바뀌는 사선과 엄폐물을 확인하세요.'),
 'execute if score #skill fw.skill matches 6 run '+message('포위 화살! 0.6초 뒤 중심으로 모입니다. 원 밖이나 엄폐물로 이동하세요.'),
 'execute if score #phase fw.phase matches 3 if score #skill fw.skill matches 1..2 run '+call('bomb/mark'),
 'execute at @e[tag=fw.boss,limit=1] run playsound minecraft:entity.stray.ambient hostile @a[tag=fw.active] ~ ~ ~ 1 1.6',
 message('활을 들었다! 사격 방향 또는 발밑 폭격 표식을 확인하세요.')])
 fn('skills/lock',['kill @e[tag=fw.aim]','execute at @a[tag=fw.active,gamemode=!creative,sort=random,limit=1] run summon minecraft:marker ~ ~1 ~ {Tags:["fw.owned","fw.aim"]}'])
 fn('skills/casting',['scoreboard players remove #cast fw.cast 1',
 'execute if score #cast fw.cast matches 17.. at @e[tag=fw.boss,limit=1] run particle minecraft:snowflake ~ ~1.5 ~ .3 .3 .3 0 8 force @a[tag=fw.active]',
 'execute if score #skill fw.skill matches 1 if score #cast fw.cast matches 16 at @e[tag=fw.boss,limit=1] rotated as @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ run '+call('skills/fan'),
 *[f'execute if score #skill fw.skill matches 2 if score #cast fw.cast matches {t} at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @e[tag=fw.aim,limit=1] feet run '+call('arrows/normal') for t in (16,12,8)],
 'execute if score #skill fw.skill matches 4 if score #cast fw.cast matches 12 at @e[tag=fw.boss,limit=1] rotated as @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ run '+call('arrows/explosive'),
 'execute if score #skill fw.skill matches 5 if score #cast fw.cast matches 16 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ run '+call('walls/wave_one'),
 'execute if score #skill fw.skill matches 5 if score #cast fw.cast matches 8 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ run '+call('walls/wave_two'),
 'execute if score #skill fw.skill matches 6 if score #cast fw.cast matches 17.. at @e[tag=fw.ring] run particle minecraft:snowflake ~ ~ ~ .08 .08 .08 0 2 force @a[tag=fw.active]',
 'execute if score #skill fw.skill matches 6 if score #cast fw.cast matches 16 run '+call('skills/collapse'),
 'execute if score #cast fw.cast matches 0 run '+call('skills/recover')])
 fn('skills/fan',[f'execute rotated ~{angle} ~ run '+call('arrows/normal') for angle in (-22,-11,0,11,22)])
 fn('skills/radial',[call('walls/wave_one')])
 fn('skills/ring',['kill @e[tag=fw.ring]',*[f'execute rotated {i*15} 0 positioned ^ ^ ^10 run '+call('arrows/hover')+' with storage frost_warden:ctx' for i in range(24)]])
 # v19: teleport, dense patterns, physical stun arrows and fight-scoped binding.
 append(N,'fight/spawn',['scoreboard players set #blink fw.blink 100','scoreboard players set #enraged fw.tmp 0',call('teleport/setup')])
 fn('teleport/setup',[*[f'execute positioned ~{x} ~ ~{z} if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless block ~ ~-1 ~ #frost_warden:blast_pass run summon minecraft:marker ~ ~ ~ {{Tags:["fw.owned","fw.teleport_point"]}}' for x,z in [(-12,-10),(12,-10),(-12,6),(12,6),(0,-12),(-6,-5),(6,-5)] ]])
 fn('teleport/tick',['scoreboard players remove #blink fw.blink 1','execute if score #blink fw.blink matches ..0 if score #cast fw.cast matches 0 run '+call('teleport/blink')])
 fn('teleport/blink',['tag @e[tag=fw.teleport_point] remove fw.destination','execute at @e[tag=fw.boss,limit=1] as @e[tag=fw.teleport_point,distance=6..] at @s if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless block ~ ~-1 ~ #frost_warden:blast_pass unless entity @a[tag=fw.active,distance=..3] run tag @s add fw.destination',
 'execute if entity @e[tag=fw.destination] run '+call('teleport/move'),'scoreboard players set #blink fw.blink 100'])
 fn('teleport/move',['execute at @e[tag=fw.boss,limit=1] run particle minecraft:portal ~ ~1 ~ .4 .7 .4 .05 40 force @a[tag=fw.active]',
 'execute at @e[tag=fw.destination,sort=random,limit=1] run tp @e[tag=fw.boss,limit=1] ~ ~ ~',
 'execute as @e[tag=fw.boss,limit=1] at @s facing entity @a[tag=fw.active,sort=nearest,limit=1] eyes run tp @s ~ ~ ~ ~ ~',
 'execute at @e[tag=fw.boss,limit=1] run particle minecraft:snowflake ~ ~1 ~ .5 .7 .5 .03 35 force @a[tag=fw.active]',
 'execute at @e[tag=fw.boss,limit=1] run playsound minecraft:entity.enderman.teleport hostile @a[tag=fw.active] ~ ~ ~ .8 1.4','scoreboard players add #teleports fw.tmp 1'])
 append(N,'fight/tick',['execute as @a[tag=fw.bound,tag=!fw.active] run '+call('debuff/clear'),'execute as @a[tag=fw.stunned,tag=!fw.active] run '+call('debuff/clear')])
 append(N,'fight/alive',[call('teleport/tick'),
 'execute if score #time fw.time matches 1200.. if score #enraged fw.tmp matches 0 run '+call('debuff/enrage'),
 'execute as @a[tag=fw.active,tag=fw.stunned] run '+call('debuff/tick'),
 'execute as @a[tag=fw.active,tag=fw.bound,tag=!fw.stunned] run effect give @s minecraft:slowness infinite 1 true'])
 append(N,'tick',['execute if score #state fw.state matches 0 as @a[tag=fw.bound] run '+call('debuff/clear'),'execute if score #state fw.state matches 0 as @a[tag=fw.stunned] run '+call('debuff/clear')])
 fn('debuff/enrage',['scoreboard players set #enraged fw.tmp 1','execute as @a[tag=fw.active,gamemode=!creative] run '+call('debuff/bind'),message('영구 동결! 전투가 끝날 때까지 구속 II가 지속됩니다.')])
 fn('debuff/bind',['tag @s add fw.bound','execute unless entity @s[tag=fw.stunned] run effect give @s minecraft:slowness infinite 1 true'])
 fn('stun/hit',['advancement revoke @s only frost_warden:internal/stun','execute if score #state fw.state matches 1 if entity @s[tag=fw.active,gamemode=!creative] run '+call('stun/apply')])
 fn('stun/apply',['tag @s add fw.stunned','scoreboard players set @s fw.stun 40','effect give @s minecraft:slowness 2 6 true','effect give @s minecraft:blindness 2 0 true',
 'tellraw @s {text:"스턴 화살! 2초 동결 후 전투 종료까지 구속 II",color:"dark_aqua"}'])
 fn('debuff/tick',['scoreboard players remove @s fw.stun 1','execute if score @s fw.stun matches 1.. run effect give @s minecraft:slowness 2 6 true',
 'execute if score @s fw.stun matches ..0 run '+call('stun/end')])
 fn('stun/end',['tag @s remove fw.stunned','effect clear @s minecraft:slowness','effect clear @s minecraft:blindness',call('debuff/bind')])
 fn('debuff/clear',['effect clear @s minecraft:slowness','execute if entity @s[tag=fw.stunned] run effect clear @s minecraft:blindness','tag @s remove fw.bound','tag @s remove fw.stunned','scoreboard players set @s fw.stun 0'])
 append(N,'cleanup',['execute as @a[tag=fw.bound] run '+call('debuff/clear'),'execute as @a[tag=fw.stunned] run '+call('debuff/clear')])
 append(N,'skills/begin',['execute if score #skill fw.skill matches 7 run '+message('동결 사격! 청록색 화살에 맞으면 움직일 수 없습니다. 엄폐하세요.')])
 append(N,'skills/casting',[*[f'execute if score #skill fw.skill matches 7 if score #cast fw.cast matches {t} at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes run '+call('arrows/stun') for t in (16,10,4)],
 'execute if score #skill fw.skill matches 5 if score #cast fw.cast matches 4 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ run '+call('walls/wave_one')])
 fn('arrows/stun',[call('arrows/normal'),'execute as @e[tag=fw.arrow] if score @s fw.id = #serial fw.id run tag @s add fw.stun_arrow',
 'execute as @e[tag=fw.stun_arrow] if score @s fw.id = #serial fw.id run data merge entity @s {damage:5.0d}'])
 append(N,'arrows/tick',['execute if entity @s[tag=fw.stun_arrow] run particle minecraft:soul_fire_flame ~ ~ ~ .05 .05 .05 0 3 force @a[tag=fw.active]'])
 js(DP/f'data/{N}/advancement/internal/stun.json',{'criteria':{'event':{'trigger':'minecraft:entity_hurt_player','conditions':{'damage':{'taken':{'min':.001},'type':{'direct_entity':{'minecraft:nbt':'{Tags:["fw.stun_arrow"]}'}}}}}},'rewards':{'function':f'{N}:stun/hit'}})
 # Fixed arena-wall origins; move an emitter inward past solid grandstand sections.
 append(N,'fight/spawn',[call('walls/setup')])
 fn('walls/setup',['kill @e[tag=fw.wall_emitter]',*[f'execute positioned ~{x} ~1.25 ~{z} rotated {yaw} 0 run '+call('walls/find_'+parity) for parity,positions in [('one',range(-14,15,4)),('two',range(-12,13,4))] for q in positions for x,z,yaw in [(-16.25,q,-90),(16.25,q,90),(q,-16.25,0),(q,16.25,180)]]])
 for parity in ('one','two'):
  fn('walls/find_'+parity,['scoreboard players set #wall_steps fw.tmp 0',call('walls/seek_'+parity)])
  fn('walls/seek_'+parity,['execute if block ~ ~ ~ #frost_warden:blast_pass run return run '+call('walls/place_'+parity),
   'scoreboard players add #wall_steps fw.tmp 1','execute if score #wall_steps fw.tmp matches ..20 positioned ^ ^ ^.5 run '+call('walls/seek_'+parity)])
  fn('walls/place_'+parity,[f'summon minecraft:marker ~ ~ ~ {{Tags:["fw.owned","fw.wall_emitter","fw.wall_{parity}","fw.wall_new"]}}','tp @e[tag=fw.wall_new] ~ ~ ~ ~ ~','tag @e[tag=fw.wall_new] remove fw.wall_new'])
  fn('walls/wave_'+parity,['execute as @e[tag=fw.wall_'+parity+'] at @s rotated as @s run '+call('walls/fire')])
 fn('walls/fire',[call('arrows/normal'),'execute as @e[tag=fw.arrow] if score @s fw.id = #serial fw.id run tag @s add fw.wall_arrow',
 'particle minecraft:snowflake ~ ~ ~ .1 .15 .1 0 5 force @a[tag=fw.active]'])
 append(N,'skills/casting',['execute if score #skill fw.skill matches 5 if score #cast fw.cast matches 17.. at @e[tag=fw.wall_emitter] run particle minecraft:soul_fire_flame ~ ~ ~ .08 .15 .08 0 2 force @a[tag=fw.active]'])
 fn('arrows/hover',['$summon minecraft:arrow ~ ~ ~ {Tags:["fw.owned","fw.ring"],NoGravity:1b,Motion:[0d,0d,0d],Owner:$(owner),damage:0d,PierceLevel:1b,pickup:0b,item:{id:"minecraft:arrow",count:1}}'])
 fn('skills/collapse',['execute as @e[tag=fw.ring] at @s facing entity @e[tag=fw.boss,limit=1] eyes run '+call('arrows/normal'),'kill @e[tag=fw.ring]'])
 fn('skills/recover',['scoreboard players set #safe fw.safe 12','execute if score #skill fw.skill matches 3..4 run scoreboard players set #safe fw.safe 16','kill @e[tag=fw.aim]',
 'data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}',message('장전 중! 지금 반격하세요.')])
 # Re-enable native AI only when the explicit recovery window is over.
 append(N,'fight/alive',['execute if score #cast fw.cast matches 0 if score #safe fw.safe matches 0 run data merge entity @e[tag=fw.boss,limit=1] {NoAI:0b}'])
 fn('arrows/native',['$execute as @e[type=minecraft:arrow,tag=!fw.arrow,tag=!fw.ring,nbt={Owner:$(owner)}] at @s run function frost_warden:arrows/adopt'])
 fn('arrows/add_scan',['data modify storage frost_warden:add_ctx owner set from entity @s UUID',call('arrows/add_native')+' with storage frost_warden:add_ctx'])
 fn('arrows/add_native',['$execute as @e[type=minecraft:arrow,tag=!fw.arrow,tag=!fw.ring,nbt={Owner:$(owner)}] at @s run function frost_warden:arrows/add_adopt'])
 fn('arrows/add_adopt',[call('arrows/adopt'),'data merge entity @s {damage:1.8d,PierceLevel:0b}'])
 fn('arrows/adopt',['tag @s add fw.owned','tag @s add fw.arrow','scoreboard players set @s fw.age 160','data merge entity @s {pickup:0b,damage:2.6d,PierceLevel:1b,item:{id:"minecraft:tipped_arrow",count:1,components:{"minecraft:potion_contents":{custom_effects:[{id:"minecraft:slowness",duration:40,amplifier:0}]}}}}'])
 for kind,damage in [('normal',2.6),('explosive',.2)]:
  fn('arrows/'+kind,['scoreboard players set #explosive fw.tmp '+('1' if kind=='explosive' else '0'),
   'data modify storage frost_warden:shot damage set value '+str(damage),call('arrows/vector')])
 fn('arrows/vector',['kill @e[tag=fw.vector]','summon minecraft:marker ~ ~ ~ {Tags:["fw.vector"]}',
 *[f'execute store result score #{axis} fw.tmp run data get entity @e[tag=fw.vector,limit=1] Pos[{i}] 1000' for i,axis in enumerate('xyz')],
 'execute positioned ^ ^ ^1 run tp @e[tag=fw.vector,limit=1] ~ ~ ~',
 *[cmd for i,axis in enumerate('xyz') for cmd in [f'execute store result score #v{axis} fw.tmp run data get entity @e[tag=fw.vector,limit=1] Pos[{i}] 1000',f'scoreboard players operation #v{axis} fw.tmp -= #{axis} fw.tmp',f'execute store result storage frost_warden:shot v{axis} double 0.0026 run scoreboard players get #v{axis} fw.tmp']],
 'data modify storage frost_warden:shot owner set from storage frost_warden:ctx owner',call('arrows/summon')+' with storage frost_warden:shot',
 call('arrows/register'),'kill @e[tag=fw.vector]'])
 fn('arrows/summon',['$summon minecraft:arrow ~ ~ ~ {Tags:["fw.owned","fw.arrow","fw.new"],Motion:[$(vx),$(vy),$(vz)],Owner:$(owner),damage:$(damage),PierceLevel:1b,pickup:0b,item:{id:"minecraft:arrow",count:1}}'])
 fn('arrows/register',['scoreboard players add #serial fw.id 1','scoreboard players operation @e[tag=fw.new] fw.id = #serial fw.id','scoreboard players set @e[tag=fw.new] fw.age 160',
 'execute if score #explosive fw.tmp matches 1 run tag @e[tag=fw.new] add fw.explosive',
 'execute if score #explosive fw.tmp matches 1 at @e[tag=fw.new,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["fw.owned","fw.tracker","fw.newtrack"]}',
 'execute if score #explosive fw.tmp matches 1 run scoreboard players operation @e[tag=fw.newtrack] fw.id = #serial fw.id','scoreboard players set @e[tag=fw.newtrack] fw.age 160','tag @e[tag=fw.newtrack] remove fw.newtrack','tag @e[tag=fw.new] remove fw.new'])
 fn('arrows/tick',['scoreboard players remove @s fw.age 1','execute if entity @s[tag=fw.explosive] run particle minecraft:flame ~ ~ ~ .04 .04 .04 0 2 force @a[tag=fw.active]',
 'execute if entity @s[tag=fw.explosive,nbt={inGround:1b}] run '+call('arrows/impact'),
 'execute if entity @s[tag=!fw.explosive,nbt={inGround:1b}] run kill @s','execute if score @s fw.age matches ..0 run '+call('arrows/expire')])
 fn('arrows/expire',['scoreboard players operation #id fw.id = @s fw.id','execute as @e[tag=fw.tracker] if score @s fw.id = #id fw.id run kill @s','kill @s'])
 fn('arrows/impact',['scoreboard players operation #id fw.id = @s fw.id','execute as @e[tag=fw.tracker] if score @s fw.id = #id fw.id run kill @s',
 'execute rotated as @s positioned ^ ^ ^-.2 positioned ~ ~.2 ~ run '+call('explosion'),'kill @s'])
 fn('arrows/tracker',['scoreboard players remove @s fw.age 1','scoreboard players operation #id fw.id = @s fw.id','scoreboard players set #found fw.tmp 0',
 'execute as @e[tag=fw.arrow] if score @s fw.id = #id fw.id run scoreboard players set #found fw.tmp 1',
 'execute as @e[tag=fw.arrow] if score @s fw.id = #id fw.id at @s run '+call('arrows/sync'),
 'execute if score #found fw.tmp matches 0 if score @s fw.age matches 1.. run '+call('explosion'),
 'execute if score #found fw.tmp matches 0 run kill @s','execute if score @s fw.age matches ..0 run kill @s'])
 fn('arrows/sync',['execute as @e[tag=fw.tracker] if score @s fw.id = #id fw.id run tp @s ~ ~ ~'])
 fn('hit_explosive',['advancement revoke @s only frost_warden:internal/explosive','execute if score #state fw.state matches 1 if entity @s[tag=fw.active] at @s run '+call('hit_impact')])
 fn('hit_impact',['execute as @e[tag=fw.explosive,distance=..6,sort=nearest,limit=1] run '+call('arrows/expire'),'execute positioned ~ ~1 ~ run '+call('explosion')])
 fn('hit',['advancement revoke @s only frost_warden:internal/hit','scoreboard players add @s fw.hits 1','effect give @s minecraft:slowness 2 0 true'])
 fn('shield',['advancement revoke @s only frost_warden:internal/shield','scoreboard players add @s fw.shield 1'])
 for key,tag in [('explosive','fw.explosive'),('hit','fw.arrow'),('shield','fw.arrow')]:
  conditions={'damage':{'type':{'direct_entity':{'minecraft:nbt':'{Tags:["'+tag+'"]}'}}}}
  if key=='shield':conditions['damage']['blocked']=True
  if key=='hit':conditions['damage']['taken']={'min':.001}
  v={'criteria':{'event':{'trigger':'minecraft:entity_hurt_player','conditions':conditions}},'rewards':{'function':f'{N}:'+('hit_explosive' if key=='explosive' else key)}}
  if key=='shield':
   v['criteria']['blast']={'trigger':'minecraft:entity_hurt_player','conditions':{'damage':{'blocked':True,'type':{'source_entity':{'minecraft:nbt':'{Tags:["fw.boss"]}'}}}}}
   v['requirements']=[['event','blast']]
  js(DP/f'data/{N}/advancement/internal/{key}.json',v)
 fn('explosion',['scoreboard players add #blasts fw.tmp 1','particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 force @a[distance=..64]',
 'playsound minecraft:entity.generic.explode hostile @a[distance=..64] ~ ~ ~ 1.3 1.2',
 'execute as @a[tag=fw.active,distance=..3] run '+call('explosion/check')])
 fn('explosion/check',['kill @e[tag=fw.ray_target]','execute at @s run summon minecraft:marker ~ ~1 ~ {Tags:["fw.ray_target"]}',
 'scoreboard players set #ray fw.tmp 0','execute facing entity @e[tag=fw.ray_target,limit=1] feet run '+call('explosion/ray'),'kill @e[tag=fw.ray_target]'])
 fn('explosion/ray',['execute unless block ~ ~ ~ #frost_warden:blast_pass run return 0',
 'execute if entity @e[tag=fw.ray_target,distance=..0.25] run return run '+call('explosion/damage'),
 'scoreboard players add #ray fw.tmp 1','execute if score #ray fw.tmp matches ..24 positioned ^ ^ ^.2 run '+call('explosion/ray')])
 fn('explosion/damage',['execute store success score #hurt fw.tmp run damage @s 7 frost_warden:burst by @e[tag=fw.boss,limit=1]', 'execute if score #hurt fw.tmp matches 1 run scoreboard players add @s fw.hits 1'])
 fn('bomb/mark',['execute as @a[tag=fw.active,gamemode=!creative] at @s run summon minecraft:marker ~ ~ ~ {Tags:["fw.owned","fw.bomb_mark","fw.newmark"]}',
 'scoreboard players set @e[tag=fw.newmark] fw.age 32','tag @e[tag=fw.newmark] remove fw.newmark',message('머리 위 폭격! 표시된 위치에서 즉시 벗어나세요.')])
 fn('bomb/tick',['scoreboard players remove @s fw.age 1','execute if score @s fw.age matches 21.. run particle minecraft:flame ~ ~.15 ~ .7 0 .7 0 12 force @a[tag=fw.active]',
 'execute if score @s fw.age matches 21.. run particle minecraft:snowflake ~ ~.15 ~ 1 0 1 0 16 force @a[tag=fw.active]',
 *[f'execute if score @s fw.age matches {t} positioned ~ ~12 ~ run '+call('bomb/drop') for t in (20,15,10)],
 'execute if score @s fw.age matches ..0 run kill @s'])
 fn('bomb/drop',['data modify storage frost_warden:shot vx set value 0.0d','data modify storage frost_warden:shot vy set value -1.8d','data modify storage frost_warden:shot vz set value 0.0d',
 'data modify storage frost_warden:shot damage set value 0.2d','data modify storage frost_warden:shot owner set from storage frost_warden:ctx owner',
 'scoreboard players set #explosive fw.tmp 1',call('arrows/summon')+' with storage frost_warden:shot',call('arrows/register')])
 fn('victory',['execute as @a[tag=fw.active,gamemode=!creative] run '+call('reward'),message('서리의 파수꾼을 쓰러뜨렸습니다!'),call('abort')])
 fn('reward',['give @s minecraft:bow[minecraft:custom_name={text:"파수꾼의 서리 활",color:"aqua"},minecraft:enchantments={"minecraft:power":4,"minecraft:unbreaking":3}]',
 'give @s minecraft:emerald 12','give @s minecraft:arrow 32','advancement grant @s only frost_warden:victory',
 'execute if score #time fw.time matches ..3600 run advancement grant @s only frost_warden:speed',
 'execute if score @s fw.hits matches 0 run advancement grant @s only frost_warden:untouched',
 'execute if score @s fw.shield matches 0 run advancement grant @s only frost_warden:no_shield',
 'execute if score #adds fw.adds matches 0 run advancement grant @s only frost_warden:no_adds'])
 fn('abort',['scoreboard players set #state fw.state 0',call('cleanup')])
 fn('cleanup',['execute if data storage frost_warden:ctx owner run '+call('arrows/native')+' with storage frost_warden:ctx','execute as @e[tag=fw.add] run '+call('arrows/add_scan'),
 'kill @e[tag=fw.owned]','kill @e[tag=fw.vector]','kill @e[tag=fw.ray_target]','tag @a remove fw.member','tag @a remove fw.active','tag @e[tag=fw.current] remove fw.current',
 'bossbar set frost_warden:health visible false','scoreboard players set #cast fw.cast 0'])
 fn('add_kill',['advancement revoke @s only frost_warden:internal/add_kill','scoreboard players add #adds fw.adds 1'])
 js(DP/f'data/{N}/advancement/internal/add_kill.json',{'criteria':{'kill':{'trigger':'minecraft:player_killed_entity','conditions':{'entity':{'type':'minecraft:entity_properties','entity':'this','predicate':{'minecraft:nbt':'{Tags:["fw.add"]}'}}}}},'rewards':{'function':f'{N}:add_kill'}})
 for key,title,description in [('root','서리의 폐망루','봉인 표적을 맞히고 파수꾼에게 도전하세요.'),('victory','눈보라를 꿰뚫다','서리의 파수꾼을 처치하세요.'),('speed','눈보다 빠르게','3분 이내에 처치하세요.'),('untouched','흩날리는 사선','보스 화살과 폭발 피해 없이 승리하세요.'),('no_shield','발로 피한 폭격','방패 방어 없이 승리하세요.'),('no_adds','고독한 사냥','보조 스트레이를 직접 처치하지 않고 승리하세요.')]:
  display={'icon':{'id':'minecraft:bow'},'title':{'text':title},'description':{'text':description},'frame':'task' if key in ('root','victory') else 'challenge','show_toast':True,'announce_to_chat':True,'hidden':False}
  if key=='root':display['background']='minecraft:gui/advancements/backgrounds/adventure'
  v={'display':display,'criteria':{'done':{'trigger':'minecraft:impossible'}}}
  if key!='root':v['parent']=f'{N}:root'
  js(DP/f'data/{N}/advancement/{key}.json',v)
 js(OUT/'Frost-guide.json',{'namespace':N,'boss':'서리의 파수꾼','appearance':'Vanilla Stray; no custom resources','sun_protection':'Unbreakable iron helmets for boss and adds; no time or weather changes','health':[1200,1800,2400],'nox_health':[900,1350,1800],
 'natural_site':'/locate structure frost_warden:watchtower','manual_install':'/function frost_warden:admin/install','manual_start':'/function frost_warden:admin/summon','survival_start':'Shoot the central target block','abort':'/function frost_warden:abort',
 'bombardment':{'warning_ticks':12,'height':12,'arrows':3,'spacing_ticks':5,'radius':3,'explosion_damage':7,'terrain_damage':False},
 'recovery_ticks':[12,16],'late_cooldown_ticks':6,'shield_policy':'Boss arrows and custom burst bypass shields; blocks still stop arrows and blast; add arrows remain blockable','wall_volley':{'walls':4,'spacing_blocks':4,'waves':3,'arrows_per_wave':[32,28,32],'total_arrows':92,'wave_spacing_ticks':[8,4],'origin':'Fixed to arena; blocked stand sections advance to first open point'},'self_damage':'Helmet enchantment rejects damage whose source entity is fw.boss; player arrows still hurt','collapse':{'radius':10,'arrows':24,'hover_ticks':12},'teleport_interval_ticks':100,'stun':{'ticks':40,'arrow_damage_base':5,'after_stun':'Slowness II until fight ends'},'enrage_ticks':1200,'binding_cleanup':'Victory, abort, death, leaving or reconnect exclusion','limitations':['Difficulty relative to Nox is a tuning target; connected-client balance playtesting required.']})

