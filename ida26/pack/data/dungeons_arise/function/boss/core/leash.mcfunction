$execute at @e[type=minecraft:marker,tag=ida.site,scores={ida.sid=$(id)},limit=1] unless entity @s[distance=..24] run function dungeons_arise:boss/core/return with entity @s data
