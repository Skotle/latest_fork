tag @a remove nox.doom_safe
tag @a[tag=nox.active,distance=..4] add nox.doom_safe
execute as @a[tag=nox.active,tag=!nox.doom_safe] run damage @s 1000000 minecraft:generic_kill
scoreboard players set #cast nx.cast 0
scoreboard players set #safe nx.safe 16
scoreboard players set #next nx.next 2
scoreboard players set #expose nx.expose 1
playsound minecraft:entity.warden.sonic_boom master @a[tag=nox.member] ~ ~ ~ 1 .6
tellraw @a[tag=nox.member] {"text": "심판 종료 — 녹스의 심장이 잠시 노출됩니다!", "color": "gold"}
