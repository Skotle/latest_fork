execute as @e[tag=fw.boss] run function frost_warden:sun/protect
execute as @e[tag=fw.add] run function frost_warden:sun/protect
execute as @e[tag=fw.site_seed] at @s if entity @a[distance=..100] run function frost_warden:site/init
execute as @e[tag=fw.anchor,tag=!fw.ready] at @s run function frost_warden:site/setup
execute if score #state fw.state matches 0 as @e[tag=fw.anchor] at @s unless block ~ ~1 ~ minecraft:target[power=0] if block ~ ~1 ~ minecraft:target run function frost_warden:start
execute if score #state fw.state matches 1 as @e[tag=fw.anchor,tag=fw.current,limit=1] at @s run function frost_warden:fight/tick
execute if score #state fw.state matches 1 unless entity @e[tag=fw.anchor,tag=fw.current] run function frost_warden:abort
execute if score #state fw.state matches 0 as @a[tag=fw.bound] run function frost_warden:debuff/clear
execute if score #state fw.state matches 0 as @a[tag=fw.stunned] run function frost_warden:debuff/clear
execute if score #state fw.state matches 0 as @a[tag=fw.revealed] run effect clear @s minecraft:glowing
execute if score #state fw.state matches 0 run tag @a remove fw.revealed
