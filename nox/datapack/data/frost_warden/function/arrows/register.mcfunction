scoreboard players add #serial fw.id 1
scoreboard players operation @e[tag=fw.new] fw.id = #serial fw.id
scoreboard players set @e[tag=fw.new] fw.age 160
execute if score #explosive fw.tmp matches 1 run tag @e[tag=fw.new] add fw.explosive
execute if score #explosive fw.tmp matches 1 at @e[tag=fw.new,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["fw.owned","fw.tracker","fw.newtrack"]}
execute if score #explosive fw.tmp matches 1 run scoreboard players operation @e[tag=fw.newtrack] fw.id = #serial fw.id
scoreboard players set @e[tag=fw.newtrack] fw.age 160
tag @e[tag=fw.newtrack] remove fw.newtrack
tag @e[tag=fw.new] remove fw.new
