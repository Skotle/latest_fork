execute as @e[tag=nox.minion] at @s run function eclipse_nox:minions/entity_tick
tag @e[tag=nox.minion_visual] remove nox.riding
kill @e[tag=nox.minion_visual,tag=!nox.riding]
execute if entity @e[tag=nox.minion] run scoreboard players set #adds nx.add 0
execute unless entity @e[tag=nox.minion] run scoreboard players add #adds nx.add 1
execute if score #adds nx.add matches 360.. run function eclipse_nox:minions/reinforce
execute if score #break nx.add matches 1 if score #cast nx.cast matches 0 if score #dash nx.dash matches 0 if score #puzzle nx.puzzle matches 0 if score #safe nx.safe matches 0 run function eclipse_nox:minions/break
