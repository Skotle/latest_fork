#Tell the player what went wrong.
execute if score @s Math matches 0 run tellraw @s [{"text":"이 메시지는 나타나지 않아야 합니다. 만약 그렇다면 두렵습니다.","color":"light_purple"}]
execute if score @s Math matches 1 run tellraw @s [{"text":"이 차원에는 찾을 패널이 없습니다!","color":"light_purple"}]
execute if score @s Math matches 2 run tellraw @s [{"text":"이 차원에는 찾을 패널이 없습니다...하지만 뭔가 다른 것이 있을까요?","color":"light_purple"}]
execute if score @s Math matches 3 run tellraw @s [{"text":"이 핵심노드는 여기에 아무런 영향을 미치지 않습니다.","color":"light_purple"}]

#Also make fun effects. Return the dust on this one.
playsound minecraft:block.lava.extinguish player @a ~ ~ ~ 1 0.75
particle dust 1 0 1 1 ~ ~1.25 ~ 0.3 0.7 0.3 10 100
particle dust 1 0 1 1 ~ ~0.25 ~ 1 0.25 1 10 100
fill ~1 ~ ~1 ~-1 ~ ~-1 air destroy