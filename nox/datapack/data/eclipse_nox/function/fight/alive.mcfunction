function eclipse_nox:expansion/tick
function eclipse_nox:hazards/tick
function eclipse_nox:fight/exposure
execute store result score #hp nx.hp run data get entity @e[tag=nox.boss,limit=1] Health 100
execute store result bossbar eclipse_nox:health value run data get entity @e[tag=nox.boss,limit=1] Health
scoreboard players operation #ratio nx.tmp = #hp nx.hp
scoreboard players operation #ratio nx.tmp /= #max nx.max
execute if score #phase nx.phase matches 1 if score #ratio nx.tmp matches ..65 run function eclipse_nox:fight/phase2
execute if score #phase nx.phase matches 2 if score #ratio nx.tmp matches ..30 if score #puzzle nx.puzzle matches 0 run function eclipse_nox:fight/phase3
execute if score #lock nx.lock matches 1.. run scoreboard players remove #lock nx.lock 1
execute if score #safe nx.safe matches 1.. run scoreboard players remove #safe nx.safe 1
execute if score #puzzle nx.puzzle matches 1 run function eclipse_nox:puzzle/tick
execute if score #cast nx.cast matches 1.. run function eclipse_nox:skills/casting
execute as @e[tag=nox.boss,limit=1] unless entity @s[distance=..21] run tp @s ~ ~ ~
function eclipse_nox:fight/move
execute if score #dash nx.dash matches 1.. run function eclipse_nox:skills/dash/tick
execute if score #cast nx.cast matches 0 if score #dash nx.dash matches 0 if score #puzzle nx.puzzle matches 0 if score #safe nx.safe matches 0 if entity @a[tag=nox.active] run scoreboard players remove #next nx.next 1
execute if score #cast nx.cast matches 0 if score #dash nx.dash matches 0 if score #puzzle nx.puzzle matches 0 if score #safe nx.safe matches 0 if score #next nx.next matches ..0 if entity @a[tag=nox.active] run function eclipse_nox:skills/begin
execute as @e[tag=nox.bodypart] at @e[tag=nox.boss,limit=1] run tp @s ~ ~ ~ ~ 0
function eclipse_nox:visual/tick
execute if score #time nx.time matches 7200.. run function eclipse_nox:admin/abort
