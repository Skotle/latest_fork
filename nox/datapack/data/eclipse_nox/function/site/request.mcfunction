execute if score #state nx.state matches 1 run tellraw @a[distance=..38] {"text":"다른 관측소에서 전투가 진행 중입니다.","color":"gray"}
execute if score #state nx.state matches 0 run function eclipse_nox:site/select
