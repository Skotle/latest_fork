#Make effects.
tag @s add Activated
function explorers_eve:item/purple_particle_ring
playsound witherstormmod:command_block_summon block @a ~ ~ ~ 5 1.5

summon area_effect_cloud ~ ~ ~ {Duration:99999999,Tags:["BeaconUpgradeRing1"],Rotation:[45f,0f]}
summon area_effect_cloud ~ ~ ~ {Duration:99999999,Tags:["BeaconUpgradeRing2"]}

tellraw @a[gamemode=!spectator,distance=..24] {"text":"탐험가의 보물을 메마른 봉화에 배치하여 강화해 보세요.","color":"light_purple"}