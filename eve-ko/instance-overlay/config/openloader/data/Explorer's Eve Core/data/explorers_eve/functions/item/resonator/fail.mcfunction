#Cancel the summoning and say why.
execute if score @s Math matches 0 run tellraw @s [{"text":"이 메시지는 나타나지 않아야 합니다. 만약 그렇다면 두렵습니다.","color":"light_purple"}]
execute if score @s Math matches 1 run tellraw @s [{"text":"아주 가까이에 이미 포털이 있습니다!","color":"light_purple"}]

#And give back that item!
playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 0.75 1
execute unless entity @s[gamemode=creative] if score @s BrightResonatorUsed matches 1.. run give @s cataclysm:monstrous_eye{display:{Lore:['{"text":"오버월드와 에버브라이트 사이의 단방향 포털을 여는 데 사용됩니다. 이 포털은 플레이어만 순간이동할 수 있습니다! 보관의 부적을 사용하지 않은 경우 장착된 액세서리 및 복합 블록 부품을 제외한 인벤토리는 남게 됩니다!","color":"gray","italic":false}']}}
execute unless entity @s[gamemode=creative] if score @s DawnResonatorUsed matches 1.. run give @s cataclysm:flame_eye{display:{Lore:['{"text":"오버월드와 Everdawn 사이의 단방향 포털을 여는 데 사용됩니다. 이 포털은 플레이어만 순간이동할 수 있습니다! 보관의 부적을 사용하지 않은 경우 장착된 액세서리 및 복합 블록 부품을 제외한 인벤토리는 남게 됩니다!","color":"gray","italic":false}']}}