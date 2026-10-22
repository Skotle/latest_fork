#Give a hint if the player can't figure out what to do.
scoreboard players add @s HintTime 1
execute if score @s HintTime matches 800.. run title @a[distance=..25] actionbar {"text":"태양의 정령에 얼음 결정을 반사시켜 손상을 입히세요!","color":"light_purple"}

#Also melt snow in case the player was silly before the fight started.
fill ~3 ~-1 ~3 ~-3 ~ ~-3 air replace snow