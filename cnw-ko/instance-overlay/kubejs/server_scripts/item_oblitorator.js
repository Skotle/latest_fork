const obliterateItems = [
  'kubejs:item_sink',
  'kubejs:item_sink_powered',
  'createdeco:gold_coin',
  'createdeco:gold_coinstack',
  'createdeco:iron_coin',
  'createdeco:iron_coinstack',
  'createdeco:copper_coin',
  'createdeco:copper_coinstack',
  'createdeco:zinc_coin',
  'createdeco:zinc_coinstack',
  'createdeco:brass_coin',
  'createdeco:brass_coinstack',
  'createdeco:netherite_coin',
  'createdeco:netherite_coinstack',
  'createdeco:industrial_iron_coin',
  'createdeco:industrial_iron_coinstack',
  'create_power_loader:empty_andesite_chunk_loader',  
  'create_power_loader:empty_brass_chunk_loader',  
  'createqol:shadow_radiance_helmet',
  'createqol:shadow_radiance_chestplate',
  'createqol:shadow_radiance_leggings',
  'createqol:shadow_radiance_boots',
  'createqol:refined_radiance_helmet',
  'createqol:refined_radiance_chestplate',
  'createqol:refined_radiance_leggings',
  'createqol:refined_radiance_boots',
  'createqol:shadow_steel_helmet',
  'createqol:shadow_steel_chestplate',
  'createqol:shadow_steel_leggings',
  'createqol:shadow_steel_boots',
  'createqol:shadow_radiance_sword',
  'createqol:shadow_radiance_pickaxe',
  'createqol:shadow_radiance_axe',
  'createqol:shadow_radiance_shovel',
  'createqol:shadow_radiance_hoe',
  'createqol:refined_radiance_sword',
  'createqol:refined_radiance_pickaxe',
  'createqol:refined_radiance_axe',
  'createqol:refined_radiance_shovel',
  'createqol:refined_radiance_hoe',
  'createqol:shadow_steel_sword',
  'createqol:shadow_steel_pickaxe',
  'createqol:shadow_steel_axe',
  'createqol:shadow_steel_shovel',
  'createqol:shadow_steel_hoe',
  'createteleporters:advanced_part',
  'createpropulsion:solid_burner',
  'createpropulsion:liquid_burner',
  'createpropulsion:stirling_engine',
  'block_factorys_bosses:knight_helmet',
  'block_factorys_bosses:knight_chestplate',
  'block_factorys_bosses:knight_leggings',
  'block_factorys_bosses:knight_boots',
  'block_factorys_bosses:enhanced_shield',
  'block_factorys_bosses:dragon_bones_chestplate',
  'block_factorys_bosses:dragon_bones_leggings',
  'block_factorys_bosses:dragon_bones_boots',
  'block_factorys_bosses:dragon_skull',
  'block_factorys_bosses:large_sword',
  'block_factorys_bosses:warrior_sword',
  'block_factorys_bosses:dagger',
  'block_factorys_bosses:knight_sword',
  'block_factorys_bosses:pirate_saber',
  'block_factorys_bosses:sandworm_gauntlet',
  'block_factorys_bosses:ice_gauntlet',
  'block_factorys_bosses:kraken_trident',
  'block_factorys_bosses:dragon_guard_shield',
  'block_factorys_bosses:undying_tentacle',
  'block_factorys_bosses:kraken_tooth',
  'block_factorys_bosses:dragon_bone',
  'northstar:circuit',
  'northstar:advanced_circuit',
  'createnuclear:steel_ingot',
  'createnuclear:steel_nugget',
  'quark:potato_crate',
  'quark:carrot_crate',
  'quark:beetroot_crate',
  'supplementaries:gold_bars',
]

// Check if itemID exists within obliterateItems
function ObliterateCheck(itemID) {
    let check = false
    for (let i = 0; i < obliterateItems.length; i++) {
        let id = obliterateItems[i]
        let reg = new RegExp(id)
        if (typeof id == "string") { reg = new RegExp(`^${id}$`) }
        if (reg.test(itemID)) {
            check = true
            break
        }
    }
    return check
}

// Remove recipes
ServerEvents.recipes(event => {
    event.remove({ input: obliterateItems })
    event.remove({ output: obliterateItems })
})

// Remove tags
ServerEvents.tags('item', event => {
    event.removeAllTagsFrom(obliterateItems)
})

// Append disabled tooltip
ItemEvents.modifyTooltips(event => {
    event.add(obliterateItems, Text.red("사용 불가"))
})

// Remove from recipe viewer
RecipeViewerEvents.removeEntriesCompletely('item', event => {
    event.remove(obliterateItems)
})

// Remove from loot pools
LootJS.lootTables(event => {
    event.modifyLootTables(/.*/).removeItem(obliterateItems)
})

// Destroy on interaction
BlockEvents.rightClicked(event => {
    let { block } = event
    if (ObliterateCheck(block.id)) { block.set('minecraft:air') }
})

// Destroy on block placement
BlockEvents.placed(event => {
    let { block } = event
    if (ObliterateCheck(block.id)) {
        block.set('minecraft:air')
    }
})

// Destroy on pickup
ItemEvents.canPickUp(event => {
    let { item, itemEntity } = event
    if(itemEntity.hasPickUpDelay()) return
    if (ObliterateCheck(item.id)) { item.setCount(0) }
})

// Destroy on drop
ItemEvents.dropped(event => {
    let { item } = event
    if (ObliterateCheck(item.id)) { item.setCount(0) }
})

// Destroy on inventory changed
PlayerEvents.inventoryChanged(event => {
    let { item, player } = event
    if (ObliterateCheck(item.id)) {
        player.inventory.clear(item);
    }
})