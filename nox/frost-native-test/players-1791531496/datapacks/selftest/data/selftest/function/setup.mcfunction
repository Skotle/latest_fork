forceload add 96 -32 160 48
execute positioned 128 81 0 run function frost_warden:admin/install
tp @a[tag=probe.player] 128 81 -8
execute positioned 128 81 0 run function frost_warden:admin/summon
data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}
scoreboard players set #next fw.next 99999
scoreboard players set #safe fw.safe 99999
tag @a[tag=probe.player] add probe.native
