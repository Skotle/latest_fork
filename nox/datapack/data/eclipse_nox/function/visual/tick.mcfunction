scoreboard players set #anim nx.anim 0
execute if score #moving nx.move matches 1 run scoreboard players set #anim nx.anim 1
execute if score #cast nx.cast matches 1.. run scoreboard players set #anim nx.anim 2
execute if score #cast nx.cast matches 1..8 run scoreboard players set #anim nx.anim 3
execute if score #safe nx.safe matches 1.. run scoreboard players set #anim nx.anim 4
execute if score #dash nx.dash matches 1.. run scoreboard players set #anim nx.anim 5
execute if score #expose nx.expose matches 1 if score #safe nx.safe matches 11.. run scoreboard players set #anim nx.anim 6
execute if score #puzzle nx.puzzle matches 1 run scoreboard players set #anim nx.anim 7
execute if score #skill nx.skill matches 4 if score #cast nx.cast matches 1.. run scoreboard players set #anim nx.anim 7
execute unless score #anim nx.anim = #previous nx.anim run scoreboard players set #animtime nx.anim 0
scoreboard players operation #previous nx.anim = #anim nx.anim
scoreboard players add #animtime nx.anim 1
scoreboard players operation #frame nx.tmp = #animtime nx.anim
scoreboard players set #two nx.tmp 2
scoreboard players set #sixteen nx.tmp 16
scoreboard players operation #frame nx.tmp /= #two nx.tmp
scoreboard players operation #frame nx.tmp %= #sixteen nx.tmp
execute if score #anim nx.anim matches 2 run function eclipse_nox:visual/frame/wind
execute if score #anim nx.anim matches 3 run function eclipse_nox:visual/frame/impact
execute if score #anim nx.anim matches 4 run function eclipse_nox:visual/frame/recover
execute store result storage eclipse_nox:motion frame int 1 run scoreboard players get #frame nx.tmp
execute if score #anim nx.anim matches 0 run data modify storage eclipse_nox:motion pose set value "idle"
execute if score #anim nx.anim matches 1 run data modify storage eclipse_nox:motion pose set value "walk"
execute if score #anim nx.anim matches 2 run data modify storage eclipse_nox:motion pose set value "wind"
execute if score #anim nx.anim matches 3 run data modify storage eclipse_nox:motion pose set value "impact"
execute if score #anim nx.anim matches 4 run data modify storage eclipse_nox:motion pose set value "recover"
execute if score #anim nx.anim matches 5 run data modify storage eclipse_nox:motion pose set value "dash"
execute if score #anim nx.anim matches 6 run data modify storage eclipse_nox:motion pose set value "stagger"
execute if score #anim nx.anim matches 7 run data modify storage eclipse_nox:motion pose set value "ritual"
scoreboard players operation #fx nx.tmp = #time nx.time
scoreboard players operation #fx nx.tmp %= #two nx.tmp
execute if score #fx nx.tmp matches 0 run function eclipse_nox:visual/apply with storage eclipse_nox:motion
