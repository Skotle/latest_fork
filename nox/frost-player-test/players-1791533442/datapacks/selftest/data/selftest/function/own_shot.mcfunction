kill @e[tag=fw.arrow]
kill @e[tag=fw.tracker]
data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}
execute as @e[tag=fw.add] run data merge entity @s {NoAI:1b}
tp @e[tag=fw.boss,limit=1] 128 81 -2
scoreboard players operation #probe_pool fw.hp = #pool fw.hp
execute positioned 128 82 -8 rotated 0 0 run function frost_warden:arrows/normal
