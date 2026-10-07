$bossbar remove dungeons_arise:encounter_$(id)
$kill @e[tag=ida.add,scores={ida.sid=$(id)}]
$kill @e[tag=ida.target,scores={ida.sid=$(id)}]
$kill @e[tag=ida.visual,scores={ida.sid=$(id)}]
$team remove ida$(id)
