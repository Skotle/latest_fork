function dungeons_arise:boss/small_blimp/site
execute as @e[type=minecraft:marker,tag=ida.site.small_blimp,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/small_blimp
