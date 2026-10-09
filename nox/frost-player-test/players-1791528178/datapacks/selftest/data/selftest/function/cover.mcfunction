fill 127 81 -7 129 85 -7 minecraft:stone_bricks
execute store result storage selftest:results cover_before int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
execute positioned 128 82 -6 run function frost_warden:explosion
execute store result storage selftest:results cover_after int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
execute store result storage selftest:results cover_survived int 1 run execute if block 128 82 -7 minecraft:stone_bricks
scoreboard players set #blasts fw.tmp 0
execute positioned 138 85 -8 run function frost_warden:bomb/drop
