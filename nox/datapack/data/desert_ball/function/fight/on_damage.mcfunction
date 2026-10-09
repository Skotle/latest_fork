execute as @a[scores={db.debt=1}] at @s run function desert_ball:theft/return
execute if score #skill db.skill matches 3 run kill @e[tag=db.decoy]
