#All nearby players get unbreakable armor.
item modify entity @a[gamemode=!spectator,distance=..256] armor.head explorers_eve:unbreakable
item modify entity @a[gamemode=!spectator,distance=..256] armor.chest explorers_eve:unbreakable
item modify entity @a[gamemode=!spectator,distance=..256] armor.legs explorers_eve:unbreakable
item modify entity @a[gamemode=!spectator,distance=..256] armor.feet explorers_eve:unbreakable

#Effects!
playsound minecraft:block.enchantment_table.use hostile @a[distance=..256] ~ ~ ~ 4 1.4 1
playsound minecraft:entity.zombie_villager.converted hostile @a[distance=..256] ~ ~ ~ 4 1.7 1
playsound minecraft:block.end_portal.spawn hostile @a[distance=..256] ~ ~ ~ 4 2 1

execute at @a[gamemode=!spectator,distance=..256] run particle blue_skies:star_flare 1 0 1 ~ ~1 ~ 0.25 0.35 0.25 0.03 20
execute at @a[gamemode=!spectator,distance=..256] positioned ~ ~0.3 ~ run function explorers_eve:item/purple_particle_ring
execute at @a[gamemode=!spectator,distance=..256] positioned ~ ~1.5 ~ run function explorers_eve:item/purple_particle_ring

tellraw @a[gamemode=!spectator,distance=..256] {"text":"갑옷이 강화되었습니다!","color":"light_purple"}

kill @s

#Spawn many particles.
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 1 0 0 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -1 0 0 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0 0 1 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0 0 -1 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.7 0 0.7 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.7 0 0.7 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.7 0 -0.7 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.7 0 -0.7 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.383 0 0.924 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.383 0 0.924 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.383 0 -0.924 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.383 0 -0.924 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.924 0 0.383 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.924 0 0.383 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.924 0 -0.383 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.924 0 -0.383 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.195 0 0.981 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.195 0 0.981 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.195 0 -0.981 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.195 0 -0.981 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.981 0 0.195 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.981 0 0.195 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.981 0 -0.195 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.981 0 -0.195 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.556 0 0.831 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.556 0 0.831 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.556 0 -0.831 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.556 0 -0.831 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.831 0 0.556 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.831 0 0.556 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.831 0 -0.556 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.831 0 -0.556 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.098 0 0.995 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.098 0 0.995 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.098 0 -0.995 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.098 0 -0.995 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.995 0 0.098 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.995 0 0.098 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.995 0 -0.098 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.995 0 -0.098 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.29 0 0.957 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.29 0 0.957 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.29 0 -0.957 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.29 0 -0.957 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.957 0 0.29 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.957 0 0.29 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.957 0 -0.29 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.957 0 -0.29 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.471 0 0.882 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.471 0 0.882 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.471 0 -0.882 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.471 0 -0.882 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.882 0 0.471 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.882 0 0.471 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.882 0 -0.471 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.882 0 -0.471 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.634 0 0.773 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.634 0 0.773 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.634 0 -0.773 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.634 0 -0.773 0.75 0 force

particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.773 0 0.634 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.773 0 0.634 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ 0.773 0 -0.634 0.75 0 force
particle blue_skies:star_flare 1 0 1 ~ ~3.25 ~ -0.773 0 -0.634 0.75 0 force