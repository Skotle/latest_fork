kill @e[tag=fw.hawk]
execute at @e[tag=fw.boss,limit=1] run summon minecraft:marker ~ ~3 ~ {Tags:["fw.owned","fw.hawk"]}
scoreboard players set @e[tag=fw.hawk] fw.age 30
