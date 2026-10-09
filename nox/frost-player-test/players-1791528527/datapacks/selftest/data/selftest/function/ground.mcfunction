scoreboard players set #safe fw.safe 99999
execute store result storage selftest:results ground_blasts int 1 run scoreboard players get #blasts fw.tmp
execute store result storage selftest:results ground_arrows_cleared int 1 run execute unless entity @e[tag=fw.explosive]
scoreboard players set #blasts fw.tmp 0
execute store result storage selftest:results direct_before int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
execute at @a[tag=probe.player,limit=1] positioned ~ ~4 ~ run function frost_warden:bomb/drop
