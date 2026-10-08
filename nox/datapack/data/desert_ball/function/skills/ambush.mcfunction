scoreboard players set #follow db.anim 12
execute as @e[tag=db.boss,limit=1] at @e[tag=db.ambush,limit=1] run tp @s ~ ~ ~
execute at @e[tag=db.boss,limit=1] as @a[tag=db.active,distance=..4] run damage @s 4 minecraft:mob_attack by @e[tag=db.boss,limit=1]
execute at @e[tag=db.boss,limit=1] as @a[tag=db.active,distance=..4,sort=nearest,limit=1] run function desert_ball:theft/attempt
execute at @e[tag=db.boss,limit=1] run function desert_ball:skills/core_spawn
execute as @e[tag=db.core,limit=1] at @e[tag=db.boss,limit=1] run tp @s ~ ~1.1 ~
