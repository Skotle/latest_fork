scoreboard players set #skill db.skill 1
function desert_ball:skills/shoot
execute as @e[tag=db.shot] at @a[tag=probe.player,limit=1] run tp @s ~ ~ ~ 0 0
execute as @e[tag=db.shot] at @s run function desert_ball:shot/tick
execute store result storage selftest:results after_hit int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
function desert_ball:abort
