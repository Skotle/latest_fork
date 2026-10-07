execute store result score #x nx.tmp run data get entity @s Pos[0] 100
execute store result score #z nx.tmp run data get entity @s Pos[2] 100
scoreboard players add #rot nx.tmp 1
execute if score #rot nx.tmp matches 20.. run scoreboard players set #rot nx.tmp 0
execute if score #rot nx.tmp matches 0 run scoreboard players add #angle nx.angle 1
execute if score #angle nx.angle matches 8.. run scoreboard players set #angle nx.angle 0
execute if score #angle nx.angle matches 0 run function eclipse_nox:skills/eclipse/0
execute if score #angle nx.angle matches 1 run function eclipse_nox:skills/eclipse/1
execute if score #angle nx.angle matches 2 run function eclipse_nox:skills/eclipse/2
execute if score #angle nx.angle matches 3 run function eclipse_nox:skills/eclipse/3
execute if score #angle nx.angle matches 4 run function eclipse_nox:skills/eclipse/4
execute if score #angle nx.angle matches 5 run function eclipse_nox:skills/eclipse/5
execute if score #angle nx.angle matches 6 run function eclipse_nox:skills/eclipse/6
execute if score #angle nx.angle matches 7 run function eclipse_nox:skills/eclipse/7
