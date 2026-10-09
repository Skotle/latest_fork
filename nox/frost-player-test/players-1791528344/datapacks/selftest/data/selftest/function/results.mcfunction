execute store result storage selftest:results seen_1 int 1 run scoreboard players get #1 probe.seen
execute store result storage selftest:results seen_2 int 1 run scoreboard players get #2 probe.seen
execute store result storage selftest:results seen_3 int 1 run scoreboard players get #3 probe.seen
execute store result storage selftest:results seen_4 int 1 run scoreboard players get #4 probe.seen
execute store result storage selftest:results phase int 1 run scoreboard players get #phase fw.phase
execute store result storage selftest:results adds int 1 run execute if entity @e[tag=fw.add]
function frost_warden:abort
execute store result storage selftest:results cleanup int 1 run execute unless entity @e[tag=fw.owned]
summon minecraft:arrow 128 82.5 5 {Tags:["probe.startarrow"],Motion:[0d,0d,-2d],pickup:0b,item:{id:"minecraft:arrow",count:1}}
