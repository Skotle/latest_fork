scoreboard players remove @s fw.age 1
scoreboard players operation #id fw.id = @s fw.id
scoreboard players set #found fw.tmp 0
execute as @e[tag=fw.arrow] if score @s fw.id = #id fw.id run scoreboard players set #found fw.tmp 1
execute as @e[tag=fw.arrow] if score @s fw.id = #id fw.id at @s run function frost_warden:arrows/sync
execute if score #found fw.tmp matches 0 if score @s fw.age matches 1.. run function frost_warden:explosion
execute if score #found fw.tmp matches 0 run kill @s
execute if score @s fw.age matches ..0 run kill @s
