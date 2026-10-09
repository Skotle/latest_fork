scoreboard players remove #cast fw.cast 1
execute if score #cast fw.cast matches 17.. at @e[tag=fw.boss,limit=1] run particle minecraft:snowflake ~ ~1.5 ~ .2 .2 .2 0 4 force @a[tag=fw.active]
execute if score #skill fw.skill matches 1 if score #cast fw.cast matches 16 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ rotated as @e[tag=fw.boss,limit=1] run function frost_warden:skills/fan
execute if score #skill fw.skill matches 2 if score #cast fw.cast matches 18 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes run function frost_warden:ashe/focus_shot
execute if score #skill fw.skill matches 2 if score #cast fw.cast matches 15 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes run function frost_warden:ashe/focus_shot
execute if score #skill fw.skill matches 2 if score #cast fw.cast matches 12 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes run function frost_warden:ashe/focus_shot
execute if score #skill fw.skill matches 2 if score #cast fw.cast matches 9 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes run function frost_warden:ashe/focus_shot
execute if score #skill fw.skill matches 2 if score #cast fw.cast matches 6 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes run function frost_warden:ashe/focus_shot
execute if score #skill fw.skill matches 4 if score #cast fw.cast matches 17.. at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @e[tag=fw.aim,limit=1] feet run function frost_warden:ashe/ultimate_line
execute if score #skill fw.skill matches 4 if score #cast fw.cast matches 16 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @e[tag=fw.aim,limit=1] feet run function frost_warden:arrows/stun
execute if score #skill fw.skill matches 5 if score #cast fw.cast matches 17.. at @e[tag=fw.wall_live] run particle minecraft:soul_fire_flame ~ ~ ~ .08 .15 .08 0 2 force @a[tag=fw.active]
execute if score #skill fw.skill matches 5 if score #cast fw.cast matches 16 run function frost_warden:walls/wave_one
execute if score #skill fw.skill matches 6 if score #cast fw.cast matches 16 at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ facing entity @e[tag=fw.aim,limit=1] feet run function frost_warden:ashe/basic
execute if score #cast fw.cast matches 0 run function frost_warden:skills/recover
