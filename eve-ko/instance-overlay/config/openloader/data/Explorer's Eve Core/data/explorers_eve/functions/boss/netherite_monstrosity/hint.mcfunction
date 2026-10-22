#Give a hint if the player can't figure out what to do.
scoreboard players add @s HintTime 1
execute if score @s HintTime matches 140..340 run title @a[distance=..24,advancements={cataclysm:kill_monstrosity=false}] actionbar {"text":"방패를 사용하여 네더라이트 괴물의 근접 공격을 막아보세요!","color":"light_purple"}