execute store result score @s ida.hp run data get entity @s Health 100
execute if score @s ida.hp matches ..0 run function dungeons_arise:boss/visual/dead with entity @s data
execute if score @s ida.hp matches ..0 run return 0
$execute unless entity @e[type=minecraft:item_display,tag=ida.visual,scores={ida.sid=$(id)},limit=1] run function dungeons_arise:boss/visual/setup with entity @s data
$tp @e[type=minecraft:item_display,tag=ida.visual,scores={ida.sid=$(id)}] ~ ~ ~ ~180 0
execute if score #clock ida.tick matches 5 run function dungeons_arise:boss/visual/animate with entity @s data
execute if score #clock ida.tick matches 10 run function dungeons_arise:boss/visual/animate with entity @s data
execute if score #clock ida.tick matches 15 run function dungeons_arise:boss/visual/animate with entity @s data
execute if score #clock ida.tick matches 20 run function dungeons_arise:boss/visual/animate with entity @s data
