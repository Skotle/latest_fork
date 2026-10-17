execute store result score #material inf.sys run random value 1..100
execute store result score #enchant inf.sys run random value 1..100
execute if score #material inf.sys matches 1..50 run function infernal:piece/harder_feet_leather
execute if score #material inf.sys matches 51..100 run function infernal:piece/harder_feet_chainmail
