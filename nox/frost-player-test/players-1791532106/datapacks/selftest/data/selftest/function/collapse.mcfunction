execute store result storage selftest:results ring_hover int 1 run execute if entity @e[tag=fw.ring,nbt={NoGravity:1b,Motion:[0d,0d,0d]}]
function frost_warden:skills/collapse
execute store result storage selftest:results collapse_count int 1 run execute if entity @e[tag=fw.arrow]
execute store result storage selftest:results ring_cleared int 1 run execute unless entity @e[tag=fw.ring]
execute store result score #bx fw.tmp run data get entity @e[tag=fw.boss,limit=1] Pos[0] 1000
execute store result score #bz fw.tmp run data get entity @e[tag=fw.boss,limit=1] Pos[2] 1000
scoreboard players set #converging fw.tmp 0
execute as @e[tag=fw.arrow] run function selftest:dot
execute store result storage selftest:results converging int 1 run scoreboard players get #converging fw.tmp
kill @e[tag=fw.arrow]
attribute @a[tag=probe.player,limit=1] minecraft:knockback_resistance base set 1
item replace entity @a[tag=probe.player,limit=1] weapon.offhand with minecraft:shield
tp @a[tag=probe.player] 128 81 -12 0 0
tag @a[tag=probe.player] add probe.shield
