execute store result storage selftest:worldgen seeds int 1 run execute if entity @e[tag=fw.site_seed]
execute as @e[tag=fw.site_seed,limit=1] store result storage selftest:worldgen floor_y int 1 run data get entity @s Pos[1]
execute at @e[tag=fw.site_seed,limit=1] store result storage selftest:worldgen floor_block int 1 run execute if block ~ ~-1 ~ minecraft:packed_ice
execute at @e[tag=fw.site_seed,limit=1] store result storage selftest:worldgen roof_block int 1 run execute if block ~ ~17 ~ minecraft:air
execute at @e[tag=fw.site_seed,limit=1] store result storage selftest:worldgen inside_air int 1 run execute if block ~ ~5 ~ minecraft:air
execute as @e[tag=fw.site_seed] at @s run function frost_warden:site/init
execute store result storage selftest:worldgen anchors int 1 run execute if entity @e[tag=fw.anchor]
execute at @e[tag=fw.anchor,limit=1] store result storage selftest:worldgen target_ready int 1 run execute if block ~ ~1 ~ minecraft:target[power=0]
execute at @e[tag=fw.anchor,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["test.origin"]}
execute at @e[tag=test.origin,limit=1] run place template frost_warden:watchtower ~120 ~-2 ~-45
execute as @e[tag=fw.site_seed] at @s run function frost_warden:site/init
execute store result storage selftest:worldgen multiple_sites int 1 run execute if entity @e[tag=fw.anchor]
kill @e[tag=test.origin]
