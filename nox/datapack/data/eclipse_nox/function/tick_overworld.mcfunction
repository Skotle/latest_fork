execute as @e[tag=nox.seed] at @s if entity @a[distance=..88] run function eclipse_nox:site/init
execute as @e[tag=nox.anchor] unless score @s nx.tmp matches 1.. run function eclipse_nox:site/identify
execute if score #state nx.state matches 1 as @e[tag=nox.anchor,tag=nox.current] unless score @s nx.tmp = #active_site nx.tmp at @s run function eclipse_nox:site/retire
execute if score #state nx.state matches 1 unless entity @e[tag=nox.anchor,tag=nox.current] run function eclipse_nox:fight/abort
execute if score #state nx.state matches 0 as @e[tag=nox.anchor,tag=nox.current] at @s run function eclipse_nox:arena/open
execute if score #state nx.state matches 0 run tag @e[tag=nox.current] remove nox.current
execute if score #state nx.state matches 0 run kill @e[tag=nox.target]
execute if score #state nx.state matches 0 run kill @e[tag=nox.echo]
execute if score #state nx.state matches 0 run kill @e[tag=nox.overload]
execute if score #state nx.state matches 0 as @e[tag=nox.start] at @s if data entity @s interaction run function eclipse_nox:site/request
execute as @e[tag=nox.start] run data remove entity @s interaction
execute if score #state nx.state matches 1 as @e[tag=nox.anchor,tag=nox.current,limit=1] at @s run function eclipse_nox:fight/tick
execute unless score #state nx.state matches 1 as @e[tag=nox.bell,type=minecraft:interaction] run data remove entity @s interaction
execute if score #state nx.state matches 0 run kill @e[tag=nox.bodypart]
execute if score #state nx.state matches 0 run kill @e[tag=nox.boss]
execute if score #state nx.state matches 0 run kill @e[tag=nox.minion]
execute if score #state nx.state matches 0 run kill @e[tag=nox.minion_visual]
execute as @e[tag=nox.anchor] at @s run advancement grant @a[distance=..38,gamemode=!spectator] only eclipse_nox:challenge/discover
