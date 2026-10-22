#It's a lot harder to reset a spawn point from a bed.
advancement revoke @s only explorers_eve:use_bed
execute unless dimension minecraft:the_nether unless dimension minecraft:the_end unless dimension explorers_eve:glitch run spawnpoint @s ~ ~ ~
execute unless block ~ ~ ~ #explorers_eve:respawn_secure run tellraw @s {"text":"귀하의 스폰 지점이 차단되었을 수 있습니다! 빈 공간에 있는지 확인하세요."}