#Depending on what item this is, do it or not.
execute if block ~ ~ ~ witherstormmod:super_beacon{ResummonItems:[{tag:{Empowered:1b}}]} run function explorers_eve:item/empower/repeat

execute unless entity @s[tag=Dupe] if block ~ ~ ~ witherstormmod:super_beacon{ResummonItems:[{tag:{PrototypeZeta:1b}}]} run loot replace block ~ ~ ~ container.0 loot explorers_eve:item/empowered/prototype_zeta
execute unless entity @s[tag=Dupe] if block ~ ~ ~ witherstormmod:super_beacon{ResummonItems:[{tag:{Punisher:1}}]} run loot replace block ~ ~ ~ container.0 loot explorers_eve:item/empowered/punisher
execute unless entity @s[tag=Dupe] if block ~ ~ ~ witherstormmod:super_beacon{ResummonItems:[{id:"aether:cloud_staff"}]} run loot replace block ~ ~ ~ container.0 loot explorers_eve:item/empowered/cloud_staff
execute unless entity @s[tag=Dupe] if block ~ ~ ~ witherstormmod:super_beacon{ResummonItems:[{id:"twilightforest:lamp_of_cinders"}]} run loot replace block ~ ~ ~ container.0 loot explorers_eve:item/empowered/lamp_of_cinders
execute unless entity @s[tag=Dupe] if block ~ ~ ~ witherstormmod:super_beacon{ResummonItems:[{id:"twilightforest:fortification_scepter"}]} run loot replace block ~ ~ ~ container.0 loot explorers_eve:item/empowered/lich_scepter
execute unless entity @s[tag=Dupe] if block ~ ~ ~ witherstormmod:super_beacon{ResummonItems:[{id:"twilightforest:lifedrain_scepter"}]} run loot replace block ~ ~ ~ container.0 loot explorers_eve:item/empowered/lich_scepter
execute unless entity @s[tag=Dupe] if block ~ ~ ~ witherstormmod:super_beacon{ResummonItems:[{id:"twilightforest:twilight_scepter"}]} run loot replace block ~ ~ ~ container.0 loot explorers_eve:item/empowered/lich_scepter
execute unless entity @s[tag=Dupe] if block ~ ~ ~ witherstormmod:super_beacon{ResummonItems:[{id:"twilightforest:zombie_scepter"}]} run loot replace block ~ ~ ~ container.0 loot explorers_eve:item/empowered/lich_scepter

#Soul Cannon is functional, but it's disabled due to being overpowered. Maybe some day...
#execute unless entity @s[tag=Dupe] if block ~ ~ ~ witherstormmod:super_beacon{ResummonItems:[{id:"dungeons_plus:soul_cannon"}]} run loot replace block ~ ~ ~ container.0 loot explorers_eve:item/empowered/soul_cannon

execute unless entity @s[tag=Dupe] if block ~ ~ ~ witherstormmod:super_beacon{ResummonItems:[{tag:{Empowered:1b}}]} run function explorers_eve:item/empower/success

setblock ~ ~1 ~ yellow_shulker_box
item replace block ~ ~1 ~ container.0 from block ~ ~ ~ container.0
loot spawn ~ ~0.75 ~ mine ~ ~1 ~ air{drop_contents:1b}
setblock ~ ~1 ~ air
data remove block ~ ~ ~ ResummonItems
execute if entity @s[tag=Success] positioned ~ ~0.75 ~ run data modify entity @e[type=item,limit=1,sort=nearest] Glowing set value 1b
execute unless entity @s[tag=Success] run playsound witherstormmod:withered_symbiont_launch_mob block @a ~ ~ ~ 2 2
execute unless entity @s[tag=Success] unless entity @s[tag=Dupe] run tellraw @a[gamemode=!spectator,distance=..24] {"text":"이 아이템은 강화될 수 없습니다!","color":"light_purple"}
function explorers_eve:item/empower/end