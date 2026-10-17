execute store result score #roll inf.sys run random value 1..100
execute if score #roll inf.sys matches ..10 run function infernal:armor/harder
execute store result score #roll inf.sys run random value 1..100
execute if entity @s[type=#infernal:zombie] if score #roll inf.sys matches ..5 unless data entity @s equipment.mainhand.id run function infernal:weapon/harder
