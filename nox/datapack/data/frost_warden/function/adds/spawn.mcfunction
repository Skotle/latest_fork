execute store result score #count fw.tmp run execute if entity @e[tag=fw.add]
execute if score #count fw.tmp matches ..1 positioned ~8 ~ ~8 run summon minecraft:stray ~ ~ ~ {Tags:["fw.owned","fw.add"],PersistenceRequired:1b,Health:50f,attributes:[{id:"minecraft:max_health",base:50}],CanPickUpLoot:0b,equipment:{mainhand:{id:"minecraft:bow",count:1},head:{id:"minecraft:iron_helmet",count:1,components:{"minecraft:unbreakable":{}}}},drop_chances:{head:0.0f}}
team join fw.enemies @e[tag=fw.add]
