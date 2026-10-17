execute store result score #oldhp inf.sys run data get entity @s Health 100
execute store result score #oldmax inf.sys run attribute @s minecraft:max_health get 100
execute if data entity @s attributes[{id:"minecraft:max_health"}].modifiers[{id:"infernal:max_health"}] run attribute @s minecraft:max_health modifier remove infernal:max_health
execute if data entity @s attributes[{id:"minecraft:attack_damage"}].modifiers[{id:"infernal:attack_damage"}] run attribute @s minecraft:attack_damage modifier remove infernal:attack_damage
execute if data entity @s attributes[{id:"minecraft:movement_speed"}].modifiers[{id:"infernal:movement_speed"}] run attribute @s minecraft:movement_speed modifier remove infernal:movement_speed
execute if data entity @s attributes[{id:"minecraft:follow_range"}].modifiers[{id:"infernal:follow_range"}] run attribute @s minecraft:follow_range modifier remove infernal:follow_range
function infernal:context
function infernal:restore_data with storage infernal:ctx
function infernal:health
tag @s remove inf.gear
tag @s remove inf.active
