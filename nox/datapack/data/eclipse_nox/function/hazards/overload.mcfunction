execute as @a[tag=nox.active,tag=!nox.hit,distance=..4] run function eclipse_nox:damage/6
particle minecraft:explosion ~ ~.5 ~ 1 .1 1 0 6 force @a[tag=nox.member]
kill @s
