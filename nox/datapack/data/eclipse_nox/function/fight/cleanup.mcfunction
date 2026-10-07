scoreboard players set #dash nx.dash 0
scoreboard players set #expose nx.expose 0
tag @a remove nox.dashhit
kill @e[tag=nox.bodypart]
kill @e[tag=nox.boss]
kill @e[tag=nox.target]
kill @e[tag=nox.echo]
kill @e[tag=nox.overload]
execute as @e[tag=nox.bell,type=minecraft:interaction] run data remove entity @s interaction
bossbar set eclipse_nox:health visible false
bossbar set eclipse_nox:health players
scoreboard players set #cast nx.cast 0
scoreboard players set #puzzle nx.puzzle 0
tag @a remove nox.member
tag @a remove nox.active
execute at @e[tag=nox.anchor,tag=nox.current,limit=1] run function eclipse_nox:arena/open
tag @e[tag=nox.current] remove nox.current
kill @e[tag=nox.minion]
kill @e[tag=nox.minion_visual]
scoreboard players set #judgement nx.doom 0
tag @a remove nox.doom_safe
scoreboard players set #counter nx.move 0
scoreboard players set #break nx.add 0
