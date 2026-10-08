scoreboard players set #core db.tmp 0
execute store result score #core db.tmp run data get entity @e[tag=db.core,limit=1] Health 100
execute as @e[tag=db.core_visual] at @e[tag=db.core,limit=1] run tp @s ~ ~.25 ~
execute if score #core db.tmp matches ..799 run function desert_ball:skills/counter
