scoreboard players set #dash nx.dash 0
scoreboard players set #safe nx.safe 0
scoreboard players set #expose nx.expose 0
scoreboard players set #phase nx.phase 3
scoreboard players set #cast nx.cast 0
kill @e[tag=nox.target]
bossbar set eclipse_nox:health name {"text":"녹스 · 개기일식","color":"light_purple"}
scoreboard players set #next nx.next 20
scoreboard players set #skill nx.skill 3
tellraw @a[tag=nox.member] {"text": "개기일식 — 빛나는 회전 구역을 따라 이동하라. 종 주변은 잠시 안전하다.", "color": "gold"}
playsound eclipse_nox:bell_high master @a[tag=nox.member] ~ ~ ~ 1 .5
scoreboard players set #doom nx.doom 80
tellraw @a[tag=nox.member] {"text": "최후의 심판 — 붉은 예고가 나타나면 중앙 금빛 원(반경 4블록)으로! 밖은 즉사합니다.", "color": "gold"}
