advancement revoke @s only frost_warden:internal/explosive
execute if score #state fw.state matches 1 if entity @s[tag=fw.active] at @s run function frost_warden:hit_impact
