$scoreboard players set @s ida.sid $(id)
scoreboard players set @s ida.age 0
$team join ida$(id) @s
effect give @s minecraft:fire_resistance infinite 0 true
tag @s remove ida.newadd
