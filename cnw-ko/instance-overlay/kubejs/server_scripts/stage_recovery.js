const COPYCATS_DATA = "cnw_stage_copycats"

const STAGE1_DATA = "cnw_stage_stage1"
const DIVING_EQUIPMENT_MK1_DATA = "cnw_stage_diving_equipment_mk1"
const MACHINES_MK1_DATA = "cnw_stage_machines_mk1"
const ROTATIONAL_POWER_GENERATION_MK1_DATA = "cnw_stage_rotational_power_generation_mk1"
const CONTRAPTIONS_MK1_DATA = "cnw_stage_contraptions_mk1"
const ROTATIONAL_POWER_TRANSPORTATION_MK1_DATA = "cnw_stage_rotational_power_transportation_mk1"
const LOGISTICS_MK1_DATA = "cnw_stage_logistics_mk1"

const STAGE2_DATA = "cnw_stage_stage2"
const MACHINES_MK2_DATA = "cnw_stage_machines_mk2"
const SUPER_HEATING_DATA = "cnw_stage_super_heating"
const BLUEPRINTS_MK1_DATA = "cnw_stage_blueprints_mk1"
const FLUIDS_MK1_DATA = "cnw_stage_fluids_mk1"
const ADVANCED_REDSTONE_MK1_DATA = "cnw_stage_advanced_redstone_mk1"
const POST_PRODUCTION_DATA = "cnw_stage_post_production"

const STAGE3_DATA = "cnw_stage_stage3"
const BRASS_PRODUCTION_DATA = "cnw_stage_brass_production"
const ADVANCED_REDSTONE_MK2_DATA = "cnw_stage_advanced_redstone_mk2"
const BETTER_ITEM_MANAGMENT_DATA = "cnw_stage_better_item_managment"
const ADVANCED_FLUIDS_DATA = "cnw_stage_advanced_fluids"
const LOGISTICS_MK3_DATA = "cnw_stage_logistics_mk3"
const MOVING_CONTRAPTIONS_MK2_DATA = "cnw_stage_moving_contraptions_mk2"

const STAGE4_DATA = "cnw_stage_stage4"
const STEAM_POWER_GENERATION_DATA = "cnw_stage_steam_power_generation"
const MACHINES_MK4_DATA = "cnw_stage_machines_mk4"
const TRAINS_DATA = "cnw_stage_trains"
const ADVANCED_MACHINING_DATA = "cnw_stage_advanced_machining"
const BETTER_EQUIPMENT_DATA = "cnw_stage_better_equipment"
const VEHICLE_COMPONENTS_DATA = "cnw_stage_vehicle_components"
const ECONOMY_DATA = "cnw_stage_economy"

const STAGE5_DATA = "cnw_stage_stage5"
const DIESEL_POWER_GENERATION_DATA = "cnw_stage_diesel_power_generation"
const OIL_DATA = "cnw_stage_oil"
const ADVANCED_FARMING_DATA = "cnw_stage_advanced_farming"
const ELECTRICITY_DATA = "cnw_stage_electricity"
const HYPERTUBES_DATA = "cnw_stage_hypertubes"
const ENCHANTMENT_INDUSTRY_DATA = "cnw_stage_enchantment_industry"

const STAGE6_DATA = "cnw_stage_stage6"
const ITEM_SINK_DATA = "cnw_stage_item_sink"
const PATTERN_SCHEMATICS_DATA = "cnw_stage_pattern_schematics"
const JETPACK_MK1_DATA = "cnw_stage_jetpack_mk1"
const CHUNK_LOADING_DATA = "cnw_stage_chunk_loading"
const CANNONS_DATA = "cnw_stage_cannons"

const STAGE7_DATA = "cnw_stage_stage7"
const AUTOMATED_TRADING_DATA = "cnw_stage_automated_trading"
const RADAR_COMPONENTS_DATA = "cnw_stage_radar_components"
const OPTICAL_FABRICATION_DATA = "cnw_stage_optical_fabrication"
const ENGRAVING_DATA = "cnw_stage_engraving"
const AIRSHIP_COMPONENTS_DATA = "cnw_stage_airship_components"
const ASTROPHOTOGRAPHY_GEAR_DATA = "cnw_stage_astrophotography_gear"
const MOBILE_PACKAGES_DATA = "cnw_stage_mobile_packages"

const STAGE8_DATA = "cnw_stage_stage8"
const JETPACK_MK2_DATA = "cnw_stage_jetpack_mk2"
const SPACECRAFT_COMPONENTS_DATA = "cnw_stage_spacecraft_components"
const SPACE_GEAR_DATA = "cnw_stage_space_gear"
const ATMOSPHERIC_MACHINERY_DATA = "cnw_stage_atmospheric_machinery"
const GYROSCOPIC_COMPONENTS_DATA = "cnw_stage_gyroscopic_components"
const ROCKET_PROPULSION_DATA = "cnw_stage_rocket_propulsion"

const STAGE9_DATA = "cnw_stage_stage9"
const NUCLEAR_REACTOR_COMPONENTS_DATA = "cnw_stage_nuclear_reactor_components"
const ADVANCED_POWER_GENERATION_DATA = "cnw_stage_advanced_power_generation"
const LUNAR_SPACECRAFT_COMPONENTS_DATA = "cnw_stage_lunar_spacecraft_components"
const LUNAR_ATMOSPHERIC_MACHINERY_DATA = "cnw_stage_lunar_atmospheric_machinery"
const MARTIAN_SPACE_GEAR_DATA = "cnw_stage_martian_space_gear"
const MECHANICAL_COMPANION_DATA = "cnw_stage_mechanical_companion"

const STAGE10_DATA = "cnw_stage_stage10"
const CREATEQOL_DATA = "cnw_stage_createqol"
const TELEPORTATION_DATA = "cnw_stage_teleportation"
const POCKET_DIMENSION_DATA = "cnw_stage_pocket_dimension"
const ADVANCED_TELEPORTATION_DATA = "cnw_stage_advanced_teleportation"
const ADVANCED_PROPULSION_DATA = "cnw_stage_advanced_propulsion"

function restoreCopycats(player) {

    if (!player.persistentData.getBoolean(COPYCATS_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "copycats")) {
        return
    }

    AStages.addStageToPlayer(player, "copycats")

    console.info(
        "[STAGE RECOVERY] RESTORED copycats TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e모방범 §f스테이지가 복구되었습니다."
    )
}


function restoreStage1(player) {

    if (!player.persistentData.getBoolean(STAGE1_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "stage1")) {
        return
    }

    AStages.addStageToPlayer(player, "stage1")

    console.info(
        "[STAGE RECOVERY] RESTORED stage1 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e1 단계 §f스테이지가 복구되었습니다."
    )
}


function restoreDivingEquipmentMk1(player) {

    if (!player.persistentData.getBoolean(DIVING_EQUIPMENT_MK1_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "diving_equipment_mk1")) {
        return
    }

    AStages.addStageToPlayer(player, "diving_equipment_mk1")

    console.info(
        "[STAGE RECOVERY] RESTORED diving_equipment_mk1 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §ediving_equipment_mk1 §f스테이지가 복구되었습니다."
    )
}


function restoreMachinesMk1(player) {

    if (!player.persistentData.getBoolean(MACHINES_MK1_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "machines_mk1")) {
        return
    }

    AStages.addStageToPlayer(player, "machines_mk1")

    console.info(
        "[STAGE RECOVERY] RESTORED machines_mk1 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §emachine_mk1 §f스테이지가 복구되었습니다."
    )
}


function restoreRotationalPowerGenerationMk1(player) {

    if (!player.persistentData.getBoolean(ROTATIONAL_POWER_GENERATION_MK1_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "rotational_power_generation_mk1")) {
        return
    }

    AStages.addStageToPlayer(player, "rotational_power_generation_mk1")

    console.info(
        "[STAGE RECOVERY] RESTORED rotational_power_generation_mk1 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e회전_전력_세대_mk1 §f스테이지가 복구되었습니다."
    )
}


function restoreContraptionsMk1(player) {

    if (!player.persistentData.getBoolean(CONTRAPTIONS_MK1_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "contraptions_mk1")) {
        return
    }

    AStages.addStageToPlayer(player, "contraptions_mk1")

    console.info(
        "[STAGE RECOVERY] RESTORED contraptions_mk1 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e장치_mk1 §f스테이지가 복구되었습니다."
    )
}


function restoreRotationalPowerTransportationMk1(player) {

    if (!player.persistentData.getBoolean(ROTATIONAL_POWER_TRANSPORTATION_MK1_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "rotational_power_transportation_mk1")) {
        return
    }

    AStages.addStageToPlayer(player, "rotational_power_transportation_mk1")

    console.info(
        "[STAGE RECOVERY] RESTORED rotational_power_transportation_mk1 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e회전_전력_수송_mk1 §f스테이지가 복구되었습니다."
    )
}


function restoreLogisticsMk1(player) {

    if (!player.persistentData.getBoolean(LOGISTICS_MK1_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "logistics_mk1")) {
        return
    }

    AStages.addStageToPlayer(player, "logistics_mk1")

    console.info(
        "[STAGE RECOVERY] RESTORED logistics_mk1 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e물류_mk1 §f스테이지가 복구되었습니다."
    )
}


function restoreStage2(player) {

    if (!player.persistentData.getBoolean(STAGE2_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "stage2")) {
        return
    }

    AStages.addStageToPlayer(player, "stage2")

    console.info(
        "[STAGE RECOVERY] RESTORED stage2 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e2단계 §f스테이지가 복구되었습니다."
    )
}


function restoreMachinesMk2(player) {

    if (!player.persistentData.getBoolean(MACHINES_MK2_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "machines_mk2")) {
        return
    }

    AStages.addStageToPlayer(player, "machines_mk2")

    console.info(
        "[STAGE RECOVERY] RESTORED machines_mk2 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §emachine_mk2 §f스테이지가 복구되었습니다."
    )
}


function restoreSuperHeating(player) {

    if (!player.persistentData.getBoolean(SUPER_HEATING_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "super_heating")) {
        return
    }

    AStages.addStageToPlayer(player, "super_heating")

    console.info(
        "[STAGE RECOVERY] RESTORED super_heating TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e과열 §f스테이지가 복구되었습니다."
    )
}


function restoreBlueprintsMk1(player) {

    if (!player.persistentData.getBoolean(BLUEPRINTS_MK1_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "blueprints_mk1")) {
        return
    }

    AStages.addStageToPlayer(player, "blueprints_mk1")

    console.info(
        "[STAGE RECOVERY] RESTORED blueprints_mk1 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §eblueprints_mk1 §f스테이지가 복구되었습니다."
    )
}


function restoreFluidsMk1(player) {

    if (!player.persistentData.getBoolean(FLUIDS_MK1_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "fluids_mk1")) {
        return
    }

    AStages.addStageToPlayer(player, "fluids_mk1")

    console.info(
        "[STAGE RECOVERY] RESTORED fluids_mk1 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e유체_mk1 §f스테이지가 복구되었습니다."
    )
}


function restoreAdvancedRedstoneMk1(player) {

    if (!player.persistentData.getBoolean(ADVANCED_REDSTONE_MK1_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "advanced_redstone_mk1")) {
        return
    }

    AStages.addStageToPlayer(player, "advanced_redstone_mk1")

    console.info(
        "[STAGE RECOVERY] RESTORED advanced_redstone_mk1 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §eAdvanced_redstone_mk1 §f스테이지가 복구되었습니다."
    )
}


function restorePostProduction(player) {

    if (!player.persistentData.getBoolean(POST_PRODUCTION_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "post_production")) {
        return
    }

    AStages.addStageToPlayer(player, "post_production")

    console.info(
        "[STAGE RECOVERY] RESTORED post_production TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e후반작업 §f스테이지가 복구되었습니다."
    )
}


function restoreStage3(player) {

    if (!player.persistentData.getBoolean(STAGE3_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "stage3")) {
        return
    }

    AStages.addStageToPlayer(player, "stage3")

    console.info(
        "[STAGE RECOVERY] RESTORED stage3 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e3단계 §f스테이지가 복구되었습니다."
    )
}


function restoreBrassProduction(player) {

    if (!player.persistentData.getBoolean(BRASS_PRODUCTION_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "brass_production")) {
        return
    }

    AStages.addStageToPlayer(player, "brass_production")

    console.info(
        "[STAGE RECOVERY] RESTORED brass_production TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e황동_생산 §f스테이지가 복구되었습니다."
    )
}


function restoreAdvancedRedstoneMk2(player) {

    if (!player.persistentData.getBoolean(ADVANCED_REDSTONE_MK2_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "advanced_redstone_mk2")) {
        return
    }

    AStages.addStageToPlayer(player, "advanced_redstone_mk2")

    console.info(
        "[STAGE RECOVERY] RESTORED advanced_redstone_mk2 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §eAdvanced_redstone_mk2 §f스테이지가 복구되었습니다."
    )
}


function restoreBetterItemManagment(player) {

    if (!player.persistentData.getBoolean(BETTER_ITEM_MANAGMENT_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "better_item_managment")) {
        return
    }

    AStages.addStageToPlayer(player, "better_item_managment")

    console.info(
        "[STAGE RECOVERY] RESTORED better_item_managment TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §ebetter_item_managment §f스테이지가 복구되었습니다."
    )
}


function restoreAdvancedFluids(player) {

    if (!player.persistentData.getBoolean(ADVANCED_FLUIDS_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "advanced_fluids")) {
        return
    }

    AStages.addStageToPlayer(player, "advanced_fluids")

    console.info(
        "[STAGE RECOVERY] RESTORED advanced_fluids TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e고급_유체 §f스테이지가 복구되었습니다."
    )
}


function restoreLogisticsMk3(player) {

    if (!player.persistentData.getBoolean(LOGISTICS_MK3_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "logistics_mk3")) {
        return
    }

    AStages.addStageToPlayer(player, "logistics_mk3")

    console.info(
        "[STAGE RECOVERY] RESTORED logistics_mk3 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e물류_mk3 §f스테이지가 복구되었습니다."
    )
}


function restoreMovingContraptionsMk2(player) {

    if (!player.persistentData.getBoolean(MOVING_CONTRAPTIONS_MK2_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "moving_contraptions_mk2")) {
        return
    }

    AStages.addStageToPlayer(player, "moving_contraptions_mk2")

    console.info(
        "[STAGE RECOVERY] RESTORED moving_contraptions_mk2 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §eMoving_contraptions_mk2 §f스테이지가 복구되었습니다."
    )
}


function restoreStage4(player) {

    if (!player.persistentData.getBoolean(STAGE4_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "stage4")) {
        return
    }

    AStages.addStageToPlayer(player, "stage4")

    console.info(
        "[STAGE RECOVERY] RESTORED stage4 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e4단계 §f스테이지가 복구되었습니다."
    )
}


function restoreSteamPowerGeneration(player) {

    if (!player.persistentData.getBoolean(STEAM_POWER_GENERATION_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "steam_power_generation")) {
        return
    }

    AStages.addStageToPlayer(player, "steam_power_generation")

    console.info(
        "[STAGE RECOVERY] RESTORED steam_power_generation TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e증기_발전_발전 §f스테이지가 복구되었습니다."
    )
}


function restoreMachinesMk4(player) {

    if (!player.persistentData.getBoolean(MACHINES_MK4_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "machines_mk4")) {
        return
    }

    AStages.addStageToPlayer(player, "machines_mk4")

    console.info(
        "[STAGE RECOVERY] RESTORED machines_mk4 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §emachine_mk4 §f스테이지가 복구되었습니다."
    )
}


function restoreTrains(player) {

    if (!player.persistentData.getBoolean(TRAINS_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "trains")) {
        return
    }

    AStages.addStageToPlayer(player, "trains")

    console.info(
        "[STAGE RECOVERY] RESTORED trains TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e기차 §f스테이지가 복구되었습니다."
    )
}


function restoreAdvancedMachining(player) {

    if (!player.persistentData.getBoolean(ADVANCED_MACHINING_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "advanced_machining")) {
        return
    }

    AStages.addStageToPlayer(player, "advanced_machining")

    console.info(
        "[STAGE RECOVERY] RESTORED advanced_machining TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e고급 가공 §f스테이지가 복구되었습니다."
    )
}


function restoreBetterEquipment(player) {

    if (!player.persistentData.getBoolean(BETTER_EQUIPMENT_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "better_equipment")) {
        return
    }

    AStages.addStageToPlayer(player, "better_equipment")

    console.info(
        "[STAGE RECOVERY] RESTORED better_equipment TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e더 나은 장비 §f스테이지가 복구되었습니다."
    )
}


function restoreVehicleComponents(player) {

    if (!player.persistentData.getBoolean(VEHICLE_COMPONENTS_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "vehicle_components")) {
        return
    }

    AStages.addStageToPlayer(player, "vehicle_components")

    console.info(
        "[STAGE RECOVERY] RESTORED vehicle_components TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e차량_구성요소 §f스테이지가 복구되었습니다."
    )
}


function restoreEconomy(player) {

    if (!player.persistentData.getBoolean(ECONOMY_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "economy")) {
        return
    }

    AStages.addStageToPlayer(player, "economy")

    console.info(
        "[STAGE RECOVERY] RESTORED economy TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e경제 §f스테이지가 복구되었습니다."
    )
}


function restoreStage5(player) {

    if (!player.persistentData.getBoolean(STAGE5_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "stage5")) {
        return
    }

    AStages.addStageToPlayer(player, "stage5")

    console.info(
        "[STAGE RECOVERY] RESTORED stage5 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e5단계 §f스테이지가 복구되었습니다."
    )
}


function restoreDieselPowerGeneration(player) {

    if (!player.persistentData.getBoolean(DIESEL_POWER_GENERATION_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "diesel_power_generation")) {
        return
    }

    AStages.addStageToPlayer(player, "diesel_power_generation")

    console.info(
        "[STAGE RECOVERY] RESTORED diesel_power_generation TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e디젤 발전_발전 §f스테이지가 복구되었습니다."
    )
}


function restoreOil(player) {

    if (!player.persistentData.getBoolean(OIL_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "oil")) {
        return
    }

    AStages.addStageToPlayer(player, "oil")

    console.info(
        "[STAGE RECOVERY] RESTORED oil TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e기름 §f스테이지가 복구되었습니다."
    )
}


function restoreAdvancedFarming(player) {

    if (!player.persistentData.getBoolean(ADVANCED_FARMING_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "advanced_farming")) {
        return
    }

    AStages.addStageToPlayer(player, "advanced_farming")

    console.info(
        "[STAGE RECOVERY] RESTORED advanced_farming TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e고급농업 §f스테이지가 복구되었습니다."
    )
}


function restoreElectricity(player) {

    if (!player.persistentData.getBoolean(ELECTRICITY_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "electricity")) {
        return
    }

    AStages.addStageToPlayer(player, "electricity")

    console.info(
        "[STAGE RECOVERY] RESTORED electricity TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e전기 §f스테이지가 복구되었습니다."
    )
}


function restoreHypertubes(player) {

    if (!player.persistentData.getBoolean(HYPERTUBES_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "hypertubes")) {
        return
    }

    AStages.addStageToPlayer(player, "hypertubes")

    console.info(
        "[STAGE RECOVERY] RESTORED hypertubes TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e하이퍼튜브 §f스테이지가 복구되었습니다."
    )
}


function restoreEnchantmentIndustry(player) {

    if (!player.persistentData.getBoolean(ENCHANTMENT_INDUSTRY_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "enchantment_industry")) {
        return
    }

    AStages.addStageToPlayer(player, "enchantment_industry")

    console.info(
        "[STAGE RECOVERY] RESTORED enchantment_industry TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e마법_산업 §f스테이지가 복구되었습니다."
    )
}


function restoreStage6(player) {

    if (!player.persistentData.getBoolean(STAGE6_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "stage6")) {
        return
    }

    AStages.addStageToPlayer(player, "stage6")

    console.info(
        "[STAGE RECOVERY] RESTORED stage6 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e6 단계 §f스테이지가 복구되었습니다."
    )
}


function restoreItemSink(player) {

    if (!player.persistentData.getBoolean(ITEM_SINK_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "item_sink")) {
        return
    }

    AStages.addStageToPlayer(player, "item_sink")

    console.info(
        "[STAGE RECOVERY] RESTORED item_sink TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §eitem_sink §f스테이지가 복구되었습니다."
    )
}


function restorePatternSchematics(player) {

    if (!player.persistentData.getBoolean(PATTERN_SCHEMATICS_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "pattern_schematics")) {
        return
    }

    AStages.addStageToPlayer(player, "pattern_schematics")

    console.info(
        "[STAGE RECOVERY] RESTORED pattern_schematics TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e패턴_설계도 §f스테이지가 복구되었습니다."
    )
}


function restoreJetpackMk1(player) {

    if (!player.persistentData.getBoolean(JETPACK_MK1_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "jetpack_mk1")) {
        return
    }

    AStages.addStageToPlayer(player, "jetpack_mk1")

    console.info(
        "[STAGE RECOVERY] RESTORED jetpack_mk1 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §ejetpack_mk1 §f스테이지가 복구되었습니다."
    )
}


function restoreChunkLoading(player) {

    if (!player.persistentData.getBoolean(CHUNK_LOADING_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "chunk_loading")) {
        return
    }

    AStages.addStageToPlayer(player, "chunk_loading")

    console.info(
        "[STAGE RECOVERY] RESTORED chunk_loading TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e청크 로딩 §f스테이지가 복구되었습니다."
    )
}


function restoreCannons(player) {

    if (!player.persistentData.getBoolean(CANNONS_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "cannons")) {
        return
    }

    AStages.addStageToPlayer(player, "cannons")

    console.info(
        "[STAGE RECOVERY] RESTORED cannons TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e대포 §f스테이지가 복구되었습니다."
    )
}


function restoreStage7(player) {

    if (!player.persistentData.getBoolean(STAGE7_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "stage7")) {
        return
    }

    AStages.addStageToPlayer(player, "stage7")

    console.info(
        "[STAGE RECOVERY] RESTORED stage7 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e스테이지7 §f스테이지가 복구되었습니다."
    )
}


function restoreAutomatedTrading(player) {

    if (!player.persistentData.getBoolean(AUTOMATED_TRADING_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "automated_trading")) {
        return
    }

    AStages.addStageToPlayer(player, "automated_trading")

    console.info(
        "[STAGE RECOVERY] RESTORED automated_trading TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §eautomatic_trading §f스테이지가 복구되었습니다."
    )
}


function restoreRadarComponents(player) {

    if (!player.persistentData.getBoolean(RADAR_COMPONENTS_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "radar_components")) {
        return
    }

    AStages.addStageToPlayer(player, "radar_components")

    console.info(
        "[STAGE RECOVERY] RESTORED radar_components TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e레이더_구성요소 §f스테이지가 복구되었습니다."
    )
}


function restoreOpticalFabrication(player) {

    if (!player.persistentData.getBoolean(OPTICAL_FABRICATION_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "optical_fabrication")) {
        return
    }

    AStages.addStageToPlayer(player, "optical_fabrication")

    console.info(
        "[STAGE RECOVERY] RESTORED optical_fabrication TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e광학_가공 §f스테이지가 복구되었습니다."
    )
}


function restoreEngraving(player) {

    if (!player.persistentData.getBoolean(ENGRAVING_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "engraving")) {
        return
    }

    AStages.addStageToPlayer(player, "engraving")

    console.info(
        "[STAGE RECOVERY] RESTORED engraving TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e조각 §f스테이지가 복구되었습니다."
    )
}


function restoreAirshipComponents(player) {

    if (!player.persistentData.getBoolean(AIRSHIP_COMPONENTS_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "airship_components")) {
        return
    }

    AStages.addStageToPlayer(player, "airship_components")

    console.info(
        "[STAGE RECOVERY] RESTORED airship_components TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e비행선_구성요소 §f스테이지가 복구되었습니다."
    )
}


function restoreAstrophotographyGear(player) {

    if (!player.persistentData.getBoolean(ASTROPHOTOGRAPHY_GEAR_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "astrophotography_gear")) {
        return
    }

    AStages.addStageToPlayer(player, "astrophotography_gear")

    console.info(
        "[STAGE RECOVERY] RESTORED astrophotography_gear TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e천체 사진_기어 §f스테이지가 복구되었습니다."
    )
}


function restoreMobilePackages(player) {

    if (!player.persistentData.getBoolean(MOBILE_PACKAGES_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "mobile_packages")) {
        return
    }

    AStages.addStageToPlayer(player, "mobile_packages")

    console.info(
        "[STAGE RECOVERY] RESTORED mobile_packages TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §emobile_packages §f스테이지가 복구되었습니다."
    )
}


function restoreStage8(player) {

    if (!player.persistentData.getBoolean(STAGE8_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "stage8")) {
        return
    }

    AStages.addStageToPlayer(player, "stage8")

    console.info(
        "[STAGE RECOVERY] RESTORED stage8 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e스테이지 8 §f스테이지가 복구되었습니다."
    )
}


function restoreJetpackMk2(player) {

    if (!player.persistentData.getBoolean(JETPACK_MK2_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "jetpack_mk2")) {
        return
    }

    AStages.addStageToPlayer(player, "jetpack_mk2")

    console.info(
        "[STAGE RECOVERY] RESTORED jetpack_mk2 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §ejetpack_mk2 §f스테이지가 복구되었습니다."
    )
}


function restoreSpacecraftComponents(player) {

    if (!player.persistentData.getBoolean(SPACECRAFT_COMPONENTS_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "spacecraft_components")) {
        return
    }

    AStages.addStageToPlayer(player, "spacecraft_components")

    console.info(
        "[STAGE RECOVERY] RESTORED spacecraft_components TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e우주선_구성요소 §f스테이지가 복구되었습니다."
    )
}


function restoreSpaceGear(player) {

    if (!player.persistentData.getBoolean(SPACE_GEAR_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "space_gear")) {
        return
    }

    AStages.addStageToPlayer(player, "space_gear")

    console.info(
        "[STAGE RECOVERY] RESTORED space_gear TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §espace_gear §f스테이지가 복구되었습니다."
    )
}


function restoreAtmosphericMachinery(player) {

    if (!player.persistentData.getBoolean(ATMOSPHERIC_MACHINERY_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "atmospheric_machinery")) {
        return
    }

    AStages.addStageToPlayer(player, "atmospheric_machinery")

    console.info(
        "[STAGE RECOVERY] RESTORED atmospheric_machinery TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e대기_기계 §f스테이지가 복구되었습니다."
    )
}


function restoreGyroscopicComponents(player) {

    if (!player.persistentData.getBoolean(GYROSCOPIC_COMPONENTS_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "gyroscopic_components")) {
        return
    }

    AStages.addStageToPlayer(player, "gyroscopic_components")

    console.info(
        "[STAGE RECOVERY] RESTORED gyroscopic_components TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e자이로스코픽 구성요소 §f스테이지가 복구되었습니다."
    )
}


function restoreRocketPropulsion(player) {

    if (!player.persistentData.getBoolean(ROCKET_PROPULSION_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "rocket_propulsion")) {
        return
    }

    AStages.addStageToPlayer(player, "rocket_propulsion")

    console.info(
        "[STAGE RECOVERY] RESTORED rocket_propulsion TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e로켓_추진 §f스테이지가 복구되었습니다."
    )
}


function restoreStage9(player) {

    if (!player.persistentData.getBoolean(STAGE9_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "stage9")) {
        return
    }

    AStages.addStageToPlayer(player, "stage9")

    console.info(
        "[STAGE RECOVERY] RESTORED stage9 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e스테이지9 §f스테이지가 복구되었습니다."
    )
}


function restoreNuclearReactorComponents(player) {

    if (!player.persistentData.getBoolean(NUCLEAR_REACTOR_COMPONENTS_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "nuclear_reactor_components")) {
        return
    }

    AStages.addStageToPlayer(player, "nuclear_reactor_components")

    console.info(
        "[STAGE RECOVERY] RESTORED nuclear_reactor_components TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e핵_반응기_구성요소 §f스테이지가 복구되었습니다."
    )
}


function restoreAdvancedPowerGeneration(player) {

    if (!player.persistentData.getBoolean(ADVANCED_POWER_GENERATION_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "advanced_power_generation")) {
        return
    }

    AStages.addStageToPlayer(player, "advanced_power_generation")

    console.info(
        "[STAGE RECOVERY] RESTORED advanced_power_generation TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e고급 전력 생성 §f스테이지가 복구되었습니다."
    )
}


function restoreLunarSpacecraftComponents(player) {

    if (!player.persistentData.getBoolean(LUNAR_SPACECRAFT_COMPONENTS_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "lunar_spacecraft_components")) {
        return
    }

    AStages.addStageToPlayer(player, "lunar_spacecraft_components")

    console.info(
        "[STAGE RECOVERY] RESTORED lunar_spacecraft_components TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §elunar_spacecraft_composites §f스테이지가 복구되었습니다."
    )
}


function restoreLunarAtmosphericMachinery(player) {

    if (!player.persistentData.getBoolean(LUNAR_ATMOSPHERIC_MACHINERY_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "lunar_atmospheric_machinery")) {
        return
    }

    AStages.addStageToPlayer(player, "lunar_atmospheric_machinery")

    console.info(
        "[STAGE RECOVERY] RESTORED lunar_atmospheric_machinery TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §elunar_atmospheric_machinery §f스테이지가 복구되었습니다."
    )
}


function restoreMartianSpaceGear(player) {

    if (!player.persistentData.getBoolean(MARTIAN_SPACE_GEAR_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "martian_space_gear")) {
        return
    }

    AStages.addStageToPlayer(player, "martian_space_gear")

    console.info(
        "[STAGE RECOVERY] RESTORED martian_space_gear TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §emartian_space_gear §f스테이지가 복구되었습니다."
    )
}


function restoreMechanicalCompanion(player) {

    if (!player.persistentData.getBoolean(MECHANICAL_COMPANION_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "mechanical_companion")) {
        return
    }

    AStages.addStageToPlayer(player, "mechanical_companion")

    console.info(
        "[STAGE RECOVERY] RESTORED mechanical_companion TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §eMechanical_companion §f스테이지가 복구되었습니다."
    )
}


function restoreStage10(player) {

    if (!player.persistentData.getBoolean(STAGE10_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "stage10")) {
        return
    }

    AStages.addStageToPlayer(player, "stage10")

    console.info(
        "[STAGE RECOVERY] RESTORED stage10 TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e스테이지10 §f스테이지가 복구되었습니다."
    )
}


function restoreCreateQol(player) {

    if (!player.persistentData.getBoolean(CREATEQOL_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "createqol")) {
        return
    }

    AStages.addStageToPlayer(player, "createqol")

    console.info(
        "[STAGE RECOVERY] RESTORED createqol TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e창조하다 §f스테이지가 복구되었습니다."
    )
}


function restoreTeleportation(player) {

    if (!player.persistentData.getBoolean(TELEPORTATION_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "teleportation")) {
        return
    }

    AStages.addStageToPlayer(player, "teleportation")

    console.info(
        "[STAGE RECOVERY] RESTORED teleportation TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e순간이동 §f스테이지가 복구되었습니다."
    )
}


function restorePocketDimension(player) {

    if (!player.persistentData.getBoolean(POCKET_DIMENSION_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "pocket_dimension")) {
        return
    }

    AStages.addStageToPlayer(player, "pocket_dimension")

    console.info(
        "[STAGE RECOVERY] RESTORED pocket_dimension TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e주머니_치수 §f스테이지가 복구되었습니다."
    )
}


function restoreAdvancedTeleportation(player) {

    if (!player.persistentData.getBoolean(ADVANCED_TELEPORTATION_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "advanced_teleportation")) {
        return
    }

    AStages.addStageToPlayer(player, "advanced_teleportation")

    console.info(
        "[STAGE RECOVERY] RESTORED advanced_teleportation TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e고급_순간이동 §f스테이지가 복구되었습니다."
    )
}


function restoreAdvancedPropulsion(player) {

    if (!player.persistentData.getBoolean(ADVANCED_PROPULSION_DATA)) {
        return
    }

    if (AStages.playerHasStage(player, "advanced_propulsion")) {
        return
    }

    AStages.addStageToPlayer(player, "advanced_propulsion")

    console.info(
        "[STAGE RECOVERY] RESTORED advanced_propulsion TO " +
        player.username
    )

    player.tell(
        "§6§l진행 상황 복구 완료!§r\n" +
        "§f당신의 §e고급 추진 §f스테이지가 복구되었습니다."
    )
}

ServerEvents.commandRegistry(event => {

    event.register(
        event.commands.literal("stagebackup")

.then(
    event.commands.literal("copycats")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                COPYCATS_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 모방자"
            )

            restoreCopycats(player)

            return 1
        })
)

.then(
    event.commands.literal("stage1")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                STAGE1_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 스테이지 1"
            )

            restoreStage1(player)

            return 1
        })
)

.then(
    event.commands.literal("diving_equipment_mk1")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                DIVING_EQUIPMENT_MK1_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 diving_equipment_mk1"
            )

            restoreDivingEquipmentMk1(player)

            return 1
        })
)

.then(
    event.commands.literal("machines_mk1")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                MACHINES_MK1_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 machine_mk1"
            )

            restoreMachinesMk1(player)

            return 1
        })
)

.then(
    event.commands.literal("rotational_power_generation_mk1")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ROTATIONAL_POWER_GENERATION_MK1_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 회전_전력_세대_mk1"
            )

            restoreRotationalPowerGenerationMk1(player)

            return 1
        })
)

.then(
    event.commands.literal("contraptions_mk1")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                CONTRAPTIONS_MK1_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 장치_mk1"
            )

            restoreContraptionsMk1(player)

            return 1
        })
)

.then(
    event.commands.literal("rotational_power_transportation_mk1")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ROTATIONAL_POWER_TRANSPORTATION_MK1_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된rotational_power_transportation_mk1"
            )

            restoreRotationalPowerTransportationMk1(player)

            return 1
        })
)

.then(
    event.commands.literal("logistics_mk1")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                LOGISTICS_MK1_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 log_mk1"
            )

            restoreLogisticsMk1(player)

            return 1
        })
)

.then(
    event.commands.literal("stage2")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                STAGE2_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 스테이지 2"
            )

            restoreStage2(player)

            return 1
        })
)

.then(
    event.commands.literal("machines_mk2")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                MACHINES_MK2_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Machine_mk2"
            )

            restoreMachinesMk2(player)

            return 1
        })
)

.then(
    event.commands.literal("super_heating")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                SUPER_HEATING_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 과열"
            )

            restoreSuperHeating(player)

            return 1
        })
)

.then(
    event.commands.literal("blueprints_mk1")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                BLUEPRINTS_MK1_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 blueprints_mk1"
            )

            restoreBlueprintsMk1(player)

            return 1
        })
)

.then(
    event.commands.literal("fluids_mk1")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                FLUIDS_MK1_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Fluid_mk1"
            )

            restoreFluidsMk1(player)

            return 1
        })
)

.then(
    event.commands.literal("advanced_redstone_mk1")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ADVANCED_REDSTONE_MK1_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Advanced_redstone_mk1"
            )

            restoreAdvancedRedstoneMk1(player)

            return 1
        })
)

.then(
    event.commands.literal("post_production")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                POST_PRODUCTION_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 포스트 프로덕션"
            )

            restorePostProduction(player)

            return 1
        })
)

.then(
    event.commands.literal("stage3")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                STAGE3_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 stage3"
            )

            restoreStage3(player)

            return 1
        })
)

.then(
    event.commands.literal("brass_production")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                BRASS_PRODUCTION_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Brass_production"
            )

            restoreBrassProduction(player)

            return 1
        })
)

.then(
    event.commands.literal("advanced_redstone_mk2")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ADVANCED_REDSTONE_MK2_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Advanced_redstone_mk2"
            )

            restoreAdvancedRedstoneMk2(player)

            return 1
        })
)

.then(
    event.commands.literal("better_item_managment")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                BETTER_ITEM_MANAGMENT_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제 better_item_managment"
            )

            restoreBetterItemManagment(player)

            return 1
        })
)

.then(
    event.commands.literal("advanced_fluids")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ADVANCED_FLUIDS_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Advanced_fluids"
            )

            restoreAdvancedFluids(player)

            return 1
        })
)

.then(
    event.commands.literal("logistics_mk3")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                LOGISTICS_MK3_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 log_mk3"
            )

            restoreLogisticsMk3(player)

            return 1
        })
)

.then(
    event.commands.literal("moving_contraptions_mk2")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                MOVING_CONTRAPTIONS_MK2_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Moving_contraptions_mk2"
            )

            restoreMovingContraptionsMk2(player)

            return 1
        })
)

.then(
    event.commands.literal("stage4")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                STAGE4_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 stage4"
            )

            restoreStage4(player)

            return 1
        })
)

.then(
    event.commands.literal("steam_power_generation")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                STEAM_POWER_GENERATION_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 steam_power_generation"
            )

            restoreSteamPowerGeneration(player)

            return 1
        })
)

.then(
    event.commands.literal("machines_mk4")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                MACHINES_MK4_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Machine_mk4"
            )

            restoreMachinesMk4(player)

            return 1
        })
)

.then(
    event.commands.literal("trains")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                TRAINS_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 열차"
            )

            restoreTrains(player)

            return 1
        })
)

.then(
    event.commands.literal("advanced_machining")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ADVANCED_MACHINING_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Advanced_machining"
            )

            restoreAdvancedMachining(player)

            return 1
        })
)

.then(
    event.commands.literal("better_equipment")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                BETTER_EQUIPMENT_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 better_equipment"
            )

            restoreBetterEquipment(player)

            return 1
        })
)

.then(
    event.commands.literal("vehicle_components")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                VEHICLE_COMPONENTS_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 차량_구성 요소"
            )

            restoreVehicleComponents(player)

            return 1
        })
)

.then(
    event.commands.literal("economy")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ECONOMY_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 경제"
            )

            restoreEconomy(player)

            return 1
        })
)

.then(
    event.commands.literal("stage5")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                STAGE5_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 스테이지 5"
            )

            restoreStage5(player)

            return 1
        })
)

.then(
    event.commands.literal("diesel_power_generation")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                DIESEL_POWER_GENERATION_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 diesel_power_generation"
            )

            restoreDieselPowerGeneration(player)

            return 1
        })
)

.then(
    event.commands.literal("oil")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                OIL_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 오일"
            )

            restoreOil(player)

            return 1
        })
)

.then(
    event.commands.literal("advanced_farming")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ADVANCED_FARMING_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Advanced_farming"
            )

            restoreAdvancedFarming(player)

            return 1
        })
)

.then(
    event.commands.literal("electricity")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ELECTRICITY_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 전기"
            )

            restoreElectricity(player)

            return 1
        })
)

.then(
    event.commands.literal("hypertubes")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                HYPERTUBES_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 하이퍼튜브"
            )

            restoreHypertubes(player)

            return 1
        })
)

.then(
    event.commands.literal("enchantment_industry")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ENCHANTMENT_INDUSTRY_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 enchantment_industry"
            )

            restoreEnchantmentIndustry(player)

            return 1
        })
)

.then(
    event.commands.literal("stage6")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                STAGE6_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 stage6"
            )

            restoreStage6(player)

            return 1
        })
)

.then(
    event.commands.literal("item_sink")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ITEM_SINK_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 item_sink"
            )

            restoreItemSink(player)

            return 1
        })
)

.then(
    event.commands.literal("pattern_schematics")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                PATTERN_SCHEMATICS_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Pattern_schematics"
            )

            restorePatternSchematics(player)

            return 1
        })
)

.then(
    event.commands.literal("jetpack_mk1")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                JETPACK_MK1_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 jetpack_mk1"
            )

            restoreJetpackMk1(player)

            return 1
        })
)

.then(
    event.commands.literal("chunk_loading")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                CHUNK_LOADING_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Chunk_loading"
            )

            restoreChunkLoading(player)

            return 1
        })
)

.then(
    event.commands.literal("cannons")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                CANNONS_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 대포"
            )

            restoreCannons(player)

            return 1
        })
)

.then(
    event.commands.literal("stage7")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                STAGE7_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 stage7"
            )

            restoreStage7(player)

            return 1
        })
)

.then(
    event.commands.literal("automated_trading")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                AUTOMATED_TRADING_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 automatic_trading"
            )

            restoreAutomatedTrading(player)

            return 1
        })
)

.then(
    event.commands.literal("radar_components")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                RADAR_COMPONENTS_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 레이더 구성요소"
            )

            restoreRadarComponents(player)

            return 1
        })
)

.then(
    event.commands.literal("optical_fabrication")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                OPTICAL_FABRICATION_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 광학 제조"
            )

            restoreOpticalFabrication(player)

            return 1
        })
)

.then(
    event.commands.literal("engraving")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ENGRAVING_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 조각"
            )

            restoreEngraving(player)

            return 1
        })
)

.then(
    event.commands.literal("airship_components")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                AIRSHIP_COMPONENTS_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 비행선_구성요소"
            )

            restoreAirshipComponents(player)

            return 1
        })
)

.then(
    event.commands.literal("astrophotography_gear")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ASTROPHOTOGRAPHY_GEAR_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 astrophotography_gear"
            )

            restoreAstrophotographyGear(player)

            return 1
        })
)

.then(
    event.commands.literal("mobile_packages")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                MOBILE_PACKAGES_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 mobile_packages"
            )

            restoreMobilePackages(player)

            return 1
        })
)

.then(
    event.commands.literal("stage8")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                STAGE8_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 stage8"
            )

            restoreStage8(player)

            return 1
        })
)

.then(
    event.commands.literal("jetpack_mk2")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                JETPACK_MK2_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 jetpack_mk2"
            )

            restoreJetpackMk2(player)

            return 1
        })
)

.then(
    event.commands.literal("spacecraft_components")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                SPACECRAFT_COMPONENTS_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 우주선_구성요소"
            )

            restoreSpacecraftComponents(player)

            return 1
        })
)

.then(
    event.commands.literal("space_gear")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                SPACE_GEAR_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 space_gear"
            )

            restoreSpaceGear(player)

            return 1
        })
)

.then(
    event.commands.literal("atmospheric_machinery")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ATMOSPHERIC_MACHINERY_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 대기 기계"
            )

            restoreAtmosphericMachinery(player)

            return 1
        })
)

.then(
    event.commands.literal("gyroscopic_components")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                GYROSCOPIC_COMPONENTS_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 gyroscopic_comComponents"
            )

            restoreGyroscopicComponents(player)

            return 1
        })
)

.then(
    event.commands.literal("rocket_propulsion")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ROCKET_PROPULSION_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 로켓_추진 장치"
            )

            restoreRocketPropulsion(player)

            return 1
        })
)

.then(
    event.commands.literal("stage9")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                STAGE9_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 stage9"
            )

            restoreStage9(player)

            return 1
        })
)

.then(
    event.commands.literal("nuclear_reactor_components")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                NUCLEAR_REACTOR_COMPONENTS_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 핵 반응기 구성 요소"
            )

            restoreNuclearReactorComponents(player)

            return 1
        })
)

.then(
    event.commands.literal("advanced_power_generation")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ADVANCED_POWER_GENERATION_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Advanced_power_ Generation"
            )

            restoreAdvancedPowerGeneration(player)

            return 1
        })
)

.then(
    event.commands.literal("lunar_spacecraft_components")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                LUNAR_SPACECRAFT_COMPONENTS_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 lunar_spacecraft_comComponents"
            )

            restoreLunarSpacecraftComponents(player)

            return 1
        })
)

.then(
    event.commands.literal("lunar_atmospheric_machinery")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                LUNAR_ATMOSPHERIC_MACHINERY_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 lunar_atmospheric_machinery"
            )

            restoreLunarAtmosphericMachinery(player)

            return 1
        })
)

.then(
    event.commands.literal("martian_space_gear")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                MARTIAN_SPACE_GEAR_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 martian_space_gear"
            )

            restoreMartianSpaceGear(player)

            return 1
        })
)

.then(
    event.commands.literal("mechanical_companion")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                MECHANICAL_COMPANION_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Mechanical_companion"
            )

            restoreMechanicalCompanion(player)

            return 1
        })
)

.then(
    event.commands.literal("stage10")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                STAGE10_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 스테이지 10"
            )

            restoreStage10(player)

            return 1
        })
)

.then(
    event.commands.literal("createqol")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                CREATEQOL_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 createqol"
            )

            restoreCreateqol(player)

            return 1
        })
)

.then(
    event.commands.literal("teleportation")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                TELEPORTATION_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 순간이동"
            )

            restoreTeleportation(player)

            return 1
        })
)

.then(
    event.commands.literal("pocket_dimension")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                POCKET_DIMENSION_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 Pocket_dimension"
            )

            restorePocketDimension(player)

            return 1
        })
)

.then(
    event.commands.literal("advanced_teleportation")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ADVANCED_TELEPORTATION_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제됨"
            )

            restoreAdvancedTeleportation(player)

            return 1
        })
)

.then(
    event.commands.literal("advanced_propulsion")
        .executes(ctx => {

            const player = ctx.source.player

            if (!player) {
                return 0
            }

            player.persistentData.putBoolean(
                ADVANCED_PROPULSION_DATA,
                true
            )

            console.info(
                "[STAGE RECOVERY] " +
                player.username +
                " 영구적으로 잠금 해제된 고급 추진"
            )

            restoreAdvancedPropulsion(player)

            return 1
        })
)
    )
})

PlayerEvents.loggedIn(event => {

    const player = event.player

    // EXACT SAME METHOD AS THE WORKING SCRIPT
    event.server.scheduleInTicks(20, () => {

        restoreCopycats(player)
        restoreStage1(player)
        restoreDivingEquipmentMk1(player)
        restoreMachinesMk1(player)
        restoreRotationalPowerGenerationMk1(player)
        restoreContraptionsMk1(player)
        restoreRotationalPowerTransportationMk1(player)
        restoreLogisticsMk1(player)

        restoreStage2(player)
        restoreMachinesMk2(player)
        restoreSuperHeating(player)
        restoreBlueprintsMk1(player)
        restoreFluidsMk1(player)
        restoreAdvancedRedstoneMk1(player)
        restorePostProduction(player)

        restoreStage3(player)
        restoreBrassProduction(player)
        restoreAdvancedRedstoneMk2(player)
        restoreBetterItemManagment(player)
        restoreAdvancedFluids(player)
        restoreLogisticsMk3(player)
        restoreMovingContraptionsMk2(player)

        restoreStage4(player)
        restoreSteamPowerGeneration(player)
        restoreMachinesMk4(player)
        restoreTrains(player)
        restoreAdvancedMachining(player)
        restoreBetterEquipment(player)
        restoreVehicleComponents(player)
        restoreEconomy(player)

        restoreStage5(player)
        restoreDieselPowerGeneration(player)
        restoreOil(player)
        restoreAdvancedFarming(player)
        restoreElectricity(player)
        restoreHypertubes(player)
        restoreEnchantmentIndustry(player)

        restoreStage6(player)
        restoreItemSink(player)
        restorePatternSchematics(player)
        restoreJetpackMk1(player)
        restoreChunkLoading(player)
        restoreCannons(player)

        restoreStage7(player)
        restoreAutomatedTrading(player)
        restoreRadarComponents(player)
        restoreOpticalFabrication(player)
        restoreEngraving(player)
        restoreAirshipComponents(player)
        restoreAstrophotographyGear(player)
        restoreMobilePackages(player)

        restoreStage8(player)
        restoreJetpackMk2(player)
        restoreSpacecraftComponents(player)
        restoreSpaceGear(player)
        restoreAtmosphericMachinery(player)
        restoreGyroscopicComponents(player)
        restoreRocketPropulsion(player)

        restoreStage9(player)
        restoreNuclearReactorComponents(player)
        restoreAdvancedPowerGeneration(player)
        restoreLunarSpacecraftComponents(player)
        restoreLunarAtmosphericMachinery(player)
        restoreMartianSpaceGear(player)
        restoreMechanicalCompanion(player)

        restoreStage10(player)
        restoreCreateQol(player)
        restoreTeleportation(player)
        restorePocketDimension(player)
        restoreAdvancedTeleportation(player)
        restoreAdvancedPropulsion(player)

    })
})