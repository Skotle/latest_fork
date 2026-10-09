tp @a[tag=probe.player] 128 81 -12 0 0
execute store result storage selftest:results stun_before int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
execute positioned 128 82 -8 rotated 180 0 run function frost_warden:arrows/stun
execute store result storage selftest:results stun_arrow int 1 run execute if entity @e[tag=fw.stun_arrow,nbt={damage:5.0d,PierceLevel:1b}]
