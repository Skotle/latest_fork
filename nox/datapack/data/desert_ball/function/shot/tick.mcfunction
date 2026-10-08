scoreboard players remove @s db.time 1
execute if entity @s[tag=db.curve_left] run tp @s ~ ~ ~ ~-3 ~
execute if entity @s[tag=db.curve_right] run tp @s ~ ~ ~ ~3 ~
tp @s ^ ^ ^.85
scoreboard players operation #ballid db.owner = @s db.owner
execute as @e[tag=db.shot_visual] if score @s db.owner = #ballid db.owner run tp @s ~ ~ ~
particle minecraft:crit ~ ~ ~ .1 .1 .1 0 2 force @a[tag=db.member]
execute if entity @a[tag=db.active,distance=..1.2] run function desert_ball:shot/hit
execute unless block ~ ~ ~ minecraft:air run scoreboard players set @s db.time 0
execute if score @s db.time matches ..0 run function desert_ball:shot/remove
