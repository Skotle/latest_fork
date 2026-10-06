function dungeons_arise:boss/foundry/site
execute as @e[type=minecraft:marker,tag=ida.site.foundry,distance=..1] if score @s ida.sid = #next ida.sid at @s run function dungeons_arise:boss/admin/start/foundry
