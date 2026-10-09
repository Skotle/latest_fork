execute store result storage selftest:results seen_1 int 1 run scoreboard players get #1 probe.seen
execute store result storage selftest:results seen_2 int 1 run scoreboard players get #2 probe.seen
execute store result storage selftest:results seen_3 int 1 run scoreboard players get #3 probe.seen
execute store result storage selftest:results seen_4 int 1 run scoreboard players get #4 probe.seen
execute store result storage selftest:results seen_5 int 1 run scoreboard players get #5 probe.seen
execute store result storage selftest:results seen_6 int 1 run scoreboard players get #6 probe.seen
execute store result score #fire fw.tmp run data get entity @e[tag=fw.boss,limit=1] Fire
execute store result storage selftest:results sun_boss int 1 run execute if score #fire fw.tmp matches ..0
execute store result storage selftest:results sun_head int 1 run execute if items entity @e[tag=fw.boss,limit=1] armor.head minecraft:iron_helmet[minecraft:unbreakable]
execute store result storage selftest:results sun_adds int 1 run execute if items entity @e[tag=fw.add] armor.head minecraft:iron_helmet[minecraft:unbreakable]
execute store result storage selftest:results phase int 1 run scoreboard players get #phase fw.phase
execute store result storage selftest:results adds int 1 run execute if entity @e[tag=fw.add]
function frost_warden:abort
execute store result storage selftest:results cleanup int 1 run execute unless entity @e[tag=fw.owned]
summon minecraft:arrow 128 82.5 5 {Tags:["probe.startarrow"],Motion:[0d,0d,-2d],pickup:0b,item:{id:"minecraft:arrow",count:1}}
