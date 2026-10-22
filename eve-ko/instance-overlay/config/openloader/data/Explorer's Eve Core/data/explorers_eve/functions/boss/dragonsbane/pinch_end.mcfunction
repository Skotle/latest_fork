#This is the only way to drop the player. No Adventure mode here! Sorry!
execute store result score @s Math run gamerule sendCommandFeedback
execute if score @s Math matches 1 run gamerule sendCommandFeedback false
gamemode spectator @p[tag=DragonsbanePinched,distance=..4]
gamemode survival @p[tag=DragonsbanePinched,distance=..4]
effect give @p[tag=DragonsbanePinched,distance=..4] resistance 1 2 true
title @p[tag=DragonsbanePinched,distance=..8] actionbar {"text":"핀치를 사용하여 피해를 막으려면 방패를 사용하세요!","color":"light_purple"}
tag @p[tag=DragonsbanePinched,distance=..4] remove DragonsbanePinched
scoreboard players reset @s DragonsbanePinchTime
execute if score @s Math matches 1 run gamerule sendCommandFeedback true

#Begin a brief timer to track if it's being too aggressive.
scoreboard players set @s DragonsbaneComboDelay 50

#If it's not burrowing away, it jumps so the player has a chance to get away.
execute if entity @s[tag=!DragonsbaneEscaping,tag=!DragonsbaneDigging] run function explorers_eve:boss/dragonsbane/lunge_random