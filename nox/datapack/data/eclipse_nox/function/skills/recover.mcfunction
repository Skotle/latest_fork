kill @e[tag=nox.target]
scoreboard players set #safe nx.safe 12
scoreboard players set #next nx.next 2
execute if score #phase nx.phase matches 3 run scoreboard players set #next nx.next 2
execute if score #skill nx.skill matches 4 run scoreboard players set #safe nx.safe 20
execute if score #skill nx.skill matches 4 run scoreboard players set #expose nx.expose 1
