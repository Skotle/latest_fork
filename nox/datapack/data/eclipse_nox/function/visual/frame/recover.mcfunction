scoreboard players set #frame nx.tmp 12
scoreboard players operation #frame nx.tmp -= #safe nx.safe
execute if score #frame nx.tmp matches ..0 run scoreboard players set #frame nx.tmp 0
scoreboard players set #thirty nx.tmp 12
scoreboard players set #fifteen nx.tmp 15
scoreboard players operation #frame nx.tmp *= #fifteen nx.tmp
scoreboard players operation #frame nx.tmp /= #thirty nx.tmp
execute if score #frame nx.tmp matches 16.. run scoreboard players set #frame nx.tmp 15
