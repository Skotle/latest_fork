scoreboard players operation #previous_skill nx.skill = #skill nx.skill
scoreboard players add #cycle nx.combo 1
execute if score #cycle nx.combo matches 6.. run scoreboard players set #cycle nx.combo 1
scoreboard players operation #skill nx.skill = #cycle nx.combo
execute if score #cycle nx.combo matches 3 run scoreboard players set #skill nx.skill 5
execute if score #cycle nx.combo matches 4 run scoreboard players set #skill nx.skill 3
execute if score #cycle nx.combo matches 5 run scoreboard players set #skill nx.skill 1
execute if score #cycle nx.combo matches 5 if score #phase nx.phase matches 3 run scoreboard players set #skill nx.skill 4
execute at @e[tag=nox.boss,limit=1] unless entity @a[tag=nox.active,distance=..9] unless score #previous_skill nx.skill matches 5 run scoreboard players set #skill nx.skill 5
scoreboard players set #chain nx.combo 0
scoreboard players set #cast nx.cast 16
scoreboard players set #safe nx.safe 0
scoreboard players set #expose nx.expose 0
kill @e[tag=nox.target]
function eclipse_nox:skills/aim
execute if score #skill nx.skill matches 1 run tellraw @a[tag=nox.member] {"text": "종 2연격 — 정면을 피해라. 두 번째 공격이 이어진다!", "color": "gold"}
execute if score #skill nx.skill matches 2 run scoreboard players set #cast nx.cast 16
execute if score #phase nx.phase matches 3 if score #skill nx.skill matches 2 run scoreboard players set #cast nx.cast 72
execute if score #skill nx.skill matches 2 run tellraw @a[tag=nox.member] {"text": "확장 충격파 — 불꽃 고리의 안쪽으로 파고드세요!", "color": "gold"}
execute if score #skill nx.skill matches 3 run scoreboard players set #cast nx.cast 16
execute if score #skill nx.skill matches 3 run function eclipse_nox:skills/echo
execute if score #skill nx.skill matches 4 run function eclipse_nox:skills/eclipse_begin
execute if score #skill nx.skill matches 5 run scoreboard players set #cast nx.cast 14
execute if score #skill nx.skill matches 5 run tellraw @a[tag=nox.member] {"text": "시계추 돌진 — 표시된 직선 옆으로 피하세요. 벽 충돌 시 심장이 노출됩니다!", "color": "gold"}
scoreboard players operation #total nx.total = #cast nx.cast
playsound eclipse_nox:warning master @a[tag=nox.member] ~ ~ ~ 1 1
