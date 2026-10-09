execute store result storage selftest:results pool_after_hit int 1 run scoreboard players get #pool fw.hp
execute store result storage selftest:results body_restored int 1 run data get entity @e[tag=fw.boss,limit=1] Health
tp @e[tag=fw.boss,limit=1] 128 81 -2
execute at @e[tag=fw.boss,limit=1] positioned ~ ~1.5 ~ rotated 180 0 run function frost_warden:skills/fan
execute store result storage selftest:results fan int 1 run execute if entity @e[tag=fw.arrow]
kill @e[tag=fw.arrow]
scoreboard players set #focus fw.tmp 4
scoreboard players set #cycle fw.cycle 4
function frost_warden:skills/begin
execute store result storage selftest:results focus_skill int 1 run scoreboard players get #skill fw.skill
execute store result storage selftest:results focus_spent int 1 run scoreboard players get #focus fw.tmp
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
function frost_warden:skills/casting
execute store result storage selftest:results focus_arrows int 1 run execute if entity @e[tag=fw.arrow,nbt={damage:0.9d,PierceLevel:0b}]
kill @e[tag=fw.arrow]
function frost_warden:ashe/walls_select
execute store result storage selftest:results wall_side_a int 1 run execute if entity @e[tag=fw.wall_live]
function frost_warden:walls/wave_one
execute store result storage selftest:results wall_arrows int 1 run execute if entity @e[tag=fw.wall_arrow]
kill @e[tag=fw.arrow]
function frost_warden:ashe/walls_select
execute store result storage selftest:results wall_side_b int 1 run execute if entity @e[tag=fw.wall_live]
scoreboard players set #cast fw.cast 0
scoreboard players set #safe fw.safe 99999
scoreboard players set #next fw.next 99999
scoreboard players operation #probe_pool fw.hp = #pool fw.hp
execute positioned 128 82 -8 rotated 0 0 run function frost_warden:arrows/normal
