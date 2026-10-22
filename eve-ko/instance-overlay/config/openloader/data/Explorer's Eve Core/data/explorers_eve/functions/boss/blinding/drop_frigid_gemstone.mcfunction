#No. This triggers every tick, by the way.
curios drop @s necklace
execute at @s positioned ~ ~1 ~ as @e[type=item,limit=1,sort=nearest,distance=..1.5] run data merge entity @s {Glowing:1b,Invulnerable:1b,Health:10000,Age:-32768,PickupDelay:0}
tellraw @s [{"text":"당신의 Frigid Gemstone이 목에서 미끄러져 나갑니다! 여기서는 사용할 수 없습니다!","color":"gray"}]