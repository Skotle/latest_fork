time set noon
weather clear
forceload add 96 -32 160 48
execute positioned 128 81 0 run function frost_warden:admin/install
tp @a[tag=probe.player] 128 81 -12
execute positioned 128 81 0 run function frost_warden:admin/summon
function frost_warden:tick
execute store result storage selftest:results boss int 1 run execute if entity @e[tag=fw.boss]
execute store result storage selftest:results health int 1 run scoreboard players get #max fw.max
execute store result storage selftest:results bow int 1 run execute if items entity @e[tag=fw.boss,limit=1] weapon.mainhand minecraft:bow
scoreboard players set #next fw.next 99999
scoreboard players set #safe fw.safe 99999
scoreboard players set #blink fw.blink 99999
data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}
damage @e[tag=fw.boss,limit=1] 10 minecraft:fall
