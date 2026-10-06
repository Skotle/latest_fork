function dungeons_arise:boss/typhon/site
execute as @e[type=minecraft:marker,tag=ida.site.typhon,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/typhon
