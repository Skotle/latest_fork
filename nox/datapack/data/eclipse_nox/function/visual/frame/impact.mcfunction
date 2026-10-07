scoreboard players set #frame nx.tmp 8
scoreboard players operation #frame nx.tmp -= #cast nx.cast
scoreboard players set #fifteen nx.tmp 15
scoreboard players set #eighteen nx.tmp 8
scoreboard players operation #frame nx.tmp *= #fifteen nx.tmp
scoreboard players operation #frame nx.tmp /= #eighteen nx.tmp
