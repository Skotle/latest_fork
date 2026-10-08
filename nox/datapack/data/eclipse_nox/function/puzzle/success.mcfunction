scoreboard players set #puzzle nx.puzzle 0
scoreboard players set #safe nx.safe 20
scoreboard players set #next nx.next 2
data merge entity @e[tag=nox.boss,limit=1] {Invulnerable:0b}
playsound eclipse_nox:expose master @a[tag=nox.member] ~ ~ ~ 1 1
tellraw @a[tag=nox.member] {"text": "봉인 해제! 심장이 1초 동안 노출된다.", "color": "gold"}
scoreboard players set #expose nx.expose 1
execute store result score #oldhp nx.hp run data get entity @e[tag=nox.boss,limit=1] Health 100
advancement grant @a[tag=nox.active] only eclipse_nox:challenge/seal
execute if score #mistakes nx.tmp matches 0 run scoreboard players set #sealclean nx.tmp 1
