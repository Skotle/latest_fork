advancement revoke @s only frost_warden:internal/stun
execute if score #state fw.state matches 1 if entity @s[tag=fw.active,gamemode=!creative] unless score @s fw.guard matches 1.. at @s run function frost_warden:stun/apply
execute at @s as @e[tag=fw.stun_arrow,distance=..3,sort=nearest,limit=1] run function frost_warden:arrows/expire
