execute store result score #material inf.sys run random value 1..100
execute store result score #enchant inf.sys run random value 1..100
execute if score #material inf.sys matches 1..100 run function infernal:piece/nightmare_chest_iron
execute if score #enchant inf.sys matches ..40 run function infernal:piece/nightmare_chest_ench
execute if score #material inf.sys matches ..5 run function infernal:piece/nightmare_diamond
