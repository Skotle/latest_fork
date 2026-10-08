execute if dimension minecraft:overworld if score #state db.state matches 0 run place template desert_ball:bernabeu ~-32 ~-2 ~-45
execute as @e[tag=db.seed,distance=..3] at @s run function desert_ball:site/init
