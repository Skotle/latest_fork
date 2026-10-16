PlayerEvents.loggedIn(event => {
    const player = event.player
    
    // This checks if the player has never joined this world before
    if (!player.persistentData.contains("hasJoinedBefore")) {
        
        player.persistentData.putBoolean("hasJoinedBefore", true)
        
        player.tell([
            Component.literal("§o 마일스톤이나 아이템 제한 없이 이 팩을 경험하려면 /unlockallstages를 실행하세요(op 필요)."),
        ])
    }
})