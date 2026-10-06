function dungeons_arise:boss/heavenly_conqueror/site
execute as @e[type=minecraft:marker,tag=ida.site.heavenly_conqueror,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/heavenly_conqueror
