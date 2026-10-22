#Give a hint if the player can't figure out what to do.
scoreboard players add @s HintTime 1
execute if score @s HintTime matches 600.. run title @a[distance=..64] actionbar {"text":"Ghastlings를 처치하고 Ghast Trap을 활성화하여 Ur-Ghast에 피해를 입히세요!","color":"light_purple"}