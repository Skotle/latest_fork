#Give a hint if the player can't figure out what to do.
scoreboard players add @s HintTime 1
execute if score @s HintTime matches 400.. run title @a[distance=..32] actionbar {"text":"회오리바람이 당신을 멀리 날려버릴 수 없도록 점프하지 마세요!","color":"light_purple"}