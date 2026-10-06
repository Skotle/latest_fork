scoreboard players operation #mod ida.tmp = #clock ida.tick
scoreboard players set #five ida.tmp 5
scoreboard players operation #mod ida.tmp %= #five ida.tmp
execute if score #mod ida.tmp matches 0 in minecraft:overworld as @e[tag=ida.boss] at @s run function dungeons_arise:boss/core/fast with entity @s data
execute if score #mod ida.tmp matches 0 in minecraft:the_nether as @e[tag=ida.boss] at @s run function dungeons_arise:boss/core/fast with entity @s data
execute if score #mod ida.tmp matches 0 in minecraft:the_end as @e[tag=ida.boss] at @s run function dungeons_arise:boss/core/fast with entity @s data
