scoreboard players set #mode db.anim 9
scoreboard players operation #frame db.motion = #time db.time
scoreboard players set #last db.tmp 23
scoreboard players operation #frame db.motion *= #last db.tmp
scoreboard players set #length db.tmp 36
scoreboard players operation #frame db.motion /= #length db.tmp
