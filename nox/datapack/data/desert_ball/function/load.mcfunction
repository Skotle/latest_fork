scoreboard objectives add db.state dummy
scoreboard objectives add db.time dummy
scoreboard objectives add db.cast dummy
scoreboard objectives add db.skill dummy
scoreboard objectives add db.safe dummy
scoreboard objectives add db.hp dummy
scoreboard objectives add db.max dummy
scoreboard objectives add db.next dummy
scoreboard objectives add db.tmp dummy
scoreboard objectives add db.owner dummy
scoreboard objectives add db.debt dummy
scoreboard objectives add db.motion dummy
scoreboard objectives add db.idle dummy
scoreboard objectives add db.olddeath dummy
scoreboard objectives add db.oldleave dummy
scoreboard objectives add db.cycle dummy
bossbar add desert_ball:health {text:"사막의 볼, 크리스티아누",color:"gold"}
bossbar set desert_ball:health color yellow
execute unless score #serial db.owner matches 0.. run scoreboard players set #serial db.owner 0
execute unless data storage desert_ball:vault accounts run data modify storage desert_ball:vault accounts set value {}
scoreboard players set #state db.state 0
function desert_ball:cleanup
tellraw @a[tag=db.member] {"text": "크리스티아누 추가 — /locate structure desert_ball:bernabeu", "color": "gold"}
