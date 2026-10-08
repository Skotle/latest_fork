advancement revoke @s only eclipse_nox:internal/hurt
execute if score #state nx.state matches 1 if entity @s[tag=nox.member] run scoreboard players set @s nx.clean 0
