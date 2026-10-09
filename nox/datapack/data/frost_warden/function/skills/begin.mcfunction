scoreboard players add #cycle fw.cycle 1
execute if score #cycle fw.cycle matches 10.. run scoreboard players set #cycle fw.cycle 1
execute if score #cycle fw.cycle matches 1 run scoreboard players set #skill fw.skill 1
execute if score #cycle fw.cycle matches 2 run scoreboard players set #skill fw.skill 6
execute if score #cycle fw.cycle matches 3 run scoreboard players set #skill fw.skill 1
execute if score #cycle fw.cycle matches 4 run scoreboard players set #skill fw.skill 6
execute if score #cycle fw.cycle matches 5 run scoreboard players set #skill fw.skill 2
execute if score #cycle fw.cycle matches 6 run scoreboard players set #skill fw.skill 3
execute if score #cycle fw.cycle matches 7 run scoreboard players set #skill fw.skill 1
execute if score #cycle fw.cycle matches 8 run scoreboard players set #skill fw.skill 5
execute if score #cycle fw.cycle matches 9 run scoreboard players set #skill fw.skill 4
execute if score #skill fw.skill matches 2 unless score #focus fw.tmp matches 4.. run scoreboard players set #skill fw.skill 6
scoreboard players set #cast fw.cast 26
execute if score #skill fw.skill matches 2 run scoreboard players set #cast fw.cast 24
execute if score #skill fw.skill matches 4 run scoreboard players set #cast fw.cast 32
execute if score #skill fw.skill matches 3 run scoreboard players set #cast fw.cast 20
execute if score #skill fw.skill matches 6 run scoreboard players set #cast fw.cast 20
scoreboard players set #next fw.next 8
execute if score #phase fw.phase matches 2 run scoreboard players set #next fw.next 6
execute if score #phase fw.phase matches 3 run scoreboard players set #next fw.next 4
data merge entity @e[tag=fw.boss,limit=1] {NoAI:1b}
execute as @e[tag=fw.boss,limit=1] at @s facing entity @a[tag=fw.active,gamemode=!creative,sort=nearest,limit=1] eyes run tp @s ~ ~ ~ ~ ~
function frost_warden:skills/lock
execute if score #skill fw.skill matches 2 run scoreboard players set #focus fw.tmp 0
execute if score #skill fw.skill matches 3 run function frost_warden:ashe/hawk_begin
execute if score #skill fw.skill matches 5 run function frost_warden:ashe/walls_select
execute if score #skill fw.skill matches 1 run tellraw @a[tag=fw.member] {"text": "일제 사격! 활이 향하는 부채꼴 바깥이나 기둥 뒤로 이동하세요.", "color": "aqua"}
execute if score #skill fw.skill matches 2 run tellraw @a[tag=fw.member] {"text": "궁사의 집중! 강화 화살 5발 연사 — 엄폐하세요.", "color": "aqua"}
execute if score #skill fw.skill matches 3 run tellraw @a[tag=fw.member] {"text": "매 날리기! 정찰 중에는 피해 공격이 없습니다.", "color": "aqua"}
execute if score #skill fw.skill matches 4 run tellraw @a[tag=fw.member] {"text": "마법의 수정화살! 푸른 사선을 보고 옆으로 피하세요. 발사 후 짧은 반격 기회!", "color": "aqua"}
execute if score #skill fw.skill matches 5 run tellraw @a[tag=fw.member] {"text": "외벽 사격! 표시된 두 벽에서 한 번만 발사합니다.", "color": "aqua"}
execute at @e[tag=fw.boss,limit=1] run playsound minecraft:entity.stray.ambient hostile @a[tag=fw.active] ~ ~ ~ .7 1.5
