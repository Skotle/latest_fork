execute as @a[tag=nox.active] at @s run summon minecraft:marker ~ ~ ~ {Tags:["nox.owned","nox.echo"]}
scoreboard players set @e[tag=nox.echo] nx.time 20
tellraw @a[tag=nox.member] {"text": "잔향 — 지금 발자국이 1초 후 폭발한다. 이동!", "color": "gold"}
