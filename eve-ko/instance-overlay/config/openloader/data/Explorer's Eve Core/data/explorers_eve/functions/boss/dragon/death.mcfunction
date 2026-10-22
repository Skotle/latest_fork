#When the dragon dies, dispose of its children and summon the Redstone Heart over the portal.
execute positioned 0 60 0 run function explorers_eve:boss/dragon/heart
tellraw @a[distance=..200] [{"text":"에이","color":"white"},{"text":"레드스톤 하트","color":"red"},{"text":"엔드 포탈 위에 형성되었습니다!","color":"white"}]
execute unless data storage world DragonUnspawned run summon experience_orb ~4 ~4 ~ {Value:3000}
execute unless data storage world DragonUnspawned run summon experience_orb ~-4 ~4 ~ {Value:3000}
execute unless data storage world DragonUnspawned run summon experience_orb ~ ~4 ~4 {Value:3000}
execute unless data storage world DragonUnspawned run summon experience_orb ~ ~4 ~-4 {Value:3000}
data remove storage world DragonUnspawned
kill @e[type=endertrigon:baby_ender_dragon]
kill @s