scoreboard players remove @e[tag=nox.echo] nx.time 1
scoreboard players remove @e[tag=nox.overload] nx.time 1
execute as @e[tag=nox.echo] at @s run particle minecraft:reverse_portal ~ ~.1 ~ 1.3 .05 1.3 .01 12 force @a[tag=nox.member]
execute as @e[tag=nox.overload] at @s run particle minecraft:electric_spark ~ ~.5 ~ 2 .2 2 .02 15 force @a[tag=nox.member]
tag @a remove nox.hit
execute as @e[tag=nox.echo,scores={nx.time=..0}] at @s run function eclipse_nox:hazards/echo
tag @a remove nox.hit
execute as @e[tag=nox.overload,scores={nx.time=..0}] at @s run function eclipse_nox:hazards/overload
