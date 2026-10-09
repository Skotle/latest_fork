"""v21: Ashe-inspired, readable frost archer; overrides the former hardmode."""
import json
from build import DP,OUT,js
from frost import fn,call,append,message,N

def edit(name,transform):
 p=DP/f'data/{N}/function/{name}.mcfunction'
 p.write_text(transform(p.read_text(encoding='utf-8')),encoding='utf-8')

def generate():
 # Reduce health and native pressure, retaining the tested physical boss and self-hit guard.
 edit('fight/spawn',lambda s:s.replace('#max fw.max 600','#max fw.max 450').replace('#max fw.max 2400','#max fw.max 1800').replace('matches 2401..','matches 1801..').replace('#blink fw.blink 100','#blink fw.blink 200'))
 append(N,'fight/spawn',['scoreboard players set #focus fw.tmp 0','scoreboard players set #wall_side fw.tmp 0','scoreboard players set @a[tag=fw.member] fw.guard 0'])
 edit('load',lambda s:'scoreboard objectives add fw.guard dummy\n'+s)
 edit('fight/carrier',lambda s:s.replace('"minecraft:enchantments":{"minecraft:piercing":1}','"minecraft:enchantments":{}'))
 edit('fight/alive',lambda s:'\n'.join(l for l in s.splitlines() if 'debuff/enrage' not in l and 'slowness infinite' not in l)+'\n')
 append(N,'fight/alive',['execute as @a[tag=fw.active,scores={fw.guard=1..}] run scoreboard players remove @s fw.guard 1','execute as @e[tag=fw.hawk] at @s run '+call('ashe/hawk_tick')])
 edit('teleport/tick',lambda s:s.replace('if score #cast fw.cast matches 0 run','if score #cast fw.cast matches 0 if score #safe fw.safe matches 0 run'))
 edit('teleport/blink',lambda s:s.replace('#blink fw.blink 100','#blink fw.blink 200'))
 fn('phase/two',['scoreboard players set #phase fw.phase 2',call('adds/spawn'),message('서리 화살 강화! 짧은 둔화를 경계하고 기둥을 이용하세요.')])
 fn('phase/three',['scoreboard players set #phase fw.phase 3',message('최후의 집중! 패턴 간격이 조금 짧아집니다. 궁극기 후 반격하세요.')])
 edit('arrows/add_adopt',lambda s:s.replace('damage:1.8d','damage:1.0d'))
 fn('arrows/adopt',['tag @s add fw.owned','tag @s add fw.arrow','scoreboard players set @s fw.age 160','data merge entity @s {pickup:0b,damage:1.6d,PierceLevel:0b}'])
 # All ordinary attacks share the short Frost Shot slow; only R pierces shields.
 fn('arrows/normal',['scoreboard players set #explosive fw.tmp 0','data modify storage frost_warden:shot damage set value 1.6d',call('arrows/vector')])
 edit('arrows/vector',lambda s:s.replace('double 0.0026','double 0.0020'))
 edit('arrows/summon',lambda s:s.replace('PierceLevel:1b','PierceLevel:0b'))
 fn('hit',['advancement revoke @s only frost_warden:internal/hit','scoreboard players add @s fw.hits 1','effect give @s minecraft:slowness 1 0 true'])
 fn('skills/begin',['scoreboard players add #cycle fw.cycle 1','execute if score #cycle fw.cycle matches 10.. run scoreboard players set #cycle fw.cycle 1',
 *[f'execute if score #cycle fw.cycle matches {i} run scoreboard players set #skill fw.skill {v}' for i,v in enumerate([1,6,1,6,2,3,1,5,4],1)],
 'execute if score #skill fw.skill matches 2 unless score #focus fw.tmp matches 4.. run scoreboard players set #skill fw.skill 6',
 'scoreboard players set #cast fw.cast 36','execute if score #skill fw.skill matches 2 run scoreboard players set #cast fw.cast 48','execute if score #skill fw.skill matches 4 run scoreboard players set #cast fw.cast 48','execute if score #skill fw.skill matches 3 run scoreboard players set #cast fw.cast 28','execute if score #skill fw.skill matches 6 run scoreboard players set #cast fw.cast 28',
 'scoreboard players set #next fw.next 32','execute if score #phase fw.phase matches 2 run scoreboard players set #next fw.next 24','execute if score #phase fw.phase matches 3 run scoreboard players set #next fw.next 20',
 'data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}',
 'execute as @e[tag=fw.boss,limit=1] at @s facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes run tp @s ~ ~ ~ ~ ~',call('skills/lock'),
 'execute if score #skill fw.skill matches 2 run scoreboard players set #focus fw.tmp 0','execute if score #skill fw.skill matches 3 run '+call('ashe/hawk_begin'),
 'execute if score #skill fw.skill matches 5 run '+call('ashe/walls_select'),
 *[f'execute if score #skill fw.skill matches {i} run '+message(msg) for i,msg in [(1,'일제 사격! 활이 향하는 부채꼴 바깥이나 기둥 뒤로 이동하세요.'),(2,'궁사의 집중! 약한 화살 5발 연사 — 엄폐하세요.'),(3,'매 날리기! 정찰 중에는 피해 공격이 없습니다.'),(4,'마법의 수정화살! 푸른 사선을 보고 옆으로 피하세요. 발사 후 긴 반격 기회!'),(5,'외벽 사격! 표시된 두 벽에서 한 번만 발사합니다.')]],
 'execute at @e[tag=fw.boss,limit=1] run playsound minecraft:entity.stray.ambient hostile @a[tag=fw.active] ~ ~ ~ .7 1.5'])
 fn('skills/casting',['scoreboard players remove #cast fw.cast 1',
 'execute if score #cast fw.cast matches 17.. at @e[tag=fw.boss,limit=1] run particle minecraft:snowflake ~ ~1.5 ~ .2 .2 .2 0 4 force @a[tag=fw.active]',
 'execute if score #skill fw.skill matches 1 if score #cast fw.cast matches 16 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ rotated as @e[tag=fw.boss,limit=1] run '+call('skills/fan'),
 *[f'execute if score #skill fw.skill matches 2 if score #cast fw.cast matches {t} at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes run '+call('ashe/focus_shot') for t in [28,22,16,10,4]],
 'execute if score #skill fw.skill matches 4 if score #cast fw.cast matches 17.. at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @e[tag=fw.aim,limit=1] feet run '+call('ashe/ultimate_line'),
 'execute if score #skill fw.skill matches 4 if score #cast fw.cast matches 16 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @e[tag=fw.aim,limit=1] feet run '+call('arrows/stun'),
 'execute if score #skill fw.skill matches 5 if score #cast fw.cast matches 17.. at @e[tag=fw.wall_live] run particle minecraft:soul_fire_flame ~ ~ ~ .08 .15 .08 0 2 force @a[tag=fw.active]',
 'execute if score #skill fw.skill matches 5 if score #cast fw.cast matches 16 run '+call('walls/wave_one'),
 'execute if score #skill fw.skill matches 6 if score #cast fw.cast matches 16 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @e[tag=fw.aim,limit=1] feet run '+call('ashe/basic'),
 'execute if score #cast fw.cast matches 0 run '+call('skills/recover')])
 fn('skills/fan',[*[f'execute rotated ~{angle} ~ run '+call('arrows/normal') for angle in range(-36,37,9)],call('ashe/focus_gain')])
 fn('ashe/basic',[call('arrows/normal'),call('ashe/focus_gain')])
 fn('ashe/focus_gain',['scoreboard players add #focus fw.tmp 1','execute if score #focus fw.tmp matches 5.. run scoreboard players set #focus fw.tmp 4'])
 fn('ashe/focus_shot',['scoreboard players set #explosive fw.tmp 0','data modify storage frost_warden:shot damage set value .9d',call('arrows/vector')])
 fn('ashe/ultimate_line',[f'execute positioned ^ ^ ^{i} run particle minecraft:soul_fire_flame ~ ~ ~ .02 .02 .02 0 1 force @a[tag=fw.active]' for i in range(2,25,2)])
 fn('skills/recover',['scoreboard players set #safe fw.safe 30','execute if score #skill fw.skill matches 3 run scoreboard players set #safe fw.safe 20','execute if score #skill fw.skill matches 6 run scoreboard players set #safe fw.safe 20','execute if score #skill fw.skill matches 4 run scoreboard players set #safe fw.safe 50','kill @e[tag=fw.aim]','data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}',message('장전 중! 반격하세요.')])
 fn('ashe/hawk_begin',['kill @e[tag=fw.hawk]','execute at @e[tag=fw.boss,limit=1] run summon minecraft:marker ~ ~3 ~ {Tags:["fw.owned","fw.hawk"]}','scoreboard players set @e[tag=fw.hawk] fw.age 30'])
 fn('ashe/hawk_tick',['scoreboard players remove @s fw.age 1','execute facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes positioned ^ ^ ^.8 run tp @s ~ ~ ~','particle minecraft:end_rod ~ ~ ~ .1 .05 .1 0 3 force @a[tag=fw.active]','execute if entity @a[tag=fw.active,distance=..2] run '+call('ashe/hawk_finish'),'execute if score @s fw.age matches ..0 run '+call('ashe/hawk_finish')])
 fn('ashe/hawk_finish',['effect give @a[tag=fw.active,distance=..6] minecraft:glowing 3 0 true','tag @a[tag=fw.active,distance=..6] add fw.revealed','kill @s'])
 fn('ashe/walls_select',['tag @e[tag=fw.wall_emitter] remove fw.wall_live','scoreboard players add #wall_side fw.tmp 1','execute if score #wall_side fw.tmp matches 2.. run scoreboard players set #wall_side fw.tmp 0',
 'execute if score #wall_side fw.tmp matches 0 run tag @e[tag=fw.wall_one,y_rotation=0..0] add fw.wall_live','execute if score #wall_side fw.tmp matches 0 run tag @e[tag=fw.wall_one,y_rotation=180..180] add fw.wall_live',
 'execute if score #wall_side fw.tmp matches 1 run tag @e[tag=fw.wall_one,y_rotation=90..90] add fw.wall_live','execute if score #wall_side fw.tmp matches 1 run tag @e[tag=fw.wall_one,y_rotation=-90..-90] add fw.wall_live'])
 fn('walls/wave_one',['execute as @e[tag=fw.wall_live] at @s rotated as @s run '+call('walls/fire')])
 # Ultimate: one physical projectile, finite distance-based stun, then full mobility.
 fn('arrows/stun',[call('arrows/normal'),'execute as @e[tag=fw.arrow] if score @s fw.id = #serial fw.id run tag @s add fw.stun_arrow','execute as @e[tag=fw.stun_arrow] if score @s fw.id = #serial fw.id run data merge entity @s {damage:2.5d,PierceLevel:1b}'])
 fn('stun/hit',['advancement revoke @s only frost_warden:internal/stun','execute if score #state fw.state matches 1 if entity @s[tag=fw.active,gamemode=!creative] unless score @s fw.guard matches 1.. at @s run '+call('stun/apply'),'execute at @s as @e[tag=fw.stun_arrow,distance=..3,sort=nearest,limit=1] run '+call('arrows/expire')])
 fn('stun/apply',['tag @s add fw.stunned','scoreboard players set @s fw.stun 30','execute at @s if entity @e[tag=fw.boss,distance=..18] run scoreboard players set @s fw.stun 20','execute at @s if entity @e[tag=fw.boss,distance=..8] run scoreboard players set @s fw.stun 10','scoreboard players set @s fw.guard 80','effect give @s minecraft:slowness 1 6 true','effect give @a[tag=fw.active,distance=..2] minecraft:slowness 1 0 true','tellraw @s {text:"수정화살에 피격! 짧은 기절 후 이동이 회복됩니다.",color:"aqua"}'])
 fn('debuff/tick',['scoreboard players remove @s fw.stun 1','execute if score @s fw.stun matches 1.. run effect give @s minecraft:slowness 1 6 true','execute if score @s fw.stun matches ..0 run '+call('stun/end')])
 fn('stun/end',['tag @s remove fw.stunned','effect clear @s minecraft:slowness'])
 fn('debuff/enrage',['return 0'])
 fn('debuff/bind',['effect give @s minecraft:slowness 1 0 true'])
 append(N,'cleanup',['execute as @a[tag=fw.revealed] run effect clear @s minecraft:glowing','tag @a remove fw.revealed','scoreboard players set @a fw.guard 0'])
 append(N,'fight/tick',['execute as @a[tag=fw.revealed,tag=!fw.active] run effect clear @s minecraft:glowing','tag @a[tag=!fw.active] remove fw.revealed'])
 append(N,'tick',['execute if score #state fw.state matches 0 as @a[tag=fw.revealed] run effect clear @s minecraft:glowing','execute if score #state fw.state matches 0 run tag @a remove fw.revealed'])
 js(OUT/'Frost-guide.json',{'revision':21,'namespace':N,'boss':'서리의 파수꾼','health':[900,1350,1800],'appearance':'Vanilla Stray','manual_install':'/function frost_warden:admin/install','manual_start':'/function frost_warden:admin/summon','natural_site':'/locate structure frost_warden:watchtower','sources':['https://www.leagueoflegends.com/ko-kr/champions/ashe/','https://ddragon.leagueoflegends.com/cdn/16.20.1/data/ko_KR/champion/Ashe.json'],'requested_wiki_access':'Blocked; Riot official champion data used instead',
 'passive':{'slow_ticks':20,'amplifier':0,'ordinary_arrow_damage_base':1.6,'speed':2},'focus':{'required_stacks':4,'shots':5,'spacing_ticks':6,'damage_base':.9},'volley':{'arrows':9,'degrees':72,'warning_ticks':20},'hawk':{'damage':0,'reveal_ticks':60},'ultimate':{'shots':1,'warning_ticks':32,'damage_base':2.5,'stun_ticks_by_distance':[10,20,30],'ranges':[8,18],'recovery_ticks':50,'shield_piercing':True,'lock_on_after_release':False},'wall_volley':{'walls_at_once':2,'arrows':16,'waves':1,'warning_ticks':20,'spacing_blocks':4},'teleport_interval_ticks':200,'recovery_ticks':[20,30,50],'cooldown_ticks_by_phase':[32,24,20],'permanent_slowness':False,'blindness':False,'overlapping_patterns':False,'active_bombardment':False,'active_collapse_ring':False,'ordinary_arrows_blockable':True,'adds_max':1,'self_arrow_immunity':True,'limitations':['In-process server validation; connected-client balance and rendering still require playtesting.']})
