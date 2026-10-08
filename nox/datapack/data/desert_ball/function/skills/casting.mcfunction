scoreboard players remove #cast db.cast 1
execute if score #skill db.skill matches 2 if score #cast db.cast matches 39 at @e[tag=db.boss,limit=1] run function desert_ball:skills/hide
execute if score #skill db.skill matches 2 if score #cast db.cast matches 14 run function desert_ball:skills/ambush_warn
execute if score #skill db.skill matches 4 if score #cast db.cast matches 24 run function desert_ball:skills/curve_left
execute if score #skill db.skill matches 4 if score #cast db.cast matches 12 run function desert_ball:skills/curve_right
execute if score #skill db.skill matches 1 if score #cast db.cast matches 12 run function desert_ball:skills/shoot
execute if score #skill db.skill matches 5 if score #cast db.cast matches 10 run function desert_ball:skills/launch_header
execute if score #skill db.skill matches 6 if score #cast db.cast matches 14 run function desert_ball:skills/launch_overhead
execute if score #cast db.cast matches 0 run function desert_ball:skills/resolve
