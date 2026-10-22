#Fire a big ball of doom!
tag @s add ZetaUsed
summon dungeons_plus:soul_fireball ~ ~1.5 ~ {Tags:["ZetaShot","NewZetaShot"],fuse:40,power:2b,knockback:1,CustomName:'{"text":"제타 차지"}'}
execute if predicate explorers_eve:empowered run data merge entity @e[tag=ZetaShot,limit=1,sort=nearest] {knockback:2,has_flame:1b}
execute if score @s ZetaCharges matches 5.. run data merge entity @e[tag=NewZetaShot,limit=1,sort=nearest] {power:3b,knockback:3,has_flame:1b}
execute if predicate explorers_eve:structure/blue_skies_dungeon run data modify entity @e[tag=NewZetaShot,limit=1,sort=nearest] has_flame set value 0b
execute as @e[tag=NewZetaShot,limit=1,sort=nearest] at @s run function explorers_eve:item/prototype_zeta/aim
execute if predicate explorers_eve:empowered run tag @e[tag=ZetaShotTracker,limit=1,sort=nearest] add Empowered
tag @s remove ZetaUsed

#Now to set up the cooldown and effect stuff.
execute if score @s ZetaCharges matches 5.. run scoreboard players set @s ZetaCharges 0
execute if score @s ZetaCharges matches 1.. run scoreboard players remove @s ZetaCharges 1
execute unless score @s ZetaCharges matches 0 run tag @s add ZetaCooldown
execute unless score @s ZetaCharges matches 0 run scoreboard players set @s ZetaCooldown 60
playsound minecraft:entity.generic.explode player @s ~ ~ ~ 1 2 1
