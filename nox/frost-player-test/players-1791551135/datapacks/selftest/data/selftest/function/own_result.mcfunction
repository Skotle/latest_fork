execute store result storage selftest:results own_immune int 1 run execute if score #pool fw.hp = #probe_pool fw.hp
kill @e[tag=fw.arrow]
data modify storage selftest:shot owner set from entity @a[tag=probe.player,limit=1] UUID
function selftest:external_arrow with storage selftest:shot
