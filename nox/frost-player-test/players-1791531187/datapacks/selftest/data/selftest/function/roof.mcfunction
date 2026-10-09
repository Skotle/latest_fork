execute store result storage selftest:results roof_after int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
execute store result storage selftest:results roof_blasts int 1 run scoreboard players get #blasts fw.tmp
execute store result storage selftest:results roof_intact int 1 run execute if block 128 87 -12 minecraft:stone_bricks
fill 126 87 -14 130 87 -10 minecraft:air
fill 127 81 -7 129 85 -7 minecraft:air
scoreboard players set #safe fw.safe 0
scoreboard players set #next fw.next 0
data merge entity @e[tag=fw.boss,limit=1] {Health:1000f}
scoreboard players set #pool fw.hp 30000
scoreboard objectives add probe.seen dummy
scoreboard players set #1 probe.seen 0
scoreboard players set #2 probe.seen 0
scoreboard players set #3 probe.seen 0
scoreboard players set #4 probe.seen 0
scoreboard players set #5 probe.seen 0
scoreboard players set #6 probe.seen 0
