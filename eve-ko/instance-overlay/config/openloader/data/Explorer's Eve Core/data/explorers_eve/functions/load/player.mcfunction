#Runs once for every player. Gives loot, enables mode switching, then disables modes if the other one is active.
execute unless entity @s[tag=Reloaded] run function explorers_eve:load/player_full
tag @s remove Reloaded
scoreboard players enable @s Reload
scoreboard players enable @s Challenge
scoreboard players set @a StormAttackWait 1000000000
execute unless score @s ZetaCharges matches 0.. run scoreboard players set @s ZetaCharges 0
advancement grant @s from blue_skies:progression/root
execute if data storage world WitherStormSpawned run advancement grant @s only witherstormmod:main/root
execute unless data storage world Loaded run tellraw @s [{"text":"오류: 월드 시작 상태를 확인할 수 없습니다. 기능이 완전히 활성화되었는지 확인하고 /reload를 실행하거나 월드를 다시 시작하세요.","color":"red"}]
execute if data storage world Loaded unless data storage world WitherStormSpawned run tellraw @s [{"text":"탐험가의 전야에 오신 것을 환영합니다! 자신을 잘 살펴보고 준비가 되면 위더 스톰을 소환하세요!","color":"gray"}]
execute if data storage world Loaded if data storage world WitherStormSpawned run tellraw @s [{"text":"탐험가의 전야에 오신 것을 환영합니다!","color":"gray"}]
execute if data storage world Loaded run tag @s add Loaded
tag @s[advancements={explorers_eve:left_twilight=false}] add TwilightStuck