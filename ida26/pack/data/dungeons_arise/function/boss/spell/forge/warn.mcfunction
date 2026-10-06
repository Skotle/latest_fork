function dungeons_arise:boss/core/target with entity @s data
tellraw @a[predicate=dungeons_arise:boss/eligible,distance=..32] {"text":"⚠ 용광로 분출 — 표식에서 벗어나세요!","color":"yellow"}
playsound minecraft:block.note_block.bell hostile @a[distance=..32] ~ ~ ~ 0.6 0.8
function dungeons_arise:boss/spell/forge/telegraph with entity @s data
