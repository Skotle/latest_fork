execute store result storage selftest:results external_physical_hits int 1 run execute if score #pool fw.hp < #probe_pool fw.hp
execute as @e[tag=fw.add] run data merge entity @s {NoAI:0b}
