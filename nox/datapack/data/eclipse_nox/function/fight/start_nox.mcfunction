tag @a remove nox.member
tag @a remove nox.active
execute store result score #ymin nx.tmp run data get entity @s Pos[1] 100
scoreboard players operation #ymax nx.tmp = #ymin nx.tmp
scoreboard players remove #ymin nx.tmp 100
scoreboard players add #ymax nx.tmp 400
execute as @a[distance=..34,gamemode=survival] run function eclipse_nox:fight/enroll
execute as @a[distance=..34,gamemode=adventure] run function eclipse_nox:fight/enroll
execute if entity @a[tag=nox.member] run function eclipse_nox:fight/begin
