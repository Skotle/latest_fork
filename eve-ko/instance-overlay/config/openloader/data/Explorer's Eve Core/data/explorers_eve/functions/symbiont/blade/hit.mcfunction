#Triggered via advancement for melee.
advancement revoke @s only explorers_eve:hit_by_resummoned_symbiont
execute at @e[type=witherstormmod:withered_symbiont,tag=WeaponActive,scores={SymbiontBladeCharge=125..249},limit=1,sort=nearest,distance=..8] run summon creeper ~ ~1.5 ~ {Tags:["ApocalypseIgnore"],Silent:1b,ExplosionRadius:4b,Fuse:0,CustomName:'{"text":"엄청난 폭발"}'}
execute at @e[type=witherstormmod:withered_symbiont,tag=WeaponActive,scores={SymbiontBladeCharge=250..},limit=1,sort=nearest,distance=..8] run summon creeper ~ ~1.5 ~ {Tags:["ApocalypseIgnore"],Silent:1b,ExplosionRadius:5b,Fuse:0,CustomName:'{"text":"엄청난 폭발"}'}
execute at @e[type=witherstormmod:withered_symbiont,tag=WeaponActive,scores={SymbiontBladeCharge=125..},limit=1,sort=nearest,distance=..8] run playsound witherstormmod:formidi_blade_decharge hostile @a ~ ~1 ~ 3 1
scoreboard players reset @e[type=witherstormmod:withered_symbiont,tag=WeaponActive,limit=1,sort=nearest] SymbiontBladeCharge