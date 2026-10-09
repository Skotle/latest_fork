execute store result storage selftest:results won int 1 run execute if entity @a[tag=probe.player,advancements={frost_warden:victory=true}]
execute store result storage selftest:results emeralds int 1 run clear @a[tag=probe.player] minecraft:emerald 0
execute store result storage selftest:results won_cleanup int 1 run execute unless entity @e[tag=fw.owned]
data get storage selftest:results
