scoreboard players remove @s fw.stun 1
execute if score @s fw.stun matches 1.. run effect give @s minecraft:slowness 1 6 true
execute if score @s fw.stun matches ..0 run function frost_warden:stun/end
