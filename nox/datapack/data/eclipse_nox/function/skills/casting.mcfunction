scoreboard players remove #cast nx.cast 1
execute if score #skill nx.skill matches 1 at @e[tag=nox.target,limit=1] run function eclipse_nox:skills/cleave_warn
execute if score #skill nx.skill matches 2 at @e[tag=nox.target,limit=1] run function eclipse_nox:skills/ring_warn
execute if score #skill nx.skill matches 5 at @e[tag=nox.target,limit=1] run function eclipse_nox:skills/dash/warn
execute if score #phase nx.phase matches 3 if score #skill nx.skill matches 2 if score #cast nx.cast matches 48 run function eclipse_nox:skills/ring_wave
execute if score #phase nx.phase matches 3 if score #skill nx.skill matches 2 if score #cast nx.cast matches 24 run function eclipse_nox:skills/ring_wave
execute if score #skill nx.skill matches 4 run function eclipse_nox:skills/eclipse_tick
execute if score #cast nx.cast matches 0 run function eclipse_nox:skills/resolve
