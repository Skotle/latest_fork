#Give a hint if the player can't figure out what to do.
scoreboard players remove @s HintTime 1
execute if score @s HintTime matches 1..400 run title @a[distance=..32] actionbar {"text":"공기고래 왕이 어디에 있는지 잘 들어보세요!","color":"light_purple"}