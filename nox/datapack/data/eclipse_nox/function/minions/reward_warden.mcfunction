advancement revoke @s only eclipse_nox:minions/kill_warden
execute if score #state nx.state matches 1 if entity @s[tag=nox.active] at @s run function eclipse_nox:minions/boon_warden
execute if score #state nx.state matches 1 if entity @s[tag=nox.member] run scoreboard players set #team_adds nx.warden 1
