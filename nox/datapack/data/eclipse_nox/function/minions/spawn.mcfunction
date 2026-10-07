execute store result score #count nx.add if entity @e[tag=nox.minion]
execute if score #count nx.add matches 0 positioned ~-10 ~ ~-8 run function eclipse_nox:minions/spawn_acolyte
execute if score #count nx.add matches 0 positioned ~10 ~ ~8 run function eclipse_nox:minions/spawn_warden
