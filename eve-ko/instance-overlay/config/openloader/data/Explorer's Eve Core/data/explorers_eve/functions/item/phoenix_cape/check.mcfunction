#Activates whenever the player slays a mob via melee. If the cape's equipped, proceed.
advancement revoke @s only explorers_eve:slain_mob

execute if entity @s[curios={item:{id:"lost_aether_content:phoenix_cape"}}] positioned ^ ^1 ^3.5 run function explorers_eve:item/phoenix_cape/eruption
execute if entity @s[curios={item:{id:"lost_aether_content:phoenix_cape",tag:{Unbreakable:1b,HideFlags:4,display:{Lore:['{"italic":false,"color":"gray","text":"생물이 근접 공격으로 죽으면 갑옷을 녹이는 폭발을 일으킵니다."}','{"italic":false,"color":"gray","text":"또한 공허 속으로 떨어질 위험이 있는 경우 착용자를 공중에 띄웁니다."}','{"color":"gold","text":"탐험가의 보물"}']}}}}] positioned ^ ^1 ^3.5 run function explorers_eve:item/phoenix_cape/eruption