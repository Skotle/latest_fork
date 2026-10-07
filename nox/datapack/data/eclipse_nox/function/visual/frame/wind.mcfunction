scoreboard players operation #frame nx.tmp = #total nx.total
scoreboard players operation #frame nx.tmp -= #cast nx.cast
scoreboard players set #fifteen nx.tmp 15
scoreboard players operation #frame nx.tmp *= #fifteen nx.tmp
scoreboard players operation #denom nx.tmp = #total nx.total
scoreboard players remove #denom nx.tmp 8
execute if score #denom nx.tmp matches ..0 run scoreboard players set #denom nx.tmp 1
scoreboard players operation #frame nx.tmp /= #denom nx.tmp
execute if score #frame nx.tmp matches 16.. run scoreboard players set #frame nx.tmp 15
