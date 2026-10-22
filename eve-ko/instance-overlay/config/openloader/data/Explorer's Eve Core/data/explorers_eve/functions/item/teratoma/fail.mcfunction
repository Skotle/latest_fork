#Cancel the summoning and say why.
execute if score @s Math matches 0 run tellraw @s [{"text":"이 메시지는 나타나지 않아야 합니다. 만약 그렇다면 두렵습니다.","color":"light_purple"}]
execute if score @s Math matches 1 run tellraw @s [{"text":"현재 위더 공생체가 생성 중입니다!","color":"light_purple"}]
execute if score @s Math matches 2 run tellraw @s [{"text":"위더 공생체가 이미 생성되었습니다!","color":"light_purple"}]
execute if score @s Math matches 3 run tellraw @s [{"text":"더 가까이 다가가면 위더 공생체를 소환할 수 있고, 더 멀리 다가가면 추격전을 벌일 수 있습니다!","color":"light_purple"}]
execute if score @s Math matches 4 run tellraw @s [{"text":"이 위더 스톰은 아직 위더 공생체를 소환할 만큼 진화하지 않았습니다! 슈퍼 TNT를 사용하세요!","color":"light_purple"}]
execute if score @s Math matches 5 run tellraw @s [{"text":"이 위더 스톰은 아직 다른 위더 공생체를 감염시킬 시간이 충분하지 않았습니다!","color":"light_purple"}]
execute if score @s Math matches 6 run tellraw @s [{"text":"포미디밤에 정신이 팔린 위더 스톰!","color":"light_purple"}]
execute if score @s Math matches 7 run tellraw @s [{"text":"좋은 시도였습니다. 여기서는 작동하지 않습니다.","color":"light_purple"}]
execute if score @s Math matches 8 run tellraw @s [{"text":"이 위더 스톰은 너무 아파서 아무것도 할 수 없어요!","color":"light_purple"}]
execute if score @s Math matches 9 run tellraw @s [{"text":"이 차원에는 위더스톰이 없어요!","color":"light_purple"}]
execute if score @s Math matches 10 run tellraw @s [{"text":"이 위더 스톰은 진화하느라 너무 바빠서 당신을 신경쓰지 못합니다!","color":"light_purple"}]

playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 0.75 1
execute unless entity @s[gamemode=creative] run give @s cataclysm:void_eye{display:{Lore:['{"text":"위더 스톰을 자극하는 데 사용합니다. 멀리 떨어져 있으면 가장 가까운 플레이어를 쫓기 시작합니다. 근처에 있으면 위더 공생체를 소환하려고 시도합니다.","color":"gray","italic":false}']}}