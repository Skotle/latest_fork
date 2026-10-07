data modify entity @s data.period set value 12
effect clear @s minecraft:speed
attribute @s minecraft:scale base set 1.15
data modify entity @s data.balance_version set value 2
execute unless data entity @s data{visual_version:1} run function dungeons_arise:boss/visual/setup with entity @s data
attribute @s minecraft:attack_damage base set 4
