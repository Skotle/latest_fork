function dungeons_arise:boss/thornborn_towers/site
execute as @e[type=minecraft:marker,tag=ida.site.thornborn_towers,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/thornborn_towers
