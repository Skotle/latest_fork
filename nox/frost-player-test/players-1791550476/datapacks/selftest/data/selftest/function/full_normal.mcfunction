execute store result storage selftest:results full_base_after int 1 run data get entity @a[tag=probe.player,limit=1] Health 1000
item replace entity @a[tag=probe.player,limit=1] armor.head with minecraft:leather_helmet[minecraft:enchantments={"minecraft:projectile_protection":4}]
item replace entity @a[tag=probe.player,limit=1] armor.chest with minecraft:leather_chestplate[minecraft:enchantments={"minecraft:projectile_protection":4}]
item replace entity @a[tag=probe.player,limit=1] armor.legs with minecraft:leather_leggings[minecraft:enchantments={"minecraft:projectile_protection":4}]
item replace entity @a[tag=probe.player,limit=1] armor.feet with minecraft:leather_boots[minecraft:enchantments={"minecraft:projectile_protection":4}]
execute store result storage selftest:results full_normal_before int 1 run data get entity @a[tag=probe.player,limit=1] Health 1000
damage @a[tag=probe.player,limit=1] 100 minecraft:arrow by @e[tag=probe.attacker,limit=1]
