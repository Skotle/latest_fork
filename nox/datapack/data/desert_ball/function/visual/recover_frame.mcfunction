scoreboard players set #frame db.motion 10
scoreboard players operation #frame db.motion -= #safe db.safe
scoreboard players set #last db.tmp 23
scoreboard players operation #frame db.motion *= #last db.tmp
scoreboard players set #length db.tmp 10
scoreboard players operation #frame db.motion /= #length db.tmp
