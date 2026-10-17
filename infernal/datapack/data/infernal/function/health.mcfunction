execute store result score #newmax inf.sys run attribute @s minecraft:max_health get 100
scoreboard players set #scale inf.sys 1000
scoreboard players operation #oldhp inf.sys *= #scale inf.sys
scoreboard players operation #oldhp inf.sys /= #oldmax inf.sys
scoreboard players operation #oldhp inf.sys *= #newmax inf.sys
scoreboard players operation #oldhp inf.sys /= #scale inf.sys
execute store result entity @s Health float 0.01 run scoreboard players get #oldhp inf.sys
