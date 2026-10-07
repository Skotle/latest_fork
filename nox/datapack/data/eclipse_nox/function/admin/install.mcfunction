execute unless dimension minecraft:overworld run tellraw @s {"text":"관측소는 오버월드에서만 설치할 수 있습니다.","color":"yellow"}
execute if dimension minecraft:overworld if score #state nx.state matches 0 positioned ~ ~ ~ align xyz run function eclipse_nox:arena/install
