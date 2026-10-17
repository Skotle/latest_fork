execute if entity @s[tag=inf.active] run function infernal:restore
scoreboard players operation @s inf.rev = #epoch inf.sys
execute if score #level inf.sys matches ..3 run return 0
execute unless score @s inf.id matches 1.. run function infernal:identify
function infernal:context
function infernal:snapshot with storage infernal:ctx
execute store result score #oldhp inf.sys run data get entity @s Health 100
execute store result score #oldmax inf.sys run attribute @s minecraft:max_health get 100
execute if score #level inf.sys matches 4 run function infernal:apply/harder
execute if score #level inf.sys matches 5 run function infernal:apply/insane
execute if score #level inf.sys matches 6 run function infernal:apply/demon
execute if score #level inf.sys matches 7 run function infernal:apply/nightmare
tag @s add inf.active
function infernal:health
