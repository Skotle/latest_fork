tag @e[tag=nox.anchor] remove nox.current
tag @e[tag=nox.anchor,distance=..40,sort=nearest,limit=1] add nox.current
scoreboard players operation #active_site nx.tmp = @e[tag=nox.current,limit=1] nx.tmp
execute as @e[tag=nox.anchor,tag=nox.current,limit=1] at @s run function eclipse_nox:fight/start
execute unless score #state nx.state matches 1 run tag @e[tag=nox.current] remove nox.current
