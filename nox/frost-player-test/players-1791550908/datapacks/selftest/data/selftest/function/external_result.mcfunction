execute store result storage selftest:results external_hits int 1 run execute if score #pool fw.hp < #probe_pool fw.hp
execute store result storage selftest:results hawk_before int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
scoreboard players set #cycle fw.cycle 5
function frost_warden:skills/begin
execute store result storage selftest:results hawk int 1 run execute if entity @e[tag=fw.hawk]
scoreboard players set #cast fw.cast 0
scoreboard players set #safe fw.safe 99999
scoreboard players set #next fw.next 99999
