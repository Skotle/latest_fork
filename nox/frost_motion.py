"""v23: movement independent of attack cooldown; queued blink before next attack."""
import json
from build import DP, OUT, js
from frost import fn, call, append, N
from frost_ashe import edit

def generate():
 edit('load', lambda s: 'scoreboard objectives add fw.walk dummy\n'+s)
 append(N,'fight/spawn',['scoreboard players set #walk fw.walk 0','scoreboard players set #steps fw.walk 0','scoreboard players set #blink fw.blink 120'])
 def alive(s):
  lines=[l for l in s.splitlines() if 'teleport/tick' not in l and '{NoAI:0b}' not in l]
  index=next(i for i,l in enumerate(lines) if 'run scoreboard players remove #next' in l)
  lines[index:index]=[call('teleport/tick'),call('movement/tick')]
  return '\n'.join(lines)+'\n'
 edit('fight/alive',alive)
 edit('teleport/blink',lambda s:s.replace('scoreboard players set #blink fw.blink 200','execute if entity @e[tag=fw.destination] run scoreboard players set #blink fw.blink 120\nexecute unless entity @e[tag=fw.destination] run scoreboard players set #blink fw.blink 20'))
 fn('movement/tick',[
  'scoreboard players add #walk fw.walk 1',
  'execute if score #walk fw.walk matches 80.. run scoreboard players set #walk fw.walk 0',
  # R charge and its complete recovery stay planted, preserving the fixed telegraph.
  'execute if score #safe fw.safe matches 0..24 unless score #skill fw.skill matches 4 as @e[tag=fw.boss,limit=1] at @s if entity @a[tag=fw.active,gamemode=!creative] run '+call('movement/choose'),
  'execute if score #skill fw.skill matches 4 if score #cast fw.cast matches 0 if score #safe fw.safe matches 0 as @e[tag=fw.boss,limit=1] at @s if entity @a[tag=fw.active,gamemode=!creative] run '+call('movement/choose')])
 fn('movement/choose',[
  'execute facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 unless entity @a[tag=fw.active,gamemode=!creative,distance=..12] positioned ^ ^ ^.18 run '+call('movement/step'),
  'execute facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 if entity @a[tag=fw.active,gamemode=!creative,distance=..6] positioned ^ ^ ^-.18 run '+call('movement/step'),
  'execute facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 if entity @a[tag=fw.active,gamemode=!creative,distance=6..12] if score #walk fw.walk matches ..39 positioned ^.16 ^ ^ run '+call('movement/step'),
  'execute facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 if entity @a[tag=fw.active,gamemode=!creative,distance=6..12] if score #walk fw.walk matches 40.. positioned ^-.16 ^ ^ run '+call('movement/step')])
 # Check all four corners of the body's clearance and support. Never cross arena walls.
 checks=' '.join(f'if block ~{x} ~{y} ~{z} minecraft:air' for x in ('-.31','.31') for z in ('-.31','.31') for y in ('','.9','1.8'))
 floor=' '.join(f'unless block ~{x} ~-.1 ~{z} #frost_warden:blast_pass' for x in ('-.31','.31') for z in ('-.31','.31'))
 fn('movement/step',[f'execute if entity @e[tag=fw.anchor,distance=..19] {checks} {floor} run '+call('movement/apply')])
 fn('movement/apply',['tp @s ~ ~ ~','scoreboard players add #steps fw.walk 1'])
 guide=json.loads((OUT/'Frost-guide.json').read_text(encoding='utf-8'))
 guide.update(revision=23,teleport_interval_ticks=120,teleport_failed_retry_ticks=20)
 guide['movement']={'approach_over_blocks':12,'retreat_under_blocks':6,'strafe_between_blocks':[6,12],'speed_blocks_per_second':[3.2,3.6],'direction_switch_ticks':40,'independent_of_player_movement':True,'collision_and_floor_checks':True,'ultimate_charge_and_recovery_stationary':True,'implementation':'Small server position steps; connected-client animation requires visual playtesting.'}
 js(OUT/'Frost-guide.json',guide)
