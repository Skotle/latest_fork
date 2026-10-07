$kill @e[tag=ida.visual,scores={ida.sid=$(id)}]
effect give @s minecraft:invisibility infinite 0 true
execute if data entity @s equipment.head run data modify entity @s equipment.head.components."minecraft:equippable" set value {slot:"head",asset_id:"ida_boss:hidden"}
execute if data entity @s equipment.chest run data modify entity @s equipment.chest.components."minecraft:equippable" set value {slot:"chest",asset_id:"ida_boss:hidden"}
execute if data entity @s equipment.legs run data modify entity @s equipment.legs.components."minecraft:equippable" set value {slot:"legs",asset_id:"ida_boss:hidden"}
execute if data entity @s equipment.feet run data modify entity @s equipment.feet.components."minecraft:equippable" set value {slot:"feet",asset_id:"ida_boss:hidden"}
execute if data entity @s equipment.offhand run data modify entity @s equipment.offhand.components."minecraft:item_model" set value "ida_boss:hidden"
execute if data entity @s equipment.mainhand run data modify entity @s equipment.mainhand.components."minecraft:item_model" set value "ida_boss:hidden"
data modify entity @s CustomNameVisible set value 0b
data modify entity @s data.visual_version set value 1
$function dungeons_arise:boss/visual/$(kind)/spawn with entity @s data
