execute as @e[type=minecraft:item_display,tag=ida.visual] run function dungeons_arise:boss/visual/orphan with entity @s data
execute as @e[type=minecraft:marker,tag=ida.site] at @s run function dungeons_arise:boss/site/second with entity @s data
execute as @e[tag=ida.add] run scoreboard players add @s ida.age 1
kill @e[tag=ida.add,scores={ida.age=90..}]
