#Warn the player about what they just tried to do.
advancement revoke @s only explorers_eve:banned_item
tellraw @s {"text":"이 항목은 Explorer's Eve에서 비활성화됩니다!","color":"red"}
playsound aether:entity.zephyr.shoot player @s ~ ~ ~ 0.4 2
schedule function explorers_eve:world/banned_item_clear 1t