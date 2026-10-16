AStages.addRestrictionForTag("copycats", "copycats", "astages:copycats")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('copycats')
    .titleOnAdd(stage => Component.literal("§6연구 완료!"))
    .subTitleOnAdd(stage => Component.literal("§l모방 블록"))
    .stay(120)

// ==================== Stage 1 ====================
AStages.addRestrictionForTag("stage1", "stage1", "astages:stage1")
    .globalShowName()
    .showInRecipeViewer()
    .hiddenName(stack => Component.literal("§c잠김 - 튜토리얼 완료!"))
    .useMessage(stack => Component.literal("튜토리얼을 완료해야 합니다! Cog-PDA를 확인해보세요!"))
    .pickupMessage(stack => Component.literal("튜토리얼을 완료해야 합니다! Cog-PDA를 확인해보세요!"))
    .placeMessage(stack => Component.literal("튜토리얼을 완료해야 합니다! Cog-PDA를 확인해보세요!"))
    .mineMessage(stack => Component.literal("튜토리얼을 완료해야 합니다! Cog-PDA를 확인해보세요!"))
    .attackMessage(stack => Component.literal("튜토리얼을 완료해야 합니다! Cog-PDA를 확인해보세요!"));

AStages.customizeStage('stage1')
    .titleOnAdd(stage => Component.literal("§6§a1단계 해금"))
    .subTitleOnAdd(stage => Component.literal("§l새로운 이정표를 진행할 수 있습니다"))
    .setFadeIn(20) 
    .setFadeOut(20) 
    .setStay(180) 

AStages.addRestrictionForTag("diving_equipment_mk1", "diving_equipment_mk1", "astages:diving_equipment_mk1")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('diving_equipment_mk1')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l구리 잠수 장비"))
    .stay(120)

AStages.addRestrictionForTag("machines_mk1", "machines_mk1", "astages:machines_mk1")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('machines_mk1')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l기초 기계"))
    .setStay(120) 

AStages.addRestrictionForTag("contraptions_mk1", "contraptions_mk1", "astages:contraptions_mk1")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('contraptions_mk1')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§lContraptions'))
    .setStay(120) 

AStages.addRestrictionForTag("rotational_power_generation_mk1", "rotational_power_generation_mk1", "astages:rotational_power_generation_mk1")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('rotational_power_generation_mk1')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l회전 동력 생산"))
    .setStay(120) 

AStages.addRestrictionForTag("rotational_power_transportation_mk1", "rotational_power_transportation_mk1", "astages:rotational_power_transportation_mk1")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('rotational_power_transportation_mk1')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l회전 동력 전달"))
    .setStay(120) 

AStages.addRestrictionForTag("logistics_mk1", "logistics_mk1", "astages:logistics_mk1")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('logistics_mk1')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§lLogistics'))
    .setStay(120) 

// ==================== Stage 2 ====================

AStages.customizeStage('stage2')
    .titleOnAdd(stage => Component.literal("§6§a2단계 해금"))
    .subTitleOnAdd(stage => Component.literal("§l새로운 이정표를 진행할 수 있습니다"))
    .setFadeIn(20) 
    .setFadeOut(20) 
    .setStay(180) 

AStages.addRestrictionForTag("machines_mk2", "machines_mk2", "astages:machines_mk2")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('machines_mk2')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l고급 가공"))
    .setStay(120) 

AStages.addRestrictionForTag("super_heating", "super_heating", "astages:super_heating")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('super_heating')
    .setAddTitle("§6이정표 해금") 
    .setAddSubTitle("§l초고열 가열") 
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l고급 가공"))
    .setStay(120) 

AStages.addRestrictionForTag("blueprints_mk1", "blueprints_mk1", "astages:blueprints_mk1")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('blueprints_mk1')
    .setAddTitle("§6이정표 해금") 
    .setAddSubTitle('§lSchematics') 
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§lSchematics'))
    .setStay(120) 

AStages.addRestrictionForTag("fluids_mk1", "fluids_mk1", "astages:fluids_mk1")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('fluids_mk1')
    .setAddTitle("§6이정표 해금") 
    .setAddSubTitle("§l기본 유체") 
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§lFluids'))
    .setStay(120) 

AStages.addRestrictionForTag("advanced_redstone_mk1", "advanced_redstone_mk1", "astages:advanced_redstone_mk1")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('advanced_redstone_mk1')
    .setAddTitle("§6이정표 해금") 
    .setAddSubTitle("§l고급 레드스톤") 
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l고급 레드스톤"))
    .setStay(120) 

AStages.addRestrictionForTag("post_production", "post_production", "astages:post_production")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('post_production')
    .setAddTitle("§6이정표 해금") 
    .setAddSubTitle("§l후기 생산") 
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l후기 생산"))
    .setStay(120) 

// ==================== Stage 3 ====================

AStages.customizeStage('stage3')
    .titleOnAdd(stage => Component.literal("§6§a3단계 해금"))
    .subTitleOnAdd(stage => Component.literal("§l새로운 이정표를 진행할 수 있습니다"))
    .setFadeIn(20) 
    .setFadeOut(20) 
    .setStay(180) 

AStages.addRestrictionForTag("brass_production", "brass_production", "astages:brass_production")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('brass_production')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l고급 제작"))
    .setStay(120) 

AStages.addRestrictionForTag("advanced_redstone_mk2", "advanced_redstone_mk2", "astages:advanced_redstone_mk2")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('advanced_redstone_mk2')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l스마트 레드스톤"))
    .setStay(120) 

AStages.addRestrictionForTag("better_item_managment", "better_item_managment", "astages:better_item_managment")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('better_item_managment')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l더 나은 아이템 관리"))
    .setStay(120) 

AStages.addRestrictionForTag("advanced_fluids", "advanced_fluids", "astages:advanced_fluids")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('advanced_fluids')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l더 나은 유체"))
    .setStay(120) 

AStages.addRestrictionForTag("logistics_mk3", "logistics_mk3", "astages:logistics_mk3")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('logistics_mk3')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l더 나은 물류"))
    .setStay(120) 

AStages.addRestrictionForTag("moving_contraptions_mk2", "moving_contraptions_mk2", "astages:moving_contraptions_mk2")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('moving_contraptions_mk2')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l더 나은 장치"))
    .setStay(120) 

// ==================== Stage 4 ====================

AStages.customizeStage('stage4')
    .titleOnAdd(stage => Component.literal("§6§a4단계 해금"))
    .subTitleOnAdd(stage => Component.literal("§l새로운 이정표를 진행할 수 있습니다"))
    .setFadeIn(20) 
    .setFadeOut(20) 
    .setStay(180) 

AStages.addRestrictionForTag("steam_power_generation", "steam_power_generation", "astages:steam_power_generation")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('steam_power_generation')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l증기 구성 요소"))
    .setStay(120) 

AStages.addRestrictionForTag("machines_mk4", "machines_mk4", "astages:machines_mk4")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('machines_mk4')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l순차 기계"))
    .setStay(120) 

AStages.addRestrictionForTag("trains", "trains", "astages:trains")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('trains')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§lTrains'))
    .setStay(120) 

AStages.addRestrictionForTag("advanced_machining", "advanced_machining", "astages:advanced_machining")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('advanced_machining')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l고급 가공"))
    .setStay(120) 

AStages.addRestrictionForTag("better_equipment", "better_equipment", "astages:better_equipment")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('better_equipment')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l더 나은 장비"))
    .setStay(120) 

AStages.addRestrictionForTag("vehicle_components", "vehicle_components", "astages:vehicle_components")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('vehicle_components')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l차량 부품"))
    .setStay(120) 

AStages.addRestrictionForTag("economy", "economy", "astages:economy")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('economy')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§lEconomy'))
    .setStay(120) 

// ==================== Stage 5 ====================

AStages.customizeStage('stage5')
    .titleOnAdd(stage => Component.literal("§6§a5단계 해금"))
    .subTitleOnAdd(stage => Component.literal("§l새로운 이정표를 진행할 수 있습니다"))
    .setFadeIn(20) 
    .setFadeOut(20) 
    .setStay(180) 

AStages.addRestrictionForTag("diesel_power_generation", "diesel_power_generation", "astages:diesel_power_generation")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('diesel_power_generation')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l디젤발전"))
    .setStay(120) 

AStages.addRestrictionForTag("oil", "oil", "astages:oil")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('oil')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l석유 생산"))
    .setStay(120) 

AStages.addRestrictionForTag("advanced_farming", "advanced_farming", "astages:advanced_farming")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('advanced_farming')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l고급 농업"))
    .setStay(120) 

AStages.addRestrictionForTag("electricity", "electricity", "astages:electricity")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('electricity')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§lElectricity'))
    .setStay(120) 

AStages.addRestrictionForTag("hypertubes", "hypertubes", "astages:hypertubes")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('hypertubes')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§lHypertubes'))
    .setStay(120)

AStages.addRestrictionForTag("enchantment_industry", "enchantment_industry", "astages:enchantment_industry")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('enchantment_industry')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l마법 산업"))
    .setStay(120)

// ==================== Stage 6 ====================

AStages.customizeStage('stage6')
    .titleOnAdd(stage => Component.literal("§6§a6단계 해금"))
    .subTitleOnAdd(stage => Component.literal("§l새로운 이정표를 진행할 수 있습니다"))
    .setFadeIn(20) 
    .setFadeOut(20) 
    .setStay(180) 

AStages.addRestrictionForTag("item_sink", "item_sink", "astages:item_sink")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('item_sink')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l아이템 소각기"))
    .setStay(120)

AStages.addRestrictionForTag("pattern_schematics", "pattern_schematics", "astages:pattern_schematics")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('pattern_schematics')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l패턴 회로도"))
    .setStay(120)

AStages.addRestrictionForTag("jetpack_mk1", "jetpack_mk1", "astages:jetpack_mk1")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('jetpack_mk1')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§lJetpack'))
    .setStay(120)

AStages.addRestrictionForTag("chunk_loading", "chunk_loading", "astages:chunk_loading")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('chunk_loading')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l청크 로딩"))
    .setStay(120)

AStages.addRestrictionForTag("cannons", "cannons", "astages:cannons")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('cannons')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§Cannons'))
    .setStay(120)

// ==================== Stage 7 ====================

AStages.customizeStage('stage7')
    .titleOnAdd(stage => Component.literal("§6§a7단계 해금"))
    .subTitleOnAdd(stage => Component.literal("§l새로운 이정표를 진행할 수 있습니다"))
    .setFadeIn(20) 
    .setFadeOut(20) 
    .setStay(180)

AStages.addRestrictionForTag("automated_trading", "automated_trading", "astages:automated_trading")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('automated_trading')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l자동화된 거래"))
    .setStay(120)

AStages.addRestrictionForTag("radar_components", "radar_components", "astages:radar_components")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('radar_components')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l레이더 구성요소"))
    .setStay(120)

AStages.addRestrictionForTag("optical_fabrication", "optical_fabrication", "astages:optical_fabrication")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('optical_fabrication')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l광학 제작"))
    .setStay(120)
    
AStages.addRestrictionForTag("engraving", "engraving", "astages:engraving")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('engraving')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§lEngraving'))
    .setStay(120)

AStages.addRestrictionForTag("airship_components", "airship_components", "astages:airship_components")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('airship_components')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l비행선 구성 요소"))
    .setStay(120)

AStages.addRestrictionForTag("astrophotography_gear", "astrophotography_gear", "astages:astrophotography_gear")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('astrophotography_gear')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l천체 사진 장비"))
    .setStay(120)

AStages.addRestrictionForTag("mobile_packages", "mobile_packages", "astages:mobile_packages")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('mobile_packages')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l모바일 패키지"))
    .setStay(120)

// ==================== Stage 8 ====================

AStages.customizeStage('stage8')
    .titleOnAdd(stage => Component.literal("§6§a8단계 해금"))
    .subTitleOnAdd(stage => Component.literal("§l새로운 이정표를 진행할 수 있습니다"))
    .setFadeIn(20) 
    .setFadeOut(20) 
    .setStay(180)

AStages.addRestrictionForTag("jetpack_mk2", "jetpack_mk2", "astages:jetpack_mk2")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('jetpack_mk2')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l네더라이트 장비"))
    .setStay(120)

AStages.addRestrictionForTag("spacecraft_components", "spacecraft_components", "astages:spacecraft_components")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('spacecraft_components')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l우주선 부품"))
    .setStay(120)

AStages.addRestrictionForTag("space_gear", "space_gear", "astages:space_gear")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('space_gear')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l스페이스 기어"))
    .setStay(120)

AStages.addRestrictionForTag("atmospheric_machinery", "atmospheric_machinery", "astages:atmospheric_machinery")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('atmospheric_machinery')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l대기 기계"))
    .setStay(120)

AStages.addRestrictionForTag("gyroscopic_components", "gyroscopic_components", "astages:gyroscopic_components")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('gyroscopic_components')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l자이로스코프 구성요소"))
    .setStay(120)

AStages.addRestrictionForTag("rocket_propulsion", "rocket_propulsion", "astages:rocket_propulsion")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('rocket_propulsion')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l로켓 추진"))
    .setStay(120) 

// ==================== Stage 9 ====================

AStages.customizeStage('stage9')
    .titleOnAdd(stage => Component.literal("§6§a9단계 해금"))
    .subTitleOnAdd(stage => Component.literal("§l새로운 이정표를 진행할 수 있습니다"))
    .setFadeIn(20) 
    .setFadeOut(20) 
    .setStay(180)

AStages.addRestrictionForTag("nuclear_reactor_components", "nuclear_reactor_components", "astages:nuclear_reactor_components")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('nuclear_reactor_components')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l원자로 구성 요소"))
    .setStay(120)

AStages.addRestrictionForTag("advanced_power_generation", "advanced_power_generation", "astages:advanced_power_generation")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('advanced_power_generation')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l첨단 발전"))
    .setStay(120)

AStages.addRestrictionForTag("lunar_spacecraft_components", "lunar_spacecraft_components", "astages:lunar_spacecraft_components")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('lunar_spacecraft_components')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l달 우주선 부품"))
    .setStay(120)

AStages.addRestrictionForTag("lunar_atmospheric_machinery", "lunar_atmospheric_machinery", "astages:lunar_atmospheric_machinery")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('lunar_atmospheric_machinery')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l달 대기 기계"))
    .setStay(120)

AStages.addRestrictionForTag("martian_space_gear", "martian_space_gear", "astages:martian_space_gear")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('martian_space_gear')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l화성 우주 장비"))
    .setStay(120)

AStages.addRestrictionForTag("mechanical_companion", "mechanical_companion", "astages:mechanical_companion")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('mechanical_companion')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l항공 자동화 물류"))
    .setStay(120)

// ==================== Stage 10 ====================

AStages.customizeStage('stage10')
    .titleOnAdd(stage => Component.literal("§6§a10단계 해금"))
    .subTitleOnAdd(stage => Component.literal("§l새로운 이정표를 진행할 수 있습니다"))
    .setFadeIn(20) 
    .setFadeOut(20) 
    .setStay(180)

AStages.addRestrictionForTag("createqol", "createqol", "astages:createqol")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('createqol')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§lCreateqol'))
    .setStay(120)

AStages.addRestrictionForTag("teleportation", "teleportation", "astages:teleportation")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('teleportation')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal('§Teleportation'))
    .setStay(120)

AStages.addRestrictionForTag("pocket_dimension", "pocket_dimension", "astages:pocket_dimension")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('pocket_dimension')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l포켓 차원"))
    .setStay(120)

AStages.addRestrictionForTag("advanced_teleportation", "advanced_teleportation", "astages:advanced_teleportation")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('advanced_teleportation')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l고급 순간이동"))
    .setStay(120)

AStages.addRestrictionForTag("advanced_propulsion", "advanced_propulsion", "astages:advanced_propulsion")
    .globalShowName()
    .showInRecipeViewer()
AStages.customizeStage('advanced_propulsion')
    .titleOnAdd(stage => Component.literal("§6이정표 해금"))
    .subTitleOnAdd(stage => Component.literal("§l고급 추진"))
    .setStay(120) 

//////////////////////////////////////////////////////////////////

const CREATIVE_BYPASS_STAGES = [
    "copycats",
    "stage1",
    "diving_equipment_mk1",
    "machines_mk1",
    "rotational_power_generation_mk1",
    "contraptions_mk1",
    "rotational_power_transportation_mk1",
    "logistics_mk1",
    "stage2",
    "machines_mk2",
    "super_heating",
    "blueprints_mk1",
    "fluids_mk1",
    "advanced_redstone_mk1",
    "post_production",
    "stage3",
    "brass_production",
    "advanced_redstone_mk2",
    "better_item_managment",
    "advanced_fluids",
    "logistics_mk3",
    "moving_contraptions_mk2",
    "stage4",
    "steam_power_generation",
    "machines_mk4",
    "trains",
    "advanced_machining",
    "better_equipment",
    "vehicle_components",
    "economy",
    "stage5",
    "diesel_power_generation",
    "oil",
    "advanced_farming",
    "electricity",
    "hypertubes",
    "enchantment_industry",
    "stage6",
    "item_sink",
    "pattern_schematics",
    "jetpack_mk1",
    "chunk_loading",
    "cannons",
    "stage7",
    "automated_trading",
    "radar_components",
    "optical_fabrication",
    "engraving",
    "airship_components",
    "astrophotography_gear",
    "mobile_packages",
    "stage8",
    "jetpack_mk2",
    "spacecraft_components",
    "space_gear",
    "atmospheric_machinery",
    "gyroscopic_components",
    "rocket_propulsion",
    "stage9",
    "nuclear_reactor_components",
    "advanced_power_generation",
    "lunar_spacecraft_components",
    "lunar_atmospheric_machinery",
    "martian_space_gear",
    "mechanical_companion",
    "stage10",
    "createqol",
    "teleportation",
    "pocket_dimension",
    "advanced_teleportation",
    "advanced_propulsion"
]

console.info("크리에이티브 월드 잠금 해제 로딩 중")

const CREATIVE_WORLD_INITIALIZED = "creative_world_initialized"


PlayerEvents.loggedIn(event => {

    const player = event.player

    if (player.persistentData.getBoolean(CREATIVE_WORLD_INITIALIZED)) {
        return
    }
    
    player.persistentData.putBoolean(
        CREATIVE_WORLD_INITIALIZED,
        true
    )

    if (!player.isCreative()) {

        console.info(
            "[크리에이티브 월드 잠금 해제] " +
            player.username +
            " SURVIVAL에서 생성/참여 - 스테이지가 부여되지 않습니다."
        )

        return
    }

    console.info(
        "[크리에이티브 월드 잠금 해제] " +
        player.username +
        " CREATIVE에서 생성/참여했습니다!"
    )

    // Join message
    player.tell(
        "§6§l창의적인 세계가 발견되었습니다!§r\n" +
        "§f모든 단계가 완료되었습니다. §a잠금 해제됨 §f당신이 이 세상에 합류했기 때문에 §e크리에이티브 모드§f."
    )


    let addedStages = 0


    for (const stageName of CREATIVE_BYPASS_STAGES) {

        if (!AStages.playerHasStage(player, stageName)) {

            AStages.addStageToPlayer(
                player,
                stageName
            )

            addedStages++

            console.info(
                "[크리에이티브 세계 잠금 해제] 추가됨: " +
                stageName
            )
        }
    }


    console.info(
        "[크리에이티브 월드 잠금 해제] 완료 - " +
        addedStages +
        " 단계가 부여됩니다."
    )
})

//////////////////////////////////////////////////////////////////

ServerEvents.commandRegistry(event => {

    const { commands } = event

    event.register(
        commands.literal('unlockallstages')
            .requires(source => source.hasPermission(2))
            .executes(ctx => {

                const player = ctx.source.player

                if (!player) {
                    return 0
                }

                let addedStages = 0

                for (const stageName of CREATIVE_BYPASS_STAGES) {

                    if (!AStages.playerHasStage(player, stageName)) {

                        AStages.addStageToPlayer(
                            player,
                            stageName
                        )

                        addedStages++

                        console.info(
                            "[모든 단계 잠금 해제] 추가됨: " +
                            stageName +
                            " 에게 " +
                            player.username
                        )
                    }
                }

                player.tell(
                    "§6§l스테이지 §8» §e잠금 해제됨 §6" +
                    addedStages +
                    " §e단계!"
                )

                console.info(
                    "[모든 단계 잠금 해제] " +
                    player.username +
                    " 잠금 해제됨 " +
                    addedStages +
                    " 단계."
                )

                return 1
            })
    )
})