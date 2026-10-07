tag @a remove nox.clicker
execute on target if entity @s[tag=nox.active] run tag @s add nox.clicker
execute if entity @a[tag=nox.clicker] if score #lock nx.lock matches 0 run function eclipse_nox:puzzle/press
data remove entity @s interaction
tag @a remove nox.clicker
