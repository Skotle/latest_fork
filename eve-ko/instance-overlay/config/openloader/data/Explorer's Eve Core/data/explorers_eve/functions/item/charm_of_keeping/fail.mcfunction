#Nope.
execute if score @s Math matches 0 run tellraw @s [{"text":"이 메시지는 나타나지 않아야 합니다. 만약 그렇다면 두렵습니다.","color":"light_purple"}]
execute if score @s Math matches 1 run tellraw @s [{"text":"인벤토리가 비어 있지 않으면 부적은 작동하지 않습니다!","color":"light_purple"}]
execute if score @s Math matches 2 run tellraw @s [{"text":"당신은 이 부적을 사용할 적절한 차원이 아닙니다!","color":"light_purple"}]
execute if score @s Math matches 3 run tellraw @s [{"text":"당신은 이미 이 부적을 사용했습니다!","color":"light_purple"}]

playsound minecraft:block.note_block.didgeridoo player @s ~ ~ ~ 20 0.5
#particle minecraft:smoke ~ ~1 ~ 0.3 0.5 0.3 0 15 normal @s