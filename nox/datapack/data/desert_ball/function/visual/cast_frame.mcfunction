scoreboard players set #length db.tmp 24
execute if score #skill db.skill matches 2..3 run scoreboard players set #length db.tmp 40
execute if score #skill db.skill matches 4 run scoreboard players set #length db.tmp 36
execute if score #skill db.skill matches 5..6 run scoreboard players set #length db.tmp 30
scoreboard players operation #frame db.motion = #length db.tmp
scoreboard players operation #frame db.motion -= #cast db.cast
scoreboard players set #last db.tmp 23
scoreboard players operation #frame db.motion *= #last db.tmp
scoreboard players operation #frame db.motion /= #length db.tmp
