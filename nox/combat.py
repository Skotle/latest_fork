"""Responsive pacing, committed dash, two-strike combos and punish windows."""
import json, math
from build import DP, NS, fn, call, at, msg

def read(name):return (DP/f'data/{NS}/function/{name}.mcfunction').read_text(encoding='utf-8').splitlines()
def upgrade_combat():
    begin=read('fight/begin')
    begin=[l.replace('#max nx.max 400','#max nx.max 300').replace('#max nx.max matches 2001..','#max nx.max matches 1501..').replace('#max nx.max 2000','#max nx.max 1500') for l in begin]
    begin+=['scoreboard players set #dash nx.dash 0','scoreboard players set #expose nx.expose 0',
            'scoreboard players set #cycle nx.combo 0','scoreboard players set #chain nx.combo 0',
            'scoreboard players set #previous nx.anim -1','scoreboard players set #moving nx.move 0',
            'scoreboard players set #oldhp nx.hp -1','scoreboard players set #next nx.next 45']
    fn('fight/begin',begin)
    # Motion decisions and HP bonus precede phase gates; visuals follow the carrier.
    alive=read('fight/alive')
    alive=[l for l in alive if 'run tp @s ^ ^ ^.055' not in l and not l.startswith('execute if score #cast nx.cast matches 0 if score #puzzle nx.puzzle matches 0')]
    idx=next(i for i,l in enumerate(alive) if l.startswith('execute store result score #hp'))
    alive.insert(idx,call('fight/exposure'))
    idx=next(i for i,l in enumerate(alive) if 'tag=nox.bodypart' in l and 'run tp' in l)
    alive[idx:idx]=[call('fight/move'),
                   'execute if score #dash nx.dash matches 1.. run '+call('skills/dash/tick'),
                   'execute if score #cast nx.cast matches 0 if score #dash nx.dash matches 0 if score #puzzle nx.puzzle matches 0 if score #safe nx.safe matches 0 if entity @a[tag=nox.active] run scoreboard players remove #next nx.next 1',
                   'execute if score #cast nx.cast matches 0 if score #dash nx.dash matches 0 if score #puzzle nx.puzzle matches 0 if score #safe nx.safe matches 0 if score #next nx.next matches ..0 if entity @a[tag=nox.active] run '+call('skills/begin')]
    fn('fight/alive',alive)
    fn('fight/move',['scoreboard players set #moving nx.move 0',
                     'execute if score #cast nx.cast matches 0 if score #dash nx.dash matches 0 if score #safe nx.safe matches 0 if score #puzzle nx.puzzle matches 0 as @e[tag=nox.boss,limit=1] at @s facing entity @a[tag=nox.active,sort=nearest,limit=1] feet run '+call('fight/step')])
    fn('fight/step',['execute if entity @a[tag=nox.active,distance=4..,limit=1] positioned ^ ^ ^.12 if entity @e[tag=nox.anchor,tag=nox.current,distance=..21,limit=1] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~ ~ 0',
                     'execute if entity @a[tag=nox.active,distance=..3,limit=1] positioned ^.06 ^ ^-.03 if entity @e[tag=nox.anchor,tag=nox.current,distance=..21,limit=1] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~ ~ 0',
                     'execute if entity @a[tag=nox.active,limit=1] run scoreboard players set #moving nx.move 1'])
    # Store observed HP after the bonus. Next tick compares only new incoming damage.
    fn('fight/exposure',['execute store result score #seen nx.hp run data get entity @e[tag=nox.boss,limit=1] Health 100',
                         'execute if score #expose nx.expose matches 1 if score #safe nx.safe matches 1.. if score #oldhp nx.hp matches 1.. if score #seen nx.hp < #oldhp nx.hp run '+call('fight/bonus'),
                         'execute store result score #oldhp nx.hp run data get entity @e[tag=nox.boss,limit=1] Health 100',
                         'execute if score #safe nx.safe matches 0 run scoreboard players set #expose nx.expose 0'])
    fn('fight/bonus',['scoreboard players operation #lost nx.hp = #oldhp nx.hp','scoreboard players operation #lost nx.hp -= #seen nx.hp',
                     'scoreboard players set #two nx.tmp 2','scoreboard players operation #lost nx.hp /= #two nx.tmp',
                     'scoreboard players operation #seen nx.hp -= #lost nx.hp',
                     'execute if score #seen nx.hp matches 1.. store result storage eclipse_nox:damage health double .01 run scoreboard players get #seen nx.hp',
                     'execute if score #seen nx.hp matches 1.. run '+call('fight/set_health')+' with storage eclipse_nox:damage',
                     'execute if score #seen nx.hp matches ..0 run kill @e[tag=nox.boss]',
                     'execute at @e[tag=nox.boss,limit=1] run particle minecraft:crit ~ ~1.8 ~ .6 .5 .6 .1 12 force @a[tag=nox.member]'])
    fn('fight/set_health',['$data modify entity @e[tag=nox.boss,limit=1] Health set value $(health)f'])
    fn('skills/begin',['scoreboard players operation #previous_skill nx.skill = #skill nx.skill',
                       'scoreboard players add #cycle nx.combo 1','execute if score #cycle nx.combo matches 6.. run scoreboard players set #cycle nx.combo 1',
                       'scoreboard players operation #skill nx.skill = #cycle nx.combo',
                       'execute if score #cycle nx.combo matches 3 run scoreboard players set #skill nx.skill 5',
                       'execute if score #cycle nx.combo matches 4 run scoreboard players set #skill nx.skill 3',
                       'execute if score #cycle nx.combo matches 5 run scoreboard players set #skill nx.skill 1',
                       'execute if score #cycle nx.combo matches 5 if score #phase nx.phase matches 3 run scoreboard players set #skill nx.skill 4',
                       'execute at @e[tag=nox.boss,limit=1] unless entity @a[tag=nox.active,distance=..9] unless score #previous_skill nx.skill matches 5 run scoreboard players set #skill nx.skill 5',
                       'scoreboard players set #chain nx.combo 0','scoreboard players set #cast nx.cast 44','scoreboard players set #safe nx.safe 0','scoreboard players set #expose nx.expose 0',
                       'kill @e[tag=nox.target]',call('skills/aim'),
                       'execute if score #skill nx.skill matches 1 run '+msg('종 2연격 — 정면을 피해라. 두 번째 공격이 이어진다!'),
                       'execute if score #skill nx.skill matches 2 run scoreboard players set #cast nx.cast 54',
                       'execute if score #phase nx.phase matches 3 if score #skill nx.skill matches 2 run scoreboard players set #cast nx.cast 90',
                       'execute if score #skill nx.skill matches 2 run '+msg('확장 충격파 — 불꽃 고리의 안쪽으로 파고드세요!'),
                       'execute if score #skill nx.skill matches 3 run scoreboard players set #cast nx.cast 50',
                       'execute if score #skill nx.skill matches 3 run '+call('skills/echo'),
                       'execute if score #skill nx.skill matches 4 run '+call('skills/eclipse_begin'),
                       'execute if score #skill nx.skill matches 5 run scoreboard players set #cast nx.cast 32',
                       'execute if score #skill nx.skill matches 5 run '+msg('시계추 돌진 — 표시된 직선 옆으로 피하세요. 벽 충돌 시 심장이 노출됩니다!'),
                       'scoreboard players operation #total nx.total = #cast nx.cast',
                       'playsound eclipse_nox:warning master @a[tag=nox.member] ~ ~ ~ 1 1'])
    fn('skills/aim',['execute as @e[tag=nox.boss,limit=1] at @s facing entity @a[tag=nox.active,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                     'execute at @e[tag=nox.boss,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["nox.owned","nox.target"]}',
                     'execute as @e[tag=nox.target,limit=1] at @s rotated as @e[tag=nox.boss,limit=1] run tp @s ~ ~ ~ ~ 0'])
    fn('skills/echo',['execute as @a[tag=nox.active] at @s run summon minecraft:marker ~ ~ ~ {Tags:["nox.owned","nox.echo"]}',
                      'scoreboard players set @e[tag=nox.echo] nx.time 50',msg('잔향 — 지금 발자국이 2.5초 후 폭발한다. 이동!')])
    fn('skills/casting',['scoreboard players remove #cast nx.cast 1',
                         'execute if score #skill nx.skill matches 1 at @e[tag=nox.target,limit=1] run '+call('skills/cleave_warn'),
                         'execute if score #skill nx.skill matches 2 at @e[tag=nox.target,limit=1] run '+call('skills/ring_warn'),
                         'execute if score #skill nx.skill matches 5 at @e[tag=nox.target,limit=1] run '+call('skills/dash/warn'),
                         'execute if score #phase nx.phase matches 3 if score #skill nx.skill matches 2 if score #cast nx.cast matches 60 run '+call('skills/ring_wave'),
                         'execute if score #phase nx.phase matches 3 if score #skill nx.skill matches 2 if score #cast nx.cast matches 30 run '+call('skills/ring_wave'),
                         'execute if score #skill nx.skill matches 4 run '+call('skills/eclipse_tick'),
                         'execute if score #cast nx.cast matches 0 run '+call('skills/resolve')])
    fn('skills/ring_wave',['tag @a remove nox.hit','execute at @e[tag=nox.target,limit=1] run '+call('skills/ring_hit'),
                           'execute at @e[tag=nox.target,limit=1] run particle minecraft:explosion ~ ~.2 ~ 1 0 1 0 5 force @a[tag=nox.member]',
                           'playsound eclipse_nox:bell_low master @a[tag=nox.member] ~ ~ ~ .8 .8'])
    ringwarn=[]
    for i in range(40):
        a=i*math.tau/40
        for inner,outer,condition in [(3,6,'if score #phase nx.phase matches ..2'),(3,6,'if score #phase nx.phase matches 3 if score #cast nx.cast matches 60..'),(7,10,'if score #phase nx.phase matches 3 if score #cast nx.cast matches 30..59'),(11,14,'if score #phase nx.phase matches 3 if score #cast nx.cast matches ..29')]:
            for r in (inner,outer):ringwarn.append(f'execute {condition} run particle minecraft:soul_fire_flame ~{math.cos(a)*r:.3f} ~.1 ~{math.sin(a)*r:.3f} 0 0 0 0 1 force @a[tag=nox.member]')
    fn('skills/ring_warn',ringwarn)
    hit=[]
    for radius,condition in [('3..6','if score #phase nx.phase matches ..2'),('3..6','if score #phase nx.phase matches 3 if score #cast nx.cast matches 60..'),('7..10','if score #phase nx.phase matches 3 if score #cast nx.cast matches 30..59'),('11..14','if score #phase nx.phase matches 3 if score #cast nx.cast matches ..29')]:
        hit.append(f'execute {condition} as @a[tag=nox.active,tag=!nox.hit,distance={radius}] run '+call('damage/4'))
    fn('skills/ring_hit',hit)
    # First strike branches into a second committed swing; no recovery between swings.
    fn('skills/resolve',['scoreboard players operation #resolved nx.skill = #skill nx.skill',
                         'tag @a remove nox.hit','execute if score #skill nx.skill matches 1 at @e[tag=nox.target,limit=1] run '+call('skills/cleave_hit'),
                         'execute if score #skill nx.skill matches 2 at @e[tag=nox.target,limit=1] run '+call('skills/ring_hit'),
                         'execute if score #skill nx.skill matches 1 if score #chain nx.combo matches 0 run '+call('skills/combo'),
                         'execute if score #resolved nx.skill matches 1 if score #chain nx.combo matches 2 run '+call('skills/recover'),
                         'execute if score #resolved nx.skill matches 2..4 run '+call('skills/recover'),
                         'execute if score #resolved nx.skill matches 5 run '+call('skills/dash/begin'),
                         'execute if score #chain nx.combo matches 1 run scoreboard players set #chain nx.combo 2',
                         'playsound eclipse_nox:impact master @a[tag=nox.member] ~ ~ ~ .65 1'])
    fn('skills/combo',['scoreboard players set #chain nx.combo 1','scoreboard players set #cast nx.cast 28','scoreboard players set #total nx.total 28',
                       'execute as @e[tag=nox.target,limit=1] at @s run tp @s ~ ~ ~ ~70 0',
                       'execute as @e[tag=nox.boss,limit=1] at @s rotated as @e[tag=nox.target,limit=1] run tp @s ~ ~ ~ ~ 0',
                       msg('두 번째 타격 — 종이 옆으로 돌아간다! 새 불꽃 표식을 피하세요.')])
    fn('skills/recover',['kill @e[tag=nox.target]','scoreboard players set #safe nx.safe 30','scoreboard players set #next nx.next 22',
                         'execute if score #phase nx.phase matches 3 run scoreboard players set #next nx.next 14',
                         'execute if score #skill nx.skill matches 4 run scoreboard players set #safe nx.safe 90',
                         'execute if score #skill nx.skill matches 4 run scoreboard players set #expose nx.expose 1'])
    fn('skills/dash/warn',[f'execute rotated as @e[tag=nox.target,limit=1] positioned ^ ^.1 ^{r} run particle minecraft:electric_spark ~ ~ ~ .8 .04 .3 .01 4 force @a[tag=nox.member]' for r in range(2,19,2)])
    fn('skills/dash/begin',['scoreboard players set #dash nx.dash 18','scoreboard players set #safe nx.safe 0','tag @a remove nox.dashhit',
                           'execute at @e[tag=nox.boss,limit=1] run playsound eclipse_nox:impact master @a[tag=nox.member] ~ ~ ~ 1 .7'])
    fn('skills/dash/tick',['scoreboard players remove #dash nx.dash 1','scoreboard players set #moved nx.move 0',
                          'execute as @e[tag=nox.boss,limit=1] at @s rotated as @e[tag=nox.target,limit=1] positioned ^ ^ ^.8 if entity @e[tag=nox.anchor,tag=nox.current,distance=..21,limit=1] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air store success score #moved nx.move run tp @s ~ ~ ~ ~ 0',
                          'execute as @e[tag=nox.boss,limit=1] at @s run particle minecraft:cloud ~ ~.3 ~ .4 .2 .4 .02 10 force @a[tag=nox.member]',
                          'execute as @e[tag=nox.boss,limit=1] at @s as @a[tag=nox.active,tag=!nox.dashhit,distance=..2.7] run '+call('damage/dash'),
                          'execute if score #moved nx.move matches 0 run '+call('skills/dash/crash'),
                          'execute at @e[tag=nox.anchor,tag=nox.current,limit=1] as @e[tag=nox.boss,limit=1] unless entity @s[distance=..21] run '+call('skills/dash/crash'),
                          'execute if score #dash nx.dash matches 0 run '+call('skills/dash/end')])
    fn('skills/dash/crash',['scoreboard players set #dash nx.dash 0','scoreboard players set #crash nx.move 1',
                           'execute at @e[tag=nox.boss,limit=1] run particle minecraft:explosion ~ ~1 ~ .8 .4 .8 0 12 force @a[tag=nox.member]'])
    fn('skills/dash/end',['kill @e[tag=nox.target]','scoreboard players set #safe nx.safe 60','scoreboard players set #next nx.next 18','scoreboard players set #expose nx.expose 1',
                         'execute if score #crash nx.move matches 1 run scoreboard players set #safe nx.safe 90',
                         'scoreboard players set #crash nx.move 0',msg('균형 붕괴 — 녹스의 심장 노출! 지금 공격하면 피해가 1.5배.')])
    fn('damage/dash',['damage @s 7 minecraft:mob_attack by @e[tag=nox.boss,limit=1]','tag @s add nox.dashhit'])
    fn('damage/8',['damage @s 6 minecraft:mob_attack by @e[tag=nox.boss,limit=1]','tag @s add nox.hit'])
    # Puzzle break is now a real damage bonus, with the baseline captured immediately.
    success=read('puzzle/success')+['scoreboard players set #expose nx.expose 1',
                                 'execute store result score #oldhp nx.hp run data get entity @e[tag=nox.boss,limit=1] Health 100']
    fn('puzzle/success',success)
    for name in ['fight/phase2','fight/phase3']:
        lines=read(name);fn(name,['scoreboard players set #dash nx.dash 0','scoreboard players set #safe nx.safe 0','scoreboard players set #expose nx.expose 0']+lines)
    cleanup=read('fight/cleanup');fn('fight/cleanup',['scoreboard players set #dash nx.dash 0','scoreboard players set #expose nx.expose 0','tag @a remove nox.dashhit']+cleanup)
