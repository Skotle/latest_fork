attribute @a[tag=probe.player,limit=1] minecraft:knockback_resistance base set 1
summon minecraft:zombie 150 81 0 {Tags:["probe.attacker"],NoAI:1b,PersistenceRequired:1b,equipment:{head:{id:"minecraft:iron_helmet",count:1,components:{"minecraft:unbreakable":{}}}}}
tag @a[tag=probe.player] add probe.armor_sample
tag @a[tag=probe.player] add probe.shield
tag @a[tag=probe.player] add probe.heal
item replace entity @a[tag=probe.player,limit=1] armor.head with minecraft:leather_helmet
