tag @s add nox.paid
scoreboard players operation #carrier nx.mid = @s nx.mid
execute as @e[tag=nox.minion_visual] if score @s nx.mid = #carrier nx.mid run kill @s
