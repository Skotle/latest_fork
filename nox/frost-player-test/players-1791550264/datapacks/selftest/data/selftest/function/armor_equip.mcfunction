summon minecraft:marker 150 81 0 {Tags:["probe.attacker"]}
tag @a[tag=probe.player] add probe.armor_sample
tag @a[tag=probe.player] add probe.shield
tag @a[tag=probe.player] add probe.heal
item replace entity @a[tag=probe.player,limit=1] armor.head with minecraft:leather_helmet
