execute store result storage selftest:results direct_after int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
execute store result storage selftest:results direct_blasts int 1 run scoreboard players get #blasts fw.tmp
execute store result storage selftest:results damage_tracked int 1 run scoreboard players get @a[tag=probe.player,limit=1] fw.hits
scoreboard players set #blasts fw.tmp 0
function frost_warden:bomb/mark
execute store result storage selftest:results mark_z int 1 run data get entity @e[tag=fw.bomb_mark,limit=1] Pos[2]
tp @a[tag=probe.player] 128 81 8
execute store result storage selftest:results mark_stays int 1 run data get entity @e[tag=fw.bomb_mark,limit=1] Pos[2]
