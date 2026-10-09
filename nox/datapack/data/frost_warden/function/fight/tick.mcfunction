tag @a remove fw.active
execute as @a[tag=fw.member,distance=..25,gamemode=!spectator] if score @s nx.death = @s fw.olddeath if score @s nx.leave = @s fw.oldleave run tag @s add fw.active
execute if entity @a[tag=fw.active,gamemode=!creative] run scoreboard players set #idle fw.tmp 0
execute unless entity @a[tag=fw.active,gamemode=!creative] run scoreboard players add #idle fw.tmp 1
execute if score #idle fw.tmp matches 200.. run function frost_warden:abort
execute if score #state fw.state matches 1 unless entity @e[tag=fw.boss] run function frost_warden:victory
execute if score #state fw.state matches 1 if entity @e[tag=fw.boss] run function frost_warden:fight/alive
execute as @a[tag=fw.bound,tag=!fw.active] run function frost_warden:debuff/clear
execute as @a[tag=fw.stunned,tag=!fw.active] run function frost_warden:debuff/clear
execute as @a[tag=fw.revealed,tag=!fw.active] run effect clear @s minecraft:glowing
tag @a[tag=!fw.active] remove fw.revealed
