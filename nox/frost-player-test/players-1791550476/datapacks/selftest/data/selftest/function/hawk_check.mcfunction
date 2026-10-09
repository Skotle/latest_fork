execute store result storage selftest:results hawk_after int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
execute store result storage selftest:results revealed int 1 run execute if entity @a[tag=fw.revealed]
execute store result storage selftest:results hawk_finished int 1 run execute unless entity @e[tag=fw.hawk]
attribute @a[tag=probe.player,limit=1] minecraft:knockback_resistance base set 1
item replace entity @a[tag=probe.player,limit=1] weapon.offhand with minecraft:shield
tp @a[tag=probe.player] 128 81 -12 0 0
tag @a[tag=probe.player] add probe.shield
