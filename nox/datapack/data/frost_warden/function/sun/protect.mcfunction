execute unless entity @s[tag=fw.sunproof] run data merge entity @s {Fire:-1s}
execute unless items entity @s armor.head minecraft:iron_helmet[minecraft:unbreakable] run item replace entity @s armor.head with minecraft:iron_helmet[minecraft:unbreakable={}]
execute if entity @s[tag=fw.boss] unless items entity @s armor.head minecraft:iron_helmet[minecraft:enchantments~[{enchantments:"frost_warden:own_arrow_guard",levels:{min:1}}]] run item replace entity @s armor.head with minecraft:iron_helmet[minecraft:unbreakable={},minecraft:enchantments={"frost_warden:own_arrow_guard":1}]
tag @s add fw.sunproof
