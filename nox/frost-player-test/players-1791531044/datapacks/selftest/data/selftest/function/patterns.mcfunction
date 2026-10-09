kill @e[tag=fw.arrow]
kill @e[tag=fw.tracker]
data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}
tp @e[tag=fw.boss,limit=1] 128 81 -2
execute at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ rotated 0 0 run function frost_warden:skills/radial
execute at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ rotated 11.25 0 run function frost_warden:skills/radial
execute store result storage selftest:results radial_count int 1 run execute if entity @e[tag=fw.arrow]
execute store result storage selftest:results radial_piercing int 1 run execute if entity @e[tag=fw.arrow,nbt={PierceLevel:1b}]
scoreboard players set #east fw.tmp 0
scoreboard players set #west fw.tmp 0
scoreboard players set #north fw.tmp 0
scoreboard players set #south fw.tmp 0
execute as @e[tag=fw.arrow] run function selftest:direction
execute store result storage selftest:results radial_east int 1 run execute if score #east fw.tmp matches 1..
execute store result storage selftest:results radial_west int 1 run execute if score #west fw.tmp matches 1..
execute store result storage selftest:results radial_north int 1 run execute if score #north fw.tmp matches 1..
execute store result storage selftest:results radial_south int 1 run execute if score #south fw.tmp matches 1..
kill @e[tag=fw.arrow]
execute at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ run function frost_warden:skills/ring
execute store result storage selftest:results ring_count int 1 run execute if entity @e[tag=fw.ring]
