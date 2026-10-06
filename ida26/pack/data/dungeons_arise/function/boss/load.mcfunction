execute unless data storage dungeons_arise:boss_system installed run function dungeons_arise:boss/install
scoreboard players set #clock ida.tick 0
function dungeons_arise:boss/admin/apply_balance
execute in minecraft:overworld as @e[type=minecraft:marker,tag=ida.site,scores={ida.stage=1}] at @s run function dungeons_arise:boss/site/restore with entity @s data
execute in minecraft:the_nether as @e[type=minecraft:marker,tag=ida.site,scores={ida.stage=1}] at @s run function dungeons_arise:boss/site/restore with entity @s data
execute in minecraft:the_end as @e[type=minecraft:marker,tag=ida.site,scores={ida.stage=1}] at @s run function dungeons_arise:boss/site/restore with entity @s data
