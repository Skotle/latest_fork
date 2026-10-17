execute store result score #roll inf.sys run random value 1..100
execute if score #roll inf.sys matches ..20 run function infernal:armor/insane
execute store result score #roll inf.sys run random value 1..100
execute if entity @s[type=#infernal:zombie] if score #roll inf.sys matches ..10 unless data entity @s equipment.mainhand.id run function infernal:weapon/insane
execute store result score #roll inf.sys run random value 1..100
execute if entity @s[type=#infernal:archer] if score #roll inf.sys matches ..10 if data entity @s equipment.mainhand{id:"minecraft:bow"} unless data entity @s equipment.mainhand.components."minecraft:enchantments" run function infernal:bow/insane
