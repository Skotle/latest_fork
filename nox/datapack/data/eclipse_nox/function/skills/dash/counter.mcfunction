scoreboard players set #safe nx.safe 40
scoreboard players set #next nx.next 0
scoreboard players set #expose nx.expose 1
scoreboard players set #counter nx.move 1
execute store result score #oldhp nx.hp run data get entity @e[tag=nox.boss,limit=1] Health 100
playsound eclipse_nox:expose master @a[tag=nox.member] ~ ~ ~ 1 1.4
tellraw @a[tag=nox.member] {"text": "벽 충돌! 2초 동안 카운터 가능 — 녹스에게 주는 피해 2배!", "color": "gold"}
