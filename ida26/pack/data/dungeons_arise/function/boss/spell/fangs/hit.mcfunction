$execute at @e[tag=ida.target,scores={ida.sid=$(id)},limit=1] run particle minecraft:soul ~ ~0.5 ~ 1.5 0.8 1.5 0.05 55 force
$execute at @e[tag=ida.target,scores={ida.sid=$(id)},limit=1] run summon minecraft:evoker_fangs ~0 ~ ~0 {Tags:["ida.newfang"]}
data modify entity @e[tag=ida.newfang,limit=1] Owner set from entity @s UUID
tag @e[tag=ida.newfang] remove ida.newfang
$execute at @e[tag=ida.target,scores={ida.sid=$(id)},limit=1] run summon minecraft:evoker_fangs ~2 ~ ~0 {Tags:["ida.newfang"]}
data modify entity @e[tag=ida.newfang,limit=1] Owner set from entity @s UUID
tag @e[tag=ida.newfang] remove ida.newfang
$execute at @e[tag=ida.target,scores={ida.sid=$(id)},limit=1] run summon minecraft:evoker_fangs ~-2 ~ ~0 {Tags:["ida.newfang"]}
data modify entity @e[tag=ida.newfang,limit=1] Owner set from entity @s UUID
tag @e[tag=ida.newfang] remove ida.newfang
$execute at @e[tag=ida.target,scores={ida.sid=$(id)},limit=1] run summon minecraft:evoker_fangs ~0 ~ ~2 {Tags:["ida.newfang"]}
data modify entity @e[tag=ida.newfang,limit=1] Owner set from entity @s UUID
tag @e[tag=ida.newfang] remove ida.newfang
$execute at @e[tag=ida.target,scores={ida.sid=$(id)},limit=1] run summon minecraft:evoker_fangs ~0 ~ ~-2 {Tags:["ida.newfang"]}
data modify entity @e[tag=ida.newfang,limit=1] Owner set from entity @s UUID
tag @e[tag=ida.newfang] remove ida.newfang
