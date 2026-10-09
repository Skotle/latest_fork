effect clear @s minecraft:slowness
execute if entity @s[tag=fw.stunned] run effect clear @s minecraft:blindness
tag @s remove fw.bound
tag @s remove fw.stunned
scoreboard players set @s fw.stun 0
