scoreboard players operation #resolved nx.skill = #skill nx.skill
tag @a remove nox.hit
execute if score #skill nx.skill matches 1 at @e[tag=nox.target,limit=1] run function eclipse_nox:skills/cleave_hit
execute if score #skill nx.skill matches 2 at @e[tag=nox.target,limit=1] run function eclipse_nox:skills/ring_hit
execute if score #skill nx.skill matches 1 if score #chain nx.combo matches 0 run function eclipse_nox:skills/combo
execute if score #resolved nx.skill matches 1 if score #chain nx.combo matches 2 run function eclipse_nox:skills/recover
execute if score #resolved nx.skill matches 2..4 run function eclipse_nox:skills/recover
execute if score #resolved nx.skill matches 5 run function eclipse_nox:skills/dash/begin
execute if score #chain nx.combo matches 1 run scoreboard players set #chain nx.combo 2
playsound eclipse_nox:impact master @a[tag=nox.member] ~ ~ ~ .65 1
