#Set the player's spawn upon entering the Nether or Overworld.
advancement revoke @s only explorers_eve:dimension_spawn
spawnpoint @s ~ ~ ~
execute if block ~ ~ ~1 air unless block ~ ~-1 ~1 twilightforest:twilight_portal run spawnpoint @s ~ ~ ~1 ~
execute if block ~1 ~ ~ air unless block ~1 ~-1 ~ twilightforest:twilight_portal run spawnpoint @s ~1 ~ ~ ~
tellraw @s {"text":"리스폰 지점이 포털로 설정됨"}