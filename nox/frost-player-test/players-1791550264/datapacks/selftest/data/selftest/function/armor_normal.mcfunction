execute store result storage selftest:results armor_base_after int 1 run data get entity @a[tag=probe.player,limit=1] Health 1000
item replace entity @a[tag=probe.player,limit=1] armor.head with minecraft:leather_helmet[minecraft:enchantments={"minecraft:projectile_protection":4}]
execute store result storage selftest:results pp_normal_before int 1 run data get entity @a[tag=probe.player,limit=1] Health 1000
damage @a[tag=probe.player,limit=1] 100 minecraft:arrow by @e[tag=probe.attacker,limit=1]
