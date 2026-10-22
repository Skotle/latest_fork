#Some condition wasn't met, so fail to spawn.
execute if score @s Math matches -1 run tellraw @a[distance=..16] [{"text":"이 신호기는 더 높이 올려야 합니다!","color":"light_purple"}]
execute if score @s Math matches -2 run tellraw @a[distance=..16] [{"text":"이 차원의 주변 에너지가 메마른 봉화를 방해합니다...대신 오버월드로 옮겨보세요.","color":"light_purple"}]
execute if score @s Math matches -3 run tellraw @a[distance=..16] [{"text":"이 생물 군계는 적절한 전투를 하기에는 너무 물이 많습니다! 다른 곳으로 가세요!","color":"light_purple"}]

loot spawn ~ ~1 ~ loot explorers_eve:true_final_battle_summon_materials
kill @s