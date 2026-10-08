execute if score @s db.skill matches 1 as @a[tag=db.active,distance=..1.2,sort=nearest,limit=1] run function desert_ball:theft/attempt
damage @a[tag=db.active,distance=..1.2,sort=nearest,limit=1] 3 minecraft:magic by @e[tag=db.boss,limit=1]
scoreboard players set @s db.time 0
