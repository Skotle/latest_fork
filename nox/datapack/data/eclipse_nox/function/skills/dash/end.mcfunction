kill @e[tag=nox.target]
scoreboard players set #safe nx.safe 16
scoreboard players set #next nx.next 2
scoreboard players set #expose nx.expose 0
scoreboard players set #counter nx.move 0
execute if score #crash nx.move matches 1 run function eclipse_nox:skills/dash/counter
scoreboard players set #crash nx.move 0
