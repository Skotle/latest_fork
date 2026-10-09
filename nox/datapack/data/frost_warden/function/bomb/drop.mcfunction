data modify storage frost_warden:shot vx set value 0.0d
data modify storage frost_warden:shot vy set value -1.8d
data modify storage frost_warden:shot vz set value 0.0d
data modify storage frost_warden:shot damage set value 0.2d
data modify storage frost_warden:shot owner set from storage frost_warden:ctx owner
scoreboard players set #explosive fw.tmp 1
function frost_warden:arrows/summon with storage frost_warden:shot
function frost_warden:arrows/register
