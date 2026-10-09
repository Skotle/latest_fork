scoreboard players add #blasts fw.tmp 1
particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 force @a[distance=..64]
playsound minecraft:entity.generic.explode hostile @a[distance=..64] ~ ~ ~ 1.3 1.2
execute as @a[tag=fw.active,distance=..3] run function frost_warden:explosion/check
