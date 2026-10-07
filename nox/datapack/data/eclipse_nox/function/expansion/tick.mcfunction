function eclipse_nox:minions/tick
execute if score #phase nx.phase matches 3 run scoreboard players remove #doom nx.doom 1
execute if score #judgement nx.doom matches 1.. run function eclipse_nox:judgement/tick
execute if score #phase nx.phase matches 3 if score #doom nx.doom matches ..0 if score #judgement nx.doom matches 0 if score #cast nx.cast matches 0 if score #dash nx.dash matches 0 if score #puzzle nx.puzzle matches 0 if score #safe nx.safe matches 0 run function eclipse_nox:judgement/begin
