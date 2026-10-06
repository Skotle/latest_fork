function dungeons_arise:boss/aviary/site
execute as @e[type=minecraft:marker,tag=ida.site.aviary,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/aviary
