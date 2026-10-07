execute if score #state nx.state matches 0 in minecraft:overworld as @e[tag=nox.anchor,distance=..40,sort=nearest,limit=1] at @s run function eclipse_nox:site/remove
execute if score #state nx.state matches 1 run tellraw @s {"text":"먼저 전투를 중단하세요: /function eclipse_nox:admin/abort","color":"yellow"}
