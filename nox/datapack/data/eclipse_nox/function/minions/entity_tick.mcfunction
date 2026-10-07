execute store result score @s nx.hp run data get entity @s Health 100
execute if score @s nx.hp matches ..0 unless entity @s[tag=nox.paid] run function eclipse_nox:minions/death
execute unless entity @e[tag=nox.anchor,tag=nox.current,distance=..24] at @e[tag=nox.anchor,tag=nox.current,limit=1] run tp @s ~ ~ ~
