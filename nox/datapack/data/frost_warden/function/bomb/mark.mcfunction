execute as @a[tag=fw.active,gamemode=!creative] at @s run summon minecraft:marker ~ ~ ~ {Tags:["fw.owned","fw.bomb_mark","fw.newmark"]}
scoreboard players set @e[tag=fw.newmark] fw.age 32
tag @e[tag=fw.newmark] remove fw.newmark
tellraw @a[tag=fw.member] {"text": "머리 위 폭격! 표시된 위치에서 즉시 벗어나세요.", "color": "aqua"}
