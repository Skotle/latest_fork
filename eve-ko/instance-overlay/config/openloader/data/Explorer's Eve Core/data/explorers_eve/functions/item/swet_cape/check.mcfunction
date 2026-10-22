#Activates every time the player takes damage. Check if the cape is equipped, and if so, run effects.
advancement revoke @s only explorers_eve:damage_taken

execute if entity @s[curios={item:{id:"aether:swet_cape"}}] on attacker at @s unless entity @s[type=player] run function explorers_eve:item/swet_cape/effects
execute if entity @s[curios={item:{id:"aether:swet_cape",tag:{Unbreakable:1b,HideFlags:4,display:{Lore:['{"italic":false,"color":"gray","text":"착용자를 공격하는 슬라임 개체입니다."}','{"italic":false,"color":"gray","text":"또한 착용자가 Swets를 탈 수 있게 해줍니다."}','{"color":"gold","text":"탐험가의 보물"}']}}}}] on attacker at @s unless entity @s[type=player] run function explorers_eve:item/swet_cape/effects