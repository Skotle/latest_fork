kill @e[tag=fw.aim]
execute at @a[tag=fw.active,gamemode=!creative,sort=random,limit=1] run summon minecraft:marker ~ ~1 ~ {Tags:["fw.owned","fw.aim"]}
