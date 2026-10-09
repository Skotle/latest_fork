give @s minecraft:bow[minecraft:custom_name={text:"파수꾼의 서리 활",color:"aqua"},minecraft:enchantments={"minecraft:power":4,"minecraft:unbreaking":3}]
give @s minecraft:emerald 12
give @s minecraft:arrow 32
advancement grant @s only frost_warden:victory
execute if score #time fw.time matches ..3600 run advancement grant @s only frost_warden:speed
execute if score @s fw.hits matches 0 run advancement grant @s only frost_warden:untouched
execute if score @s fw.shield matches 0 run advancement grant @s only frost_warden:no_shield
execute if score #adds fw.adds matches 0 run advancement grant @s only frost_warden:no_adds
