package kr.infernal;

import org.bukkit.*;
import org.bukkit.entity.SpawnCategory;
import org.bukkit.persistence.PersistentDataType;

/** Owns only monster spawn settings and the sleeping percentage; snapshots live with the world. */
final class DifficultyWorldRules {
    private final InfernalDifficulties plugin;
    DifficultyWorldRules(InfernalDifficulties plugin){this.plugin=plugin;}
    private NamespacedKey key(String path){return new NamespacedKey(plugin,"world_"+path);}
    void apply(World world){
        if(!plugin.survivalScaling()||!plugin.current(world).custom()){restore(world);return;}
        var p=plugin.profile(world);var data=world.getPersistentDataContainer();
        if(!data.has(key("spawn_limit"))){
            data.set(key("spawn_limit"),PersistentDataType.INTEGER,world.getSpawnLimit(SpawnCategory.MONSTER));
            data.set(key("spawn_ticks"),PersistentDataType.LONG,world.getTicksPerSpawns(SpawnCategory.MONSTER));
            data.set(key("sleep"),PersistentDataType.INTEGER,world.getGameRuleValue(GameRules.PLAYERS_SLEEPING_PERCENTAGE));
        }
        int limit=data.get(key("spawn_limit"),PersistentDataType.INTEGER);
        long ticks=data.get(key("spawn_ticks"),PersistentDataType.LONG);
        int originalSleep=data.get(key("sleep"),PersistentDataType.INTEGER);
        int effective=limit<0?plugin.getServer().getSpawnLimit(SpawnCategory.MONSTER):limit;
        long effectiveTicks=ticks<0?plugin.getServer().getTicksPerSpawns(SpawnCategory.MONSTER):ticks;
        world.setSpawnLimit(SpawnCategory.MONSTER,effective==0?0:(int)Math.ceil(effective*p.value("spawn-cap")));
        world.setTicksPerSpawns(SpawnCategory.MONSTER,effectiveTicks==0?0:Math.max(1,(int)Math.floor(effectiveTicks/p.value("spawn-rate"))));
        world.setGameRule(GameRules.PLAYERS_SLEEPING_PERCENTAGE,Math.max(originalSleep,p.integer("sleep-percentage")));
    }
    void restore(World world){
        var data=world.getPersistentDataContainer();
        Integer limit=data.get(key("spawn_limit"),PersistentDataType.INTEGER);
        if(limit==null)return;
        Long ticks=data.get(key("spawn_ticks"),PersistentDataType.LONG);
        Integer sleep=data.get(key("sleep"),PersistentDataType.INTEGER);
        world.setSpawnLimit(SpawnCategory.MONSTER,limit);
        if(ticks!=null)world.setTicksPerSpawns(SpawnCategory.MONSTER,Math.toIntExact(ticks));
        if(sleep!=null)world.setGameRule(GameRules.PLAYERS_SLEEPING_PERCENTAGE,sleep);
        for(String path:new String[]{"spawn_limit","spawn_ticks","sleep"})data.remove(key(path));
    }
}
