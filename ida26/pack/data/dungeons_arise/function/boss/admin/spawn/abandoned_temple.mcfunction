function dungeons_arise:boss/abandoned_temple/site
execute as @e[type=minecraft:marker,tag=ida.site.abandoned_temple,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/abandoned_temple
