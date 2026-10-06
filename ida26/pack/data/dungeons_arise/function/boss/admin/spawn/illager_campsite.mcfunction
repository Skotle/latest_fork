function dungeons_arise:boss/illager_campsite/site
execute as @e[type=minecraft:marker,tag=ida.site.illager_campsite,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/illager_campsite
