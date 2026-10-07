scoreboard players set #dash nx.dash 0
scoreboard players set #safe nx.safe 0
scoreboard players set #expose nx.expose 0
scoreboard players set #phase nx.phase 2
scoreboard players set #puzzle nx.puzzle 1
scoreboard players set #cast nx.cast 0
kill @e[tag=nox.target]
bossbar set eclipse_nox:health name {"text":"녹스 · 봉인종의 공명","color":"gold"}
scoreboard players set #step nx.step 0
scoreboard players set #last nx.last 0
scoreboard players set #puzzletime nx.tmp 0
data merge entity @e[tag=nox.boss,limit=1] {Invulnerable:1b}
tellraw @a[tag=nox.member] {"text": "두 번째 종 — 봉인종을 우클릭: 북쪽 1 → 동쪽 3 → 서쪽 2. 같은 종을 연속 울리면 과부하!", "color": "gold"}
playsound eclipse_nox:bell_high master @a[tag=nox.member] ~ ~ ~ 1 .8
