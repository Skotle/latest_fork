scoreboard players set #chain nx.combo 1
scoreboard players set #cast nx.cast 12
scoreboard players set #total nx.total 12
execute as @e[tag=nox.target,limit=1] at @s run tp @s ~ ~ ~ ~70 0
execute as @e[tag=nox.boss,limit=1] at @s rotated as @e[tag=nox.target,limit=1] run tp @s ~ ~ ~ ~ 0
tellraw @a[tag=nox.member] {"text": "두 번째 타격 — 종이 옆으로 돌아간다! 새 불꽃 표식을 피하세요.", "color": "gold"}
