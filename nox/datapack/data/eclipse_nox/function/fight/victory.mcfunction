scoreboard players set #state nx.state 0
tellraw @a[tag=nox.member] {"text": "일식이 걷혔다. 녹스의 심장을 획득했습니다.", "color": "gold"}
execute as @a[tag=nox.member] if score @s nx.death = @s nx.olddeath if score @s nx.leave = @s nx.oldleave run function eclipse_nox:reward
playsound eclipse_nox:victory master @a[tag=nox.member] ~ ~ ~ 1 1
function eclipse_nox:fight/cleanup
