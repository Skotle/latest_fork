#Cancel the summoning and say why.
execute if score @s Math matches 0 run tellraw @p[gamemode=!spectator,distance=..32] [{"text":"이 메시지는 나타나지 않아야 합니다. 만약 그렇다면 두렵습니다.","color":"light_purple"}]
execute if score @s Math matches 1 run tellraw @p[gamemode=!spectator,distance=..32] [{"text":"이름없는 마법사가 이미 생성되었습니다!","color":"light_purple"}]
execute if score @s Math matches 2 run tellraw @p[gamemode=!spectator,distance=..32] [{"text":"이름 없는 마법사는 이 차원에서 싸울 수 없습니다!","color":"light_purple"}]
execute if score @s Math matches 3 run tellraw @p[gamemode=!spectator,distance=..32] [{"text":"이름 없는 마법사는 표면에서만 싸울 수 있습니다!","color":"light_purple"}]
execute if score @s Math matches 4 run tellraw @p[gamemode=!spectator,distance=..32] [{"text":"이 생물 군계는 적절한 전투를 하기에는 너무 물이 많습니다! 다른 곳으로 가세요!","color":"light_purple"}]

#Use scoreboards to prevent instant vexes!
scoreboard players set @s SorcererVexTime 1000
scoreboard players set @s SorcererTeleportTime 300

#Effects!
particle blue_skies:star_flare 1 0 1 ~ ~1 ~ 0.25 0.5 0.25 0.1 100

#And give back those expensive items!
execute if entity @s[tag=SorcererEthereal] run loot spawn ~ ~1 ~ loot explorers_eve:sorcerer_recipe_ethereal
execute if entity @s[tag=SorcererDusk] run loot spawn ~ ~1 ~ loot explorers_eve:sorcerer_recipe_dusk
execute positioned ~ ~1 ~ as @e[type=item,distance=..0.1] run data merge entity @s {Glowing:1b,Invulnerable:1b,Health:10000,Age:-32768,PickupDelay:0}

#Then instant despawn!
tp @s ~ -1000 ~
kill @s