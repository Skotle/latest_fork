advancement revoke @s only eclipse_nox:internal/counter_hit
execute if score #state nx.state matches 1 if score #counter nx.move matches 1 if score #safe nx.safe matches 1.. if entity @s[tag=nox.active] run function eclipse_nox:challenge/counter_credit
