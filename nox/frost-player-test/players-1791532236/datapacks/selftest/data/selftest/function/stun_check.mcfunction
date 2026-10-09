data get entity @a[tag=probe.player,limit=1] active_effects
execute store result storage selftest:results stun_after int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
execute store result storage selftest:results stunned int 1 run execute if entity @a[tag=fw.stunned]
execute store result storage selftest:results stun_effect int 1 run execute if entity @a[tag=probe.player,nbt={active_effects:[{id:"minecraft:slowness",amplifier:6b}]}]
