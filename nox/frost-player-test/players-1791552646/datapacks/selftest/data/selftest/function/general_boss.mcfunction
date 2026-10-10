execute store result storage selftest:results general_normal_after int 1 run data get entity @a[tag=probe.player,limit=1] Health 1000
execute store result storage selftest:results general_boss_before int 1 run data get entity @a[tag=probe.player,limit=1] Health 1000
damage @a[tag=probe.player,limit=1] 100 minecraft:arrow by @e[tag=fw.boss,limit=1]
