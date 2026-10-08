kill @e[tag=db.ambush]
kill @e[tag=db.jump_origin]
execute as @a[tag=db.active,sort=random,limit=1] at @s rotated as @s rotated ~ 0 positioned ^ ^ ^-3 run summon minecraft:marker ~ ~ ~ {Tags:["db.owned","db.ambush"]}
execute at @e[tag=db.ambush,limit=1] run particle minecraft:dust{color:[0.9,0.7,0.35],scale:2.0} ~ ~.1 ~ .6 0 .6 0 22 force @a[tag=db.member]
playsound minecraft:entity.villager.celebrate master @a[tag=db.member] ~ ~ ~ .8 .7
