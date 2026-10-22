#Give a hint if the player can't figure out what to do.
scoreboard players add @s HintTime 1
execute if score @s HintTime matches 30.. run title @a[distance=..32,advancements={twilightforest:progress_naga=false}] actionbar {"text":"방패를 사용해 나가의 돌격을 막아보세요!","color":"light_purple"}