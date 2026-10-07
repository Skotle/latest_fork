execute if score #phase nx.phase matches ..2 as @a[tag=nox.active,tag=!nox.hit,distance=3..6] run function eclipse_nox:damage/4
execute if score #phase nx.phase matches 3 if score #cast nx.cast matches 48.. as @a[tag=nox.active,tag=!nox.hit,distance=3..6] run function eclipse_nox:damage/4
execute if score #phase nx.phase matches 3 if score #cast nx.cast matches 24..47 as @a[tag=nox.active,tag=!nox.hit,distance=7..10] run function eclipse_nox:damage/4
execute if score #phase nx.phase matches 3 if score #cast nx.cast matches ..23 as @a[tag=nox.active,tag=!nox.hit,distance=11..14] run function eclipse_nox:damage/4
