execute store result storage selftest:results bound_after_stun int 1 run execute if entity @a[tag=fw.bound,tag=!fw.stunned,nbt={active_effects:[{id:"minecraft:slowness",amplifier:1b,duration:-1}]}]
execute as @a[tag=probe.player] run function frost_warden:debuff/clear
execute store result storage selftest:results binding_cleared int 1 run execute unless entity @a[tag=fw.bound]
scoreboard players set #time fw.time 1199
function frost_warden:fight/alive
execute store result storage selftest:results enrage_binding int 1 run execute if entity @a[tag=fw.bound]
execute store result storage selftest:results blink_before double 1 run data get entity @e[tag=fw.boss,limit=1] Pos[0]
scoreboard players set #teleports fw.tmp 0
scoreboard players set #blink fw.blink 1
function frost_warden:teleport/tick
execute store result storage selftest:results blink_moved int 1 run scoreboard players get #teleports fw.tmp
execute store result storage selftest:results blink_points int 1 run execute if entity @e[tag=fw.teleport_point]
execute at @e[tag=fw.boss,limit=1] store success storage selftest:results blink_safe int 1 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless block ~ ~-1 ~ #frost_warden:blast_pass
scoreboard players set #safe fw.safe 0
scoreboard players set #next fw.next 0
