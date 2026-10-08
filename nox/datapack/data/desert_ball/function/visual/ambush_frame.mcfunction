scoreboard players set #mode db.anim 3
scoreboard players set #frame db.motion 12
scoreboard players operation #frame db.motion -= #follow db.anim
scoreboard players set #tail db.tmp 9
scoreboard players operation #frame db.motion *= #tail db.tmp
scoreboard players set #length db.tmp 12
scoreboard players operation #frame db.motion /= #length db.tmp
scoreboard players add #frame db.motion 14
