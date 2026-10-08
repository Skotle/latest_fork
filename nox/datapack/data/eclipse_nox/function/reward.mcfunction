give @s minecraft:amethyst_shard[minecraft:item_model="eclipse_nox:relic",minecraft:item_name={"text":"일식의 심장","color":"light_purple"},minecraft:lore=[{"text":"일식의 종지기 녹스 처치 증표","color":"gray"}],minecraft:custom_data={nox_relic:1b}] 1
give @s minecraft:diamond 4
experience add @s 500 points
advancement grant @s only eclipse_nox:challenge/victory
execute if score @s nx.clean matches 1 run advancement grant @s only eclipse_nox:challenge/flawless
function eclipse_nox:challenge/win
