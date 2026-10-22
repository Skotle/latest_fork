#Give one panel at a time until they're all done.
give @s blue_skies:zeal_lighter{display:{Lore:['{"text":"화재를 일으킵니다. Everbright 및 Everdawn으로 향하는 영구 포털을 활성화할 수도 있습니다.","color":"gray","italic":false}','{"text":"퓨즈를 켜는 데 어려움을 겪습니다 ...","color":"gray","italic":false}','{"text":"탐험가의 보물","color":"gold"}']},HideFlags:4,Unbreakable:1b,RepairCost:99,Enchantments:[{}]}
scoreboard players remove $Zeal Math 1
execute if score $Zeal Math matches 1.. run function explorers_eve:world/blue_skies/give_zeal_lighter