"""Generate a native 26.3 encounter system on top of the converted IDA pack."""
import json,zipfile
from pathlib import Path

BASE=Path(__file__).resolve().parent
PACK=BASE/'pack'; DATA=PACK/'data/dungeons_arise'; OUTPUT=BASE/'output'

# id, name, entity, hp, melee damage, interval(seconds), primary, secondary,
# add type, relic item, relic name, enchantments
BOSSES=[
 ('abandoned_temple','잊힌 사원의 독니','cave_spider',180,5,7,'venom','fangs','cave_spider','iron_sword','독니의 의식검',{'dungeons_arise:ensnaring':2,'minecraft:smite':3}),
 ('aviary','철창 위의 폭풍날개','phantom',200,6,8,'gale','snipe','phantom','bow','폭풍날개의 장궁',{'minecraft:power':4,'minecraft:punch':2}),
 ('bandit_towers','붉은 절벽의 저격수','pillager',200,5,7,'snipe','reinforcements','pillager','crossbow','절벽 감시자의 쇠뇌',{'minecraft:quick_charge':2,'minecraft:piercing':3}),
 ('bandit_village','약탈왕 붉은송곳','vindicator',260,7,8,'cleave','reinforcements','vindicator','iron_axe','약탈왕의 도끼',{'minecraft:sharpness':4,'minecraft:unbreaking':3}),
 ('bathhouse','침수된 목욕장의 파수꾼','drowned',200,5,8,'tide','frost','drowned','trident','탕수의 삼지창',{'minecraft:impaling':3,'minecraft:loyalty':2}),
 ('ceryneian_hind','금빛 모래의 사냥꾼','husk',220,6,8,'sandstorm','charge','husk','diamond_boots','사막 순례자의 장화',{'minecraft:feather_falling':4,'minecraft:soul_speed':2}),
 ('desert_hall','태양왕 아케트','husk',360,8,9,'sunfire','sandstorm','husk','diamond_chestplate','태양왕의 흉갑',{'minecraft:fire_protection':4,'minecraft:unbreaking':3}),
 ('foundry','용광로의 검은 대장장이','wither_skeleton',340,8,8,'forge','reinforcements','wither_skeleton','netherite_sword','검은 용광로의 검',{'minecraft:fire_aspect':2,'minecraft:smite':4}),
 ('greenwood_pub','unused','zombie',1,1,1,'cleave','cleave','zombie','stick','unused',{}),
 ('heavenly_challenger','천공의 시험관','shulker',280,6,8,'gale','void','endermite','shield','천공 시험관의 방패',{'minecraft:unbreaking':3,'minecraft:mending':1}),
 ('heavenly_conqueror','공허의 정복자','wither_skeleton',440,9,8,'void','thunder','endermite','netherite_sword','공허 정복자의 검',{'dungeons_arise:discharge':3,'minecraft:sharpness':4}),
 ('heavenly_rider','별바람의 기수','phantom',300,7,7,'gale','starfall','phantom','diamond_boots','별바람의 장화',{'minecraft:feather_falling':4,'minecraft:depth_strider':3}),
 ('illager_campsite','야영지의 돌격대장','vindicator',160,5,9,'charge','reinforcements','pillager','crossbow','돌격대장의 쇠뇌',{'minecraft:multishot':1,'minecraft:quick_charge':2}),
 ('infested_temple','서리 역병의 사제','stray',320,7,8,'frost','plague','stray','diamond_chestplate','서리 사제의 흉갑',{'dungeons_arise:purification':2,'minecraft:protection':3}),
 ('keep_kayra','카이라의 늪지 기사','vindicator',400,9,9,'cleave','tide','drowned','netherite_axe','카이라 기사의 전투도끼',{'minecraft:sharpness':4,'minecraft:unbreaking':3}),
 ('kisegi_sanctuary','키세기의 비단 여왕','spider',360,7,8,'web','fangs','cave_spider','diamond_sword','비단 여왕의 송곳니',{'dungeons_arise:ensnaring':3,'dungeons_arise:lolths_curse':1,'minecraft:sharpness':3}),
 ('mechanical_nest','기계 둥지의 전류감독','pillager',340,7,7,'thunder','snipe','pillager','crossbow','전류감독의 전격 쇠뇌',{'dungeons_arise:voltaic_shot':1,'minecraft:piercing':3}),
 ('mining_complex','깊은 갱도의 발파감독','bogged',300,7,8,'blast','reinforcements','zombie','diamond_pickaxe','발파감독의 채굴곡괭이',{'minecraft:efficiency':4,'minecraft:fortune':3,'minecraft:unbreaking':3}),
 ('plague_asylum','역병 수용소의 원장','wither_skeleton',440,9,9,'plague','soul','wither_skeleton','netherite_helmet','역병 원장의 가면',{'dungeons_arise:purification':3,'minecraft:protection':4}),
 ('scorched_mines','그을린 갱도의 잿빛 추적자','wither_skeleton',280,7,8,'forge','charge','wither_skeleton','diamond_sword','잿빛 추적자의 검',{'minecraft:smite':4,'minecraft:looting':2}),
 ('small_blimp','비행선장 구름갈퀴','pillager',180,5,8,'snipe','gale','pillager','crossbow','구름갈퀴의 쇠뇌',{'minecraft:quick_charge':3,'minecraft:piercing':2}),
 ('thornborn_towers','가시탑의 썩은 군주','zombie',320,8,9,'roots','plague','zombie','diamond_axe','가시 군주의 도끼',{'dungeons_arise:ensnaring':3,'minecraft:sharpness':4}),
 ('typhon','심해의 폭풍왕 티폰','drowned',380,8,8,'tide','thunder','drowned','trident','티폰의 폭풍 삼지창',{'minecraft:impaling':5,'minecraft:loyalty':3,'minecraft:channeling':1}),
]
BOSSES=[dict(zip(['id','name','entity','hp','damage','period','primary','secondary','add','relic','relic_name','enchants'],row)) for row in BOSSES if row[0]!='greenwood_pub']
# Verified against the bundled Minecraft 26.3 registry and this pack's custom
# enchantment definitions. Only relic item components exceed these caps;
# enchanting tables, books and regular dungeon loot keep their original caps.
NORMAL_ENCHANT_CAPS={
 'dungeons_arise:discharge':3,'dungeons_arise:ensnaring':4,'dungeons_arise:lolths_curse':1,
 'dungeons_arise:purification':3,'dungeons_arise:voltaic_shot':1,
 'minecraft:channeling':1,'minecraft:depth_strider':3,'minecraft:efficiency':5,
 'minecraft:feather_falling':4,'minecraft:fire_aspect':2,'minecraft:fire_protection':4,
 'minecraft:fortune':3,'minecraft:impaling':5,'minecraft:looting':3,'minecraft:loyalty':3,
 'minecraft:mending':1,'minecraft:multishot':1,'minecraft:piercing':4,'minecraft:power':5,
 'minecraft:protection':4,'minecraft:punch':2,'minecraft:quick_charge':3,
 'minecraft:sharpness':5,'minecraft:smite':5,'minecraft:soul_speed':3,'minecraft:unbreaking':3}
OVER_CAP_RELIC_BOSSES={'kisegi_sanctuary','plague_asylum','heavenly_conqueror'}
for b in BOSSES:
 b['over_cap_reward']=b['id'] in OVER_CAP_RELIC_BOSSES
 if b['over_cap_reward']:
  b['enchants']={name:NORMAL_ENCHANT_CAPS[name]+1 for name in b['enchants']}
 b['period']+=3
 b['damage']=max(3,round(b['damage']*.75))
SPELLS={
 'venom':('독안개','spore_blossom_air',5,3,'magic',[('poison',4,0)]),
 'fangs':('비단 송곳니','soul',3,0,'magic',[]),
 'gale':('폭풍의 날개','cloud',5,3,'magic',[('levitation',1,0)]),
 'snipe':('조준 사격','crit',2,6,'arrow',[]),
 'reinforcements':('증원 호출','smoke',3,0,'magic',[]),
 'cleave':('분쇄 내려치기','crit',4,7,'mob_attack',[('weakness',3,0)]),
 'tide':('해일의 압력','bubble',5,5,'magic',[('slowness',3,1)]),
 'frost':('서리 감옥','snowflake',4,4,'freeze',[('slowness',3,2)]),
 'sandstorm':('눈먼 모래폭풍','poof',5,4,'magic',[('blindness',2,0)]),
 'charge':('돌격 충격파','cloud',3,6,'mob_attack',[('slowness',2,1)]),
 'sunfire':('태양의 낙인','flame',4,7,'on_fire',[]),
 'forge':('용광로 분출','flame',4,6,'on_fire',[('weakness',3,0)]),
 'void':('공허 붕괴','portal',4,6,'magic',[('darkness',3,0)]),
 'thunder':('낙뢰 표식','electric_spark',3,7,'lightning_bolt',[]),
 'starfall':('별빛 낙하','end_rod',3,6,'magic',[('slowness',2,0)]),
 'plague':('역병 확산','soul',5,4,'magic',[('poison',4,0),('weakness',4,0)]),
 'web':('비단 결박','white_ash',4,3,'magic',[('slowness',3,3)]),
 'blast':('발파 충격파','explosion',4,7,'explosion',[('slowness',2,0)]),
 'soul':('영혼의 추출','soul_fire_flame',4,6,'magic',[('wither',3,0)]),
 'roots':('가시 뿌리','happy_villager',4,5,'magic',[('slowness',3,2)]),
}
for name,(label,particle,radius,damage,kind,effects) in list(SPELLS.items()):
 SPELLS[name]=(label,particle,min(radius,3),max(1,round(damage*.65)) if damage else 0,kind,
  [(effect,min(seconds,2),min(amplifier,1)) for effect,seconds,amplifier in effects])
SPELLS['sunfire']=('태양의 낙인','flame',2.5,4,'on_fire',[])
ARENA_RADIUS=24
OBJECTIVES=['sid','hp','max','phase','cd','wind','skill','stage','idle','cool','tmp','cfg','tick','age']
def js(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def fn(name,lines):
 p=DATA/'function/boss'/ (name+'.mcfunction');p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
def snbt(v):
 if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
 if isinstance(v,bool):return '1b' if v else '0b'
 if isinstance(v,dict):return '{'+','.join(json.dumps(k)+':'+snbt(x) for k,x in v.items())+'}'
 if isinstance(v,list):return '['+','.join(map(snbt,v))+']'
 return str(v)
def tag_function(tag,ident):
 p=PACK/f'data/minecraft/tags/function/{tag}.json';x=json.loads(p.read_text()) if p.exists() else {'values':[]}
 if ident not in x['values']:x['values'].append(ident)
 js(p,x)

def common():
 tag_function('load','dungeons_arise:boss/load');tag_function('tick','dungeons_arise:boss/tick')
 js(DATA/'predicate/boss/eligible.json',{'type':'minecraft:any_of','terms':[
  {'type':'minecraft:entity_properties','entity':'this','predicate':{'minecraft:type_specific/player':{'gamemode':[mode]}}} for mode in ['survival','adventure']]})
 js(DATA/'tags/block/boss_passable.json',{'values':['minecraft:air','minecraft:cave_air','minecraft:void_air','minecraft:water']})
 fn('install',[f'scoreboard objectives add ida.{n} dummy' for n in OBJECTIVES]+[
  'scoreboard players set #next ida.sid 0','scoreboard players set #enabled ida.cfg 1',
  'scoreboard players set #respawn ida.cfg 1800','scoreboard players set #abandon ida.cfg 60',
  'scoreboard players set #hundred ida.tmp 100','scoreboard players set #quarter ida.tmp 25',
  'scoreboard players set #two ida.tmp 2','data modify storage dungeons_arise:boss_system installed set value 1b'])
 fn('load',['execute unless data storage dungeons_arise:boss_system installed run function dungeons_arise:boss/install',
  'scoreboard players set #clock ida.tick 0','function dungeons_arise:boss/admin/apply_balance']+[
  f'execute in minecraft:{dim} as @e[type=minecraft:marker,tag=ida.site,scores={{ida.stage=1}}] at @s run function dungeons_arise:boss/site/restore with entity @s data' for dim in ['overworld','the_nether','the_end']])
 fn('tick',['scoreboard players add #clock ida.tick 1',
  'function dungeons_arise:boss/contain',
  'execute if score #clock ida.tick matches 5.. run function dungeons_arise:boss/fast',
  'execute if score #clock ida.tick matches 20.. run function dungeons_arise:boss/second',
  'execute if score #clock ida.tick matches 20.. run scoreboard players set #clock ida.tick 0'])
 fn('contain',[
  f'execute in minecraft:{dim} as @e[tag=ida.boss] at @s run function dungeons_arise:boss/core/leash with entity @s data' for dim in ['overworld','the_nether','the_end']]+[
  f'execute in minecraft:{dim} as @e[tag=ida.add] at @s run function dungeons_arise:boss/core/leash with entity @s data' for dim in ['overworld','the_nether','the_end']])
 fn('core/leash',[
  f'$execute at @e[type=minecraft:marker,tag=ida.site,scores={{ida.sid=$(id)}},limit=1] unless entity @s[distance=..{ARENA_RADIUS}] run function dungeons_arise:boss/core/return with entity @s data'])
 fn('core/return',[
  'tp @s ~ ~ ~','data modify entity @s Motion set value [0.0d,0.0d,0.0d]',
  'execute if entity @s[tag=ida.boss] run scoreboard players set @s ida.stage 0',
  'execute if entity @s[tag=ida.boss] run scoreboard players set @s ida.wind 0',
  'execute if entity @s[tag=ida.boss] run scoreboard players set @s ida.cd 0',
  '$execute if entity @s[tag=ida.boss] run kill @e[tag=ida.target,scores={ida.sid=$(id)}]'])
 # Fast is gated to four executions per second, not every tick after tick 5.
 fn('fast',['scoreboard players operation #mod ida.tmp = #clock ida.tick','scoreboard players set #five ida.tmp 5',
  'scoreboard players operation #mod ida.tmp %= #five ida.tmp']+[
  f'execute if score #mod ida.tmp matches 0 in minecraft:{dim} as @e[tag=ida.boss] at @s run function dungeons_arise:boss/core/fast with entity @s data' for dim in ['overworld','the_nether','the_end']])
 fn('second',['execute store result score #difficulty ida.tmp run difficulty',
  'execute if score #enabled ida.cfg matches 1 if score #difficulty ida.tmp matches 1.. as @a[predicate=dungeons_arise:boss/eligible] at @s run function dungeons_arise:boss/detect']+[
  f'execute in minecraft:{dim} run function dungeons_arise:boss/dimension' for dim in ['overworld','the_nether','the_end']])
 fn('dimension',[
  'execute as @e[type=minecraft:marker,tag=ida.site] at @s run function dungeons_arise:boss/site/second with entity @s data',
  'execute as @e[tag=ida.add] run scoreboard players add @s ida.age 1',
  'kill @e[tag=ida.add,scores={ida.age=90..}]'])
 fn('detect',[f'execute if predicate dungeons_arise:boss/in_{b["id"]} unless entity @e[type=minecraft:marker,tag=ida.site.{b["id"]},tag=!ida.manualsite,distance=..384] run function dungeons_arise:boss/{b["id"]}/site' for b in BOSSES])
 fn('site/second',[
  'execute if score #difficulty ida.tmp matches 0 if score @s ida.stage matches 1 run function dungeons_arise:boss/site/abort with entity @s data',
  '$execute unless entity @s[tag=ida.manualsite] if score #enabled ida.cfg matches 1 if score #difficulty ida.tmp matches 1.. if score @s ida.stage matches 0 if entity @a[predicate=dungeons_arise:boss/eligible,distance=..96] run function dungeons_arise:boss/$(kind)/start',
  'execute if score @s ida.stage matches 1 run function dungeons_arise:boss/site/active with entity @s data',
  'execute if score @s ida.stage matches 2 run scoreboard players add @s ida.cool 1',
  'execute if score @s ida.stage matches 2 if score @s ida.cool >= #respawn ida.cfg run scoreboard players set @s ida.stage 0'])
 fn('site/active',[
  'function dungeons_arise:boss/site/boundary',
  '$bossbar set dungeons_arise:encounter_$(id) players @a[predicate=dungeons_arise:boss/eligible,distance=..96]',
  '$execute as @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1] store result score @s ida.hp run data get entity @s Health 100',
  '$execute as @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1] store result bossbar dungeons_arise:encounter_$(id) value run data get entity @s Health 1',
  'execute unless entity @a[predicate=dungeons_arise:boss/eligible,distance=..128] run scoreboard players add @s ida.idle 1',
  'execute if entity @a[predicate=dungeons_arise:boss/eligible,distance=..128] run scoreboard players set @s ida.idle 0',
  '$execute unless entity @e[tag=ida.boss,scores={ida.sid=$(id),ida.hp=1..},limit=1] run function dungeons_arise:boss/site/victory with entity @s data',
  'execute if score @s ida.stage matches 1 if score @s ida.idle >= #abandon ida.cfg run function dungeons_arise:boss/site/abort with entity @s data'])
 import math
 fn('site/boundary',[
  f'particle minecraft:end_rod ~{math.cos(i*math.pi/8)*ARENA_RADIUS:.3f} ~0.3 ~{math.sin(i*math.pi/8)*ARENA_RADIUS:.3f} 0.08 0.15 0.08 0 2 force' for i in range(16)])
 fn('site/anchor',[
  '$tp @s @e[tag=ida.boss,scores={ida.sid=$(id)},limit=1]',
  'data modify entity @s data.anchored set value 1b'])
 fn('site/new',[
  'scoreboard players add #next ida.sid 1','scoreboard players operation @s ida.sid = #next ida.sid',
  'execute store result entity @s data.id int 1 run scoreboard players get @s ida.sid',
  'scoreboard players set @s ida.stage 0','scoreboard players set @s ida.cool 0','scoreboard players set @s ida.idle 0','tag @s remove ida.newsite'])
 fn('site/restore',[
  '$bossbar remove dungeons_arise:encounter_$(id)',
  '$bossbar add dungeons_arise:encounter_$(id) {"text":"$(name)","color":"gold"}',
  '$bossbar set dungeons_arise:encounter_$(id) max $(hp)',
  '$bossbar set dungeons_arise:encounter_$(id) color $(color)',
  '$bossbar set dungeons_arise:encounter_$(id) style notched_10',
  '$bossbar set dungeons_arise:encounter_$(id) players @a[predicate=dungeons_arise:boss/eligible,distance=..96]'])
 fn('site/victory',[
  'scoreboard players set @s ida.stage 2','scoreboard players set @s ida.cool 0',
  '$advancement grant @a[predicate=dungeons_arise:boss/eligible,distance=..96] only dungeons_arise:boss/$(kind)',
  '$tellraw @a[distance=..96] {"text":"[IDA] $(name) 격파! 보스가 있던 위치에서 전용 보상을 회수하세요.","color":"gold"}',
  'playsound minecraft:ui.toast.challenge_complete master @a[distance=..96] ~ ~ ~ 0.6 1',
  'function dungeons_arise:boss/site/cleanup with entity @s data'])
 fn('site/cleanup',[
  '$bossbar remove dungeons_arise:encounter_$(id)',
  '$kill @e[tag=ida.add,scores={ida.sid=$(id)}]',
  '$kill @e[tag=ida.target,scores={ida.sid=$(id)}]',
  '$team remove ida$(id)'])
 fn('site/abort',[
  '$execute as @e[tag=ida.boss,scores={ida.sid=$(id)}] run data modify entity @s DeathLootTable set value "minecraft:empty"',
  '$kill @e[tag=ida.boss,scores={ida.sid=$(id)}]',
  'function dungeons_arise:boss/site/cleanup with entity @s data',
  'scoreboard players set @s ida.stage 0','scoreboard players set @s ida.idle 0'])
 fn('core/setup',[
  '$scoreboard players set @s ida.sid $(id)','$scoreboard players set @s ida.max $(hp)',
  'scoreboard players operation @s ida.max *= #hundred ida.tmp','scoreboard players set @s ida.stage 0',
  'scoreboard players set @s ida.phase 1','scoreboard players set @s ida.cd 0','scoreboard players set @s ida.wind 0','scoreboard players set @s ida.skill 0',
  'scoreboard players set @s ida.age 0',
  '$team add ida$(id)','$team modify ida$(id) friendlyFire false','$team modify ida$(id) collisionRule pushOtherTeams','$team join ida$(id) @s',
  'effect give @s minecraft:fire_resistance infinite 0 true','tag @s remove ida.newboss'])
 fn('core/fast',[
  '$execute unless data entity @s data{balance_version:2} run function dungeons_arise:boss/$(kind)/refresh',
  'execute store result score @s ida.hp run data get entity @s Health 100',
  'execute if score @s ida.hp matches 1.. run function dungeons_arise:boss/core/alive with entity @s data'])
 fn('core/alive',[
  'scoreboard players operation #half ida.tmp = @s ida.max','scoreboard players operation #half ida.tmp /= #two ida.tmp',
  'execute if score @s ida.phase matches 1 if score @s ida.hp <= #half ida.tmp run function dungeons_arise:boss/core/enrage with entity @s data',
  'execute if score @s ida.wind matches 1.. run scoreboard players remove @s ida.wind 5',
  'execute if score @s ida.wind matches 1.. run function dungeons_arise:boss/core/telegraph with entity @s data',
  'execute if score @s ida.wind matches ..0 if score @s ida.stage matches 1 run function dungeons_arise:boss/core/resolve with entity @s data',
  'execute if score #clock ida.tick matches 20 run function dungeons_arise:boss/core/second with entity @s data'])
 fn('core/enrage',[
  'scoreboard players set @s ida.phase 2',
  '$bossbar set dungeons_arise:encounter_$(id) color red',
  '$tellraw @a[distance=..64] {"text":"[IDA] $(name)이(가) 격노했습니다! 공격 주기가 빨라집니다.","color":"red"}',
  'playsound minecraft:entity.ravager.roar hostile @a[distance=..64] ~ ~ ~ 0.7 0.8','particle minecraft:angry_villager ~ ~2 ~ 0.5 0.5 0.5 0 25 force'])
 fn('core/second',[
  '$execute at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] unless entity @a[predicate=dungeons_arise:boss/eligible,distance=..24] run return 0',
  'execute if score @s ida.stage matches 1 run return 0',
  'scoreboard players add @s ida.cd 1',
  '$scoreboard players set #period ida.tmp $(period)',
  'execute if score @s ida.phase matches 2 run scoreboard players remove #period ida.tmp 1',
  'execute if score @s ida.cd >= #period ida.tmp run function dungeons_arise:boss/core/begin with entity @s data'])
 fn('core/begin',[
  'scoreboard players set @s ida.stage 1','scoreboard players set @s ida.wind 40','scoreboard players set @s ida.cd 0',
  'execute if data entity @s data{primary:"sunfire"} if score @s ida.skill matches 0 run scoreboard players set @s ida.wind 60',
  '$execute if score @s ida.skill matches 0 run function dungeons_arise:boss/spell/$(primary)/warn with entity @s data',
  '$execute if score @s ida.skill matches 1 run function dungeons_arise:boss/spell/$(secondary)/warn with entity @s data'])
 fn('core/telegraph',[
  '$execute if score @s ida.skill matches 0 run function dungeons_arise:boss/spell/$(primary)/telegraph with entity @s data',
  '$execute if score @s ida.skill matches 1 run function dungeons_arise:boss/spell/$(secondary)/telegraph with entity @s data'])
 fn('core/resolve',[
  '$execute if score @s ida.skill matches 0 run function dungeons_arise:boss/spell/$(primary)/hit with entity @s data',
  '$execute if score @s ida.skill matches 1 run function dungeons_arise:boss/spell/$(secondary)/hit with entity @s data',
  '$kill @e[tag=ida.target,scores={ida.sid=$(id)}]',
  'scoreboard players set @s ida.stage 0','scoreboard players add @s ida.skill 1',
  'execute if score @s ida.skill matches 2.. run scoreboard players set @s ida.skill 0'])
 fn('core/target',[
  '$kill @e[tag=ida.target,scores={ida.sid=$(id)}]',
  '$execute at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] at @a[predicate=dungeons_arise:boss/eligible,distance=..24,sort=nearest,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["ida.target","ida.newtarget"],data:{id:$(id)}}',
  'execute as @e[tag=ida.newtarget] store result score @s ida.sid run data get entity @s data.id 1',
  'tag @e[tag=ida.newtarget] remove ida.newtarget'])
 fn('core/adds',[
  'scoreboard players set #adds ida.tmp 0',
  '$execute as @e[tag=ida.add,scores={ida.sid=$(id)}] run scoreboard players add #adds ida.tmp 1',
  '$execute if score #adds ida.tmp matches ..2 positioned ~2 ~ ~ run function dungeons_arise:boss/$(kind)/add with entity @s data',
  '$execute if score #adds ida.tmp matches ..2 positioned ~-2 ~ ~ run function dungeons_arise:boss/$(kind)/add with entity @s data'])
 fn('core/add_setup',[
  '$scoreboard players set @s ida.sid $(id)','scoreboard players set @s ida.age 0',
  '$team join ida$(id) @s','effect give @s minecraft:fire_resistance infinite 0 true','tag @s remove ida.newadd'])

def spells():
 for ident,(name,particle,radius,damage,damage_type,effects) in SPELLS.items():
  warn=['function dungeons_arise:boss/core/target with entity @s data',
   f'tellraw @a[predicate=dungeons_arise:boss/eligible,distance=..32] {{"text":"⚠ {name} — 표식에서 벗어나세요!","color":"yellow"}}',
   'playsound minecraft:block.note_block.bell hostile @a[distance=..32] ~ ~ ~ 0.6 0.8']
  telegraph=[]
  for dx,dz in [(radius,0),(-radius,0),(0,radius),(0,-radius),(radius*.7,radius*.7),(-radius*.7,radius*.7),(radius*.7,-radius*.7),(-radius*.7,-radius*.7)]:
   telegraph.append(f'$execute at @e[tag=ida.target,scores={{ida.sid=$(id)}},limit=1] run particle minecraft:{particle} ~{dx:g} ~0.2 ~{dz:g} 0.1 0.1 0.1 0.01 4 force')
  fn('spell/'+ident+'/telegraph',telegraph)
  warn.append('function dungeons_arise:boss/spell/'+ident+'/telegraph with entity @s data')
  fn('spell/'+ident+'/warn',warn)
  hit=[f'$execute at @e[tag=ida.target,scores={{ida.sid=$(id)}},limit=1] run particle minecraft:{particle} ~ ~0.5 ~ {radius/2:g} 0.8 {radius/2:g} 0.05 55 force']
  if damage:hit.append(f'$execute at @e[tag=ida.target,scores={{ida.sid=$(id)}},limit=1] as @a[predicate=dungeons_arise:boss/eligible,distance=..{radius}] at @e[type=minecraft:marker,tag=ida.site,scores={{ida.sid=$(id)}},limit=1] if entity @s[distance=..24] run damage @s {damage} minecraft:{damage_type} by @e[tag=ida.boss,scores={{ida.sid=$(id)}},limit=1]')
  for effect,seconds,amplifier in effects:hit.append(f'$execute at @e[tag=ida.target,scores={{ida.sid=$(id)}},limit=1] as @a[predicate=dungeons_arise:boss/eligible,distance=..{radius}] at @e[type=minecraft:marker,tag=ida.site,scores={{ida.sid=$(id)}},limit=1] if entity @s[distance=..24] run effect give @s minecraft:{effect} {seconds} {amplifier} true')
  if ident=='fangs':
   for dx,dz in [(0,0),(2,0),(-2,0),(0,2),(0,-2)]:
    hit += [f'$execute at @e[tag=ida.target,scores={{ida.sid=$(id)}},limit=1] run summon minecraft:evoker_fangs ~{dx} ~ ~{dz} {{Tags:["ida.newfang"]}}',
     'data modify entity @e[tag=ida.newfang,limit=1] Owner set from entity @s UUID',
     'tag @e[tag=ida.newfang] remove ida.newfang']
  if ident=='reinforcements':hit+=['function dungeons_arise:boss/core/adds with entity @s data']
  # Other bosses call a bounded extra wave only in their second phase.
  elif ident in ['web','forge','plague','void']:hit+=['execute if score @s ida.phase matches 2 run function dungeons_arise:boss/core/adds with entity @s data']
  if ident in ['thunder','blast','sunfire','forge']:hit+=['playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..48] ~ ~ ~ 0.6 1']
  fn('spell/'+ident+'/hit',hit)

def boss(b):
 ident=b['id'];color='purple' if ident.startswith('heavenly') or ident=='plague_asylum' else 'blue' if ident in ['bathhouse','infested_temple','typhon'] else 'yellow' if ident in ['desert_hall','ceryneian_hind'] else 'red'
 meta={'kind':ident,'name':b['name'],'hp':b['hp'],'color':color,'period':b['period'],'primary':b['primary'],'secondary':b['secondary']}
 js(DATA/f'predicate/boss/in_{ident}.json',{'type':'minecraft:entity_properties','entity':'this','predicate':{'minecraft:location':{'structures':'dungeons_arise:'+ident}}})
 fn(ident+'/site',[
  f'summon minecraft:marker ~ ~ ~ {snbt({"Tags":["ida.site","ida.site."+ident,"ida.newsite"],"data":meta})}',
  'execute as @e[type=minecraft:marker,tag=ida.newsite,distance=..1,limit=1,sort=nearest] at @s run function dungeons_arise:boss/site/new'])
 fn(ident+'/start',[
  'scoreboard players set #players ida.tmp 0',
  'execute as @a[predicate=dungeons_arise:boss/eligible,distance=..96] run scoreboard players add #players ida.tmp 1',
  'execute if score #players ida.tmp matches ..0 run scoreboard players set #players ida.tmp 1',
  'execute if score #players ida.tmp matches 5.. run scoreboard players set #players ida.tmp 4',
  'scoreboard players remove #players ida.tmp 1','scoreboard players operation #players ida.tmp *= #quarter ida.tmp','scoreboard players add #players ida.tmp 100',
  f'scoreboard players set #hp ida.tmp {b["hp"]}',
  'scoreboard players operation #hp ida.tmp *= #players ida.tmp','scoreboard players operation #hp ida.tmp /= #hundred ida.tmp',
  'execute store result entity @s data.hp int 1 run scoreboard players get #hp ida.tmp',
  'scoreboard players set #spawned ida.tmp 0',
  f'execute unless data entity @s data.anchored at @a[predicate=dungeons_arise:boss/eligible,distance=..96,sort=nearest,limit=1] run function dungeons_arise:boss/{ident}/search',
  f'execute if data entity @s data.anchored if score #spawned ida.tmp matches 0 run function dungeons_arise:boss/{ident}/search',
  'execute if score #spawned ida.tmp matches 1 run function dungeons_arise:boss/site/restore with entity @s data'])
 offsets=[(6,0),(-6,0),(0,6),(0,-6),(4,4),(-4,4),(4,-4),(-4,-4),(2,0),(-2,0),(0,2),(0,-2),(0,0)]
 fn(ident+'/search',[
  f'execute if score #spawned ida.tmp matches 0 positioned ~{dx} ~ ~{dz} if block ~ ~ ~ #dungeons_arise:boss_passable if block ~ ~1 ~ #dungeons_arise:boss_passable if block ~ ~2 ~ #dungeons_arise:boss_passable unless block ~ ~-1 ~ #dungeons_arise:boss_passable unless block ~ ~-1 ~ minecraft:lava run function dungeons_arise:boss/{ident}/summon with entity @s data' for dx,dz in offsets])
 attrs=[{'id':'minecraft:max_health','base':'HP_TOKEN'},{'id':'minecraft:knockback_resistance','base':.65},{'id':'minecraft:follow_range','base':48},{'id':'minecraft:scale','base':1.15}]
 if b['entity'] not in ['shulker','phantom']:attrs.append({'id':'minecraft:movement_speed','base':.25 if b['entity'] in ['husk','zombie','drowned'] else .30})
 if b['entity'] in ['cave_spider','spider','husk','vindicator','wither_skeleton','zombie','drowned','phantom']:attrs.append({'id':'minecraft:attack_damage','base':b['damage']})
 weapon='crossbow' if b['entity']=='pillager' else 'bow' if b['entity'] in ['stray','bogged'] else 'trident' if b['entity']=='drowned' else 'iron_axe' if b['entity']=='vindicator' else 'iron_sword'
 equipment={'mainhand':{'id':'minecraft:'+weapon,'count':1},'head':{'id':'minecraft:iron_helmet','count':1,'components':{'minecraft:unbreakable':{}}}}
 if b['entity'] in ['spider','cave_spider','phantom','shulker']:equipment={}
 elif b['hp']>=300:equipment['chest']={'id':'minecraft:diamond_chestplate','count':1}
 payload={'Tags':['ida.boss','ida.boss.'+ident,'ida.newboss'],'CustomName':{'text':b['name'],'color':'dark_purple' if color=='purple' else color},'CustomNameVisible':True,'PersistenceRequired':True,'CanPickUpLoot':False,
  'Health':'HP_FLOAT','attributes':attrs,'equipment':equipment,'drop_chances':{k:0.0 for k in equipment},'DeathLootTable':'dungeons_arise:boss/'+ident,'data':{'id':'ID_TOKEN',**meta}}
 summon=snbt(payload).replace('"HP_TOKEN"','$(hp)').replace('"HP_FLOAT"','$(hp)f').replace('"ID_TOKEN"','$(id)')
 # hp in boss custom data must use the scaled value, too.
 summon=summon.replace('"hp":'+str(b['hp']),'"hp":$(hp)')
 fn(ident+'/summon',[
  '$summon minecraft:'+b['entity']+' ~ ~ ~ '+summon,
  'execute as @e[tag=ida.newboss,distance=..2,limit=1,sort=nearest] at @s run function dungeons_arise:boss/core/setup with entity @s data',
  'execute unless data entity @s data.anchored run function dungeons_arise:boss/site/anchor with entity @s data',
  'scoreboard players set @s ida.stage 1','scoreboard players set @s ida.idle 0',
  'scoreboard players set #spawned ida.tmp 1',
  f'tellraw @a[distance=..96] {{"text":"[IDA] {b["name"]} 출현! 노란 공격 표식을 피하세요.","color":"gold"}}',
  'playsound minecraft:entity.wither.spawn hostile @a[distance=..64] ~ ~ ~ 0.4 1.4'])
 add_equipment={'mainhand':{'id':'minecraft:crossbow' if b['add']=='pillager' else 'minecraft:bow' if b['add'] in ['stray','bogged'] else 'minecraft:iron_sword','count':1},'head':{'id':'minecraft:iron_helmet','count':1}}
 if b['add'] in ['spider','cave_spider','phantom','endermite']:add_equipment={}
 add_payload={'Tags':['ida.add','ida.newadd'],'PersistenceRequired':True,'DeathLootTable':'minecraft:empty','equipment':add_equipment,'drop_chances':{k:0.0 for k in add_equipment},'data':{'id':'ID_TOKEN'}}
 fn(ident+'/add',[
  '$execute if block ~ ~ ~ #dungeons_arise:boss_passable if block ~ ~1 ~ #dungeons_arise:boss_passable unless block ~ ~-1 ~ #dungeons_arise:boss_passable unless block ~ ~-1 ~ minecraft:lava run summon minecraft:'+b['add']+' ~ ~ ~ '+snbt(add_payload).replace('"ID_TOKEN"','$(id)'),
  'execute as @e[tag=ida.newadd] at @s run function dungeons_arise:boss/core/add_setup with entity @s data'])
 fn('admin/spawn/'+ident,[
  f'function dungeons_arise:boss/{ident}/site',
  f'execute as @e[type=minecraft:marker,tag=ida.site.{ident},distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/{ident}'])
 fn('admin/start/'+ident,[
  'tag @s add ida.manualsite',
  f'data modify entity @s data.hp set value {b["hp"]}',
  f'function dungeons_arise:boss/{ident}/summon with entity @s data',
  'function dungeons_arise:boss/site/restore with entity @s data'])
 refresh=[f'data modify entity @s data.period set value {b["period"]}','effect clear @s minecraft:speed',
  'data modify entity @s data.balance_version set value 2']
 if b['entity'] in ['cave_spider','spider','husk','vindicator','wither_skeleton','zombie','drowned','phantom']:
  refresh.append(f'attribute @s minecraft:attack_damage base set {b["damage"]}')
 fn(ident+'/refresh',refresh)
 # Every kill yields one named relic; equipment itself has zero drop chance.
 js(DATA/f'loot_table/boss/{ident}.json',{'type':'minecraft:entity','pools':[
  {'rolls':1,'entries':[{'type':'minecraft:item','name':'minecraft:'+b['relic'],'modifier':[
   {'type':'minecraft:set_name','name':{'text':b['relic_name'],'color':'gold','italic':False},'target':'item_name'},
   {'type':'minecraft:set_components','components':{'minecraft:custom_data':{'ida_relic':ident},'minecraft:lore':[{'text':b['name']+'의 전리품','color':'gray','italic':False}]}},
   {'type':'minecraft:set_components','components':{'minecraft:enchantments':b['enchants']}}]}]},
  {'rolls':1,'entries':[{'type':'minecraft:item','name':'minecraft:emerald','modifier':{'type':'minecraft:set_count','count':{'type':'minecraft:uniform','min':6,'max':12 if b['hp']<300 else 18}}}]},
  {'rolls':1,'entries':[{'type':'minecraft:item','name':'minecraft:experience_bottle','modifier':{'type':'minecraft:set_count','count':{'type':'minecraft:uniform','min':3,'max':8}}}]}]})
 js(DATA/f'advancement/boss/{ident}.json',{'parent':'dungeons_arise:boss/root','display':{
  'icon':{'id':'minecraft:'+b['relic']},'title':{'text':b['name']},'description':{'text':b['name']+' 격파'},'frame':'challenge','show_toast':True,'announce_to_chat':False,'hidden':False},
  'criteria':{'clear':{'trigger':'minecraft:impossible'}},'rewards':{'experience':150 if b['hp']<300 else 250}})

def build():
 common();spells()
 js(DATA/'advancement/boss/root.json',{'parent':'dungeons_arise:wda_root','display':{'icon':{'id':'minecraft:netherite_sword'},'title':{'text':'던전의 지배자들'},'description':{'text':'구조물 보스를 찾아 도전하세요.'},'show_toast':False,'announce_to_chat':False},'criteria':{'first':{'trigger':'minecraft:tick'}}})
 for b in BOSSES:boss(b)
 fn('admin/apply_balance',[
  f'execute in minecraft:{dim} as @e[tag=ida.boss.{b["id"]}] run function dungeons_arise:boss/{b["id"]}/refresh' for dim in ['overworld','the_nether','the_end'] for b in BOSSES]+[
  f'execute in minecraft:{dim} as @e[type=minecraft:marker,tag=ida.site,scores={{ida.stage=1}}] run data modify entity @s data.anchored set value 1b' for dim in ['overworld','the_nether','the_end']])
 fn('admin/abort_nearby',[
  'execute as @e[type=minecraft:marker,tag=ida.site,distance=..128,scores={ida.stage=1}] at @s run function dungeons_arise:boss/site/abort with entity @s data'])
 fn('admin/reset_nearby',[
  'function dungeons_arise:boss/admin/abort_nearby','scoreboard players set @e[type=minecraft:marker,tag=ida.site,distance=..128] ida.stage 0','scoreboard players set @e[type=minecraft:marker,tag=ida.site,distance=..128] ida.cool 0'])
 fn('admin/remove_nearby',[
  'function dungeons_arise:boss/admin/abort_nearby',
  'kill @e[type=minecraft:marker,tag=ida.site,distance=..128]'])
 js(OUTPUT/'boss-roster.json',{'bosses':BOSSES,'respawn_loaded_seconds':1800,'abandon_seconds':60,'health_scaling':'+25% per extra player, maximum 4 players','excluded':['greenwood_pub','merchant_campsite','lighthouse','wishing_well']})
 with zipfile.ZipFile(OUTPUT/'IDA-Vanilla-26.3-Bosses.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in sorted(PACK.rglob('*')):
   if f.is_file():z.write(f,f.relative_to(PACK).as_posix())
 print('Bosses',len(BOSSES),'functions',len(list((DATA/'function/boss').rglob('*.mcfunction'))),'ZIP',OUTPUT/'IDA-Vanilla-26.3-Bosses.zip')

if __name__=='__main__':build()


