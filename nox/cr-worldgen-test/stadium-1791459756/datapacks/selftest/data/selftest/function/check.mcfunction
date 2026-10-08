execute store result storage selftest:worldgen seeds int 1 run execute if entity @e[tag=db.seed]
execute as @e[tag=db.seed,limit=1] store result storage selftest:worldgen floor_y int 1 run data get entity @s Pos[1]
execute at @e[tag=db.seed,limit=1] store result storage selftest:worldgen floor_block int 1 run execute if block ~ ~-1 ~ minecraft:white_concrete
execute at @e[tag=db.seed,limit=1] store result storage selftest:worldgen roof_block int 1 run execute if block ~ ~17 ~ minecraft:air
execute at @e[tag=db.seed,limit=1] store result storage selftest:worldgen inside_air int 1 run execute if block ~ ~5 ~ minecraft:air
execute as @e[tag=db.seed] at @s run function desert_ball:site/init
execute store result storage selftest:worldgen anchors int 1 run execute if entity @e[tag=db.anchor]
execute store result storage selftest:worldgen bells int 1 run execute if entity @e[tag=db.start,type=minecraft:interaction]
execute at @e[tag=db.anchor,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["test.origin"]}
execute at @e[tag=test.origin,limit=1] run place template desert_ball:bernabeu ~120 ~-2 ~-45
execute as @e[tag=db.seed] at @s run function desert_ball:site/init
execute store result storage selftest:worldgen multiple_sites int 1 run execute if entity @e[tag=db.anchor]
kill @e[tag=test.origin]
