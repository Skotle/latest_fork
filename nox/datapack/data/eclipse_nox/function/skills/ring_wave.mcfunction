tag @a remove nox.hit
execute at @e[tag=nox.target,limit=1] run function eclipse_nox:skills/ring_hit
execute at @e[tag=nox.target,limit=1] run particle minecraft:explosion ~ ~.2 ~ 1 0 1 0 5 force @a[tag=nox.member]
playsound eclipse_nox:bell_low master @a[tag=nox.member] ~ ~ ~ .8 .8
