place template eclipse_nox:observatory ~-34 ~-2 ~-34
execute as @e[tag=nox.seed,distance=..2] at @s run function eclipse_nox:site/init
tellraw @s {"text":"지하 관측소 설치 완료. 자연 생성은 새 청크에서 작동합니다.","color":"green"}
