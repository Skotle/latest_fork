scoreboard players remove @s fw.age 1
execute facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes positioned ^ ^ ^.8 run tp @s ~ ~ ~
particle minecraft:end_rod ~ ~ ~ .1 .05 .1 0 3 force @a[tag=fw.active]
execute if entity @a[tag=fw.active,distance=..2] run function frost_warden:ashe/hawk_finish
execute if score @s fw.age matches ..0 run function frost_warden:ashe/hawk_finish
