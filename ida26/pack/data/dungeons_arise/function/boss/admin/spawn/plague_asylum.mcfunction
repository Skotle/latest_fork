function dungeons_arise:boss/plague_asylum/site
execute as @e[type=minecraft:marker,tag=ida.site.plague_asylum,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/plague_asylum
