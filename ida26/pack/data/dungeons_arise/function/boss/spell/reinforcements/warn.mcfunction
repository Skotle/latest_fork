function dungeons_arise:boss/core/target with entity @s data
tellraw @a[predicate=dungeons_arise:boss/eligible,distance=..32] {"text":"⚠ 증원 호출 — 표식에서 벗어나세요!","color":"yellow"}
playsound minecraft:block.note_block.bell hostile @a[distance=..32] ~ ~ ~ 0.6 0.8
function dungeons_arise:boss/spell/reinforcements/telegraph with entity @s data
