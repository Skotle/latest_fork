scoreboard players remove @s db.time 1
execute if entity @s[tag=db.curve_left] run tp @s ~ ~ ~ ~-3 ~
execute if entity @s[tag=db.curve_right] run tp @s ~ ~ ~ ~3 ~
tp @s ^ ^ ^.85
execute at @s run function desert_ball:shot/after_move
