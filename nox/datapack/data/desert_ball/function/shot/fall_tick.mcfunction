scoreboard players remove @s db.time 1
particle minecraft:flame ~ ~.1 ~ 2 0 2 0 14 force @a[tag=db.member]
execute if score @s db.time matches ..0 as @a[tag=db.active,distance=..2.5] run damage @s 4 minecraft:magic by @e[tag=db.boss,limit=1]
execute if score @s db.time matches ..0 run kill @s
