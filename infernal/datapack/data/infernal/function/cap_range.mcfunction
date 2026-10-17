attribute @s minecraft:follow_range modifier remove infernal:follow_range
execute store result score #base inf.sys run attribute @s minecraft:follow_range get 100
scoreboard players set #cap inf.sys 6400
scoreboard players operation #cap inf.sys -= #base inf.sys
execute store result storage infernal:ctx cap double 0.01 run scoreboard players get #cap inf.sys
function infernal:cap_add with storage infernal:ctx
