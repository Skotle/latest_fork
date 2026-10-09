execute store result storage selftest:results shield_control int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
kill @e[tag=probe.control]
execute store result storage selftest:results shield_before_boss int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
execute positioned 128 82 -8 rotated 180 0 run function frost_warden:arrows/normal
