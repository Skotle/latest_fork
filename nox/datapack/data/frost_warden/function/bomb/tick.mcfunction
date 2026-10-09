scoreboard players remove @s fw.age 1
execute if score @s fw.age matches 21.. run particle minecraft:flame ~ ~.15 ~ .7 0 .7 0 12 force @a[tag=fw.active]
execute if score @s fw.age matches 21.. run particle minecraft:snowflake ~ ~.15 ~ 1 0 1 0 16 force @a[tag=fw.active]
execute if score @s fw.age matches 20 positioned ~ ~12 ~ run function frost_warden:bomb/drop
execute if score @s fw.age matches 15 positioned ~ ~12 ~ run function frost_warden:bomb/drop
execute if score @s fw.age matches 10 positioned ~ ~12 ~ run function frost_warden:bomb/drop
execute if score @s fw.age matches ..0 run kill @s
