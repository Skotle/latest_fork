#Tag to signal that this corpse is in the End.
tag @s add EndCorpse

#Keep shuffling the corpse until it's on solid ground.
tellraw @a[scores={Deaths=1..}] [{"text":"공허의 힘으로 당신의 시체가 중앙 엔드 섬 어딘가로 이동합니다...","color":"gray"}]
function explorers_eve:world/end_corpse_move