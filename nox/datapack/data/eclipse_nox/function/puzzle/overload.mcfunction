summon minecraft:marker ~ ~ ~ {Tags:["nox.owned","nox.overload"]}
scoreboard players set @e[tag=nox.overload,sort=nearest,limit=1] nx.time 20
tellraw @a[tag=nox.member] {"text": "공명 과부하! 방금 울린 종에서 떨어지세요. 1초 후 폭발.", "color": "gold"}
scoreboard players add #mistakes nx.tmp 1
