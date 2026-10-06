$execute unless data entity @s data{balance_version:2} run function dungeons_arise:boss/$(kind)/refresh
execute store result score @s ida.hp run data get entity @s Health 100
execute if score @s ida.hp matches 1.. run function dungeons_arise:boss/core/alive with entity @s data
