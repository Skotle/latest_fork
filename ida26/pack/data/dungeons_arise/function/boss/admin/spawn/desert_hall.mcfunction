function dungeons_arise:boss/desert_hall/site
execute as @e[type=minecraft:marker,tag=ida.site.desert_hall,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/desert_hall
