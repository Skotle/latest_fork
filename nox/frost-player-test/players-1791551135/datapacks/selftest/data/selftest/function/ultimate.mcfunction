execute store result storage selftest:results normal_after int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
kill @e[tag=fw.arrow]
scoreboard players set #cycle fw.cycle 8
function frost_warden:skills/begin
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
execute store result storage selftest:results ultimate_charge_clear int 1 run execute unless entity @e[tag=fw.stun_arrow]
function frost_warden:skills/casting
execute store result storage selftest:results ultimate_one int 1 run execute if entity @e[tag=fw.stun_arrow,nbt={PierceLevel:1b,damage:6.5d}]
execute store result storage selftest:results ultimate_before int 1 run data get entity @a[tag=probe.player,limit=1] Health 10
scoreboard players set #cast fw.cast 0
scoreboard players set #safe fw.safe 99999
scoreboard players set #next fw.next 99999
