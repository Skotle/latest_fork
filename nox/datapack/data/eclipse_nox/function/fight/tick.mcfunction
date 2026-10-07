scoreboard players add #time nx.time 1
tag @a remove nox.active
execute as @a[tag=nox.member,distance=..24,gamemode=survival] if score @s nx.death = @s nx.olddeath if score @s nx.leave = @s nx.oldleave run tag @s add nox.active
execute as @a[tag=nox.member,distance=..24,gamemode=adventure] if score @s nx.death = @s nx.olddeath if score @s nx.leave = @s nx.oldleave run tag @s add nox.active
execute as @a[tag=nox.member,distance=..26,tag=!nox.active] unless score #grace nx.grace matches 1.. run tp @s ~0 ~1 ~30
execute as @a[tag=!nox.member,distance=..24,gamemode=!spectator] run tp @s ~0 ~1 ~30
execute if score #grace nx.grace matches 1.. run scoreboard players remove #grace nx.grace 1
execute if score #grace nx.grace matches 1 run function eclipse_nox:arena/close
execute unless entity @a[tag=nox.active] unless score #grace nx.grace matches 1.. run scoreboard players add #idle nx.idle 1
execute if entity @a[tag=nox.active] run scoreboard players set #idle nx.idle 0
execute if score #idle nx.idle matches 100.. run function eclipse_nox:admin/abort
execute if score #state nx.state matches 1 unless entity @e[tag=nox.boss] run function eclipse_nox:fight/victory
execute if score #state nx.state matches 1 run function eclipse_nox:fight/alive
