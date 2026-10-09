scoreboard objectives add probe.seen dummy
scoreboard players set #1 probe.seen 0
scoreboard players set #2 probe.seen 0
scoreboard players set #3 probe.seen 0
scoreboard players set #4 probe.seen 0
scoreboard players set #5 probe.seen 0
scoreboard players set #6 probe.seen 0
execute as @e[tag=db.anchor,limit=1] at @s run function desert_ball:begin
