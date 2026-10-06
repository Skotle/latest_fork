function dungeons_arise:boss/ceryneian_hind/site
execute as @e[type=minecraft:marker,tag=ida.site.ceryneian_hind,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/ceryneian_hind
