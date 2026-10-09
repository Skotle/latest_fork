execute store result storage selftest:results shield_after_boss int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
execute store result storage selftest:results burst_before int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
execute at @a[tag=probe.player,limit=1] positioned ~ ~1 ~ run function frost_warden:explosion
execute store result storage selftest:results burst_after int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
tag @a[tag=probe.player] remove probe.shield
item replace entity @a[tag=probe.player,limit=1] weapon.offhand with minecraft:air
