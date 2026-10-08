execute in minecraft:overworld run function eclipse_nox:tick_overworld
execute in minecraft:overworld run function desert_ball:tick
execute as @a[scores={db.debt=1}] at @s if score #state db.state matches 0 run function desert_ball:theft/return
