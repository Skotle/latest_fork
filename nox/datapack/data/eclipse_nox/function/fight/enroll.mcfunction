execute store result score @s nx.tmp run data get entity @s Pos[1] 100
execute if score @s nx.tmp >= #ymin nx.tmp if score @s nx.tmp <= #ymax nx.tmp run tag @s add nox.member
