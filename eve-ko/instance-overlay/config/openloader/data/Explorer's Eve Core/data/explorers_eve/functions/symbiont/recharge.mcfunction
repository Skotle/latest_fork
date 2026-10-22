#The Symbiont will return to Stage 0 (basic attacks) after a while. Then, reset the scoreboard.
scoreboard players remove @s RechargeTime 1
execute if entity @s[scores={RechargeTime=..300}] positioned ~ ~2 ~ run particle dust 1 0 0 1 ~ ~ ~ 0.5 1 0.5 0 2
execute if entity @w[tag=BombReady,distance=..500] run title @a[distance=..64] actionbar {"text":"위더 공생체를 뒤에서 공격해 상처를 입힌다!","color":"light_purple"}
execute if score @s RechargeTime matches 0 run data modify entity @s Stage set value 0
execute if score @s RechargeTime matches -1 run function explorers_eve:symbiont/recharge_reset

#Also, glowing.
effect give @s minecraft:glowing 1 0 true