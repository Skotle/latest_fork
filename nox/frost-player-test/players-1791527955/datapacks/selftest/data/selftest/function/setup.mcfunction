forceload add 96 -32 160 48
execute positioned 128 81 0 run function frost_warden:admin/install
execute positioned 128 81 0 run function frost_warden:admin/summon
execute store result storage selftest:results boss int 1 run execute if entity @e[tag=fw.boss]
execute store result storage selftest:results health int 1 run data get entity @e[tag=fw.boss,limit=1] Health
execute store result storage selftest:results visible int 1 run execute unless entity @e[tag=fw.boss,nbt={active_effects:[{id:"minecraft:invisibility"}]}]
scoreboard players set #next fw.next 99999
data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}
scoreboard players set #safe fw.safe 99999
execute store result storage selftest:results blast_before int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
execute at @a[tag=probe.player,limit=1] positioned ~ ~1 ~ run function frost_warden:explosion
execute store result storage selftest:results blast_after int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
