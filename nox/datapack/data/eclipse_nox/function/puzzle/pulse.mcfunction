scoreboard players set #puzzletime nx.tmp 0
execute as @a[tag=nox.active] at @s run summon minecraft:marker ~ ~ ~ {Tags:["nox.owned","nox.echo"]}
scoreboard players set @e[tag=nox.echo] nx.time 20
tellraw @a[tag=nox.member] {"text": "발자국이 기록됐다. 1초 후 잔향 폭발!", "color": "gold"}
