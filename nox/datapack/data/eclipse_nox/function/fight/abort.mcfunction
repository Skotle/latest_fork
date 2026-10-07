scoreboard players set #state nx.state 0
tellraw @a[tag=nox.member] {"text": "전투가 중단되었습니다. 소환 장치에서 다시 시작할 수 있습니다.", "color": "gold"}
function eclipse_nox:fight/cleanup
