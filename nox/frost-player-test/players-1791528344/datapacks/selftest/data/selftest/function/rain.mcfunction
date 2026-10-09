execute store result storage selftest:results rain_blasts int 1 run scoreboard players get #blasts fw.tmp
execute store result storage selftest:results marks_expired int 1 run execute unless entity @e[tag=fw.bomb_mark]
scoreboard players set #blasts fw.tmp 0
fill 126 87 -14 130 87 -10 minecraft:stone_bricks
execute store result storage selftest:results roof_before int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
function frost_warden:bomb/mark
