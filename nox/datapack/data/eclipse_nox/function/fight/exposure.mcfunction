execute store result score #seen nx.hp run data get entity @e[tag=nox.boss,limit=1] Health 100
execute if score #expose nx.expose matches 1 if score #safe nx.safe matches 1.. if score #oldhp nx.hp matches 1.. if score #seen nx.hp < #oldhp nx.hp run function eclipse_nox:fight/bonus
execute store result score #oldhp nx.hp run data get entity @e[tag=nox.boss,limit=1] Health 100
execute if score #safe nx.safe matches 0 run scoreboard players set #expose nx.expose 0
execute if score #safe nx.safe matches 0 run scoreboard players set #counter nx.move 0
