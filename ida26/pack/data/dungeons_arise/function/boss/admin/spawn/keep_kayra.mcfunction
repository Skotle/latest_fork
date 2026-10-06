function dungeons_arise:boss/keep_kayra/site
execute as @e[type=minecraft:marker,tag=ida.site.keep_kayra,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/keep_kayra
