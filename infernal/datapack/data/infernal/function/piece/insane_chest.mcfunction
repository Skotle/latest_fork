execute store result score #material inf.sys run random value 1..100
execute store result score #enchant inf.sys run random value 1..100
execute if score #material inf.sys matches 1..75 run function infernal:piece/insane_chest_chainmail
execute if score #material inf.sys matches 76..100 run function infernal:piece/insane_chest_iron
execute if score #enchant inf.sys matches ..40 run function infernal:piece/insane_chest_ench
