scoreboard players add #next ida.sid 1
scoreboard players operation @s ida.sid = #next ida.sid
execute store result entity @s data.id int 1 run scoreboard players get @s ida.sid
scoreboard players set @s ida.stage 0
scoreboard players set @s ida.cool 0
scoreboard players set @s ida.idle 0
tag @s remove ida.newsite
