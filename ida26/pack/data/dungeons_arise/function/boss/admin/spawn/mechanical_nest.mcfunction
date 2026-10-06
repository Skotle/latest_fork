function dungeons_arise:boss/mechanical_nest/site
execute as @e[type=minecraft:marker,tag=ida.site.mechanical_nest,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/mechanical_nest
