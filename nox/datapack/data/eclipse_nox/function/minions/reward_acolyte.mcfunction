advancement revoke @s only eclipse_nox:minions/kill_acolyte
execute if score #state nx.state matches 1 if entity @s[tag=nox.active] at @s run function eclipse_nox:minions/boon_acolyte
