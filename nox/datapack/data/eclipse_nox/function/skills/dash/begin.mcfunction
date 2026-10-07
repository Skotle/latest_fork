scoreboard players set #dash nx.dash 18
scoreboard players set #safe nx.safe 0
tag @a remove nox.dashhit
execute at @e[tag=nox.boss,limit=1] run playsound eclipse_nox:impact master @a[tag=nox.member] ~ ~ ~ 1 .7
scoreboard players set #counter nx.move 0
scoreboard players set #crash nx.move 0
