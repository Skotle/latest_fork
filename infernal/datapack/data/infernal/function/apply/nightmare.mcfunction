execute if entity @s[type=#infernal:ordinary] run attribute @s minecraft:max_health modifier add infernal:max_health 1.00000 add_multiplied_total
execute if entity @s[type=#infernal:melee] run attribute @s minecraft:attack_damage modifier add infernal:attack_damage 0.80000 add_multiplied_total
execute if entity @s[type=#infernal:melee] unless entity @s[nbt={IsBaby:1b}] run attribute @s minecraft:movement_speed modifier add infernal:movement_speed 0.10000 add_multiplied_total
scoreboard players set #range inf.sys 0
execute if entity @s[type=#infernal:ordinary] store result score #range inf.sys run attribute @s minecraft:follow_range get 100
execute if entity @s[type=#infernal:ordinary] if score #range inf.sys matches 1.. run attribute @s minecraft:follow_range modifier add infernal:follow_range 0.50000 add_multiplied_total
execute if entity @s[type=#infernal:ordinary] store result score #range inf.sys run attribute @s minecraft:follow_range get 100
execute if score #range inf.sys matches 6401.. run function infernal:cap_range
execute if entity @s[type=#infernal:boss] run attribute @s minecraft:max_health modifier add infernal:max_health 0.50000 add_multiplied_total
execute if entity @s[type=minecraft:creeper] run data merge entity @s {Fuse:20s}
execute if entity @s[type=#infernal:armor] run function infernal:gear/nightmare
