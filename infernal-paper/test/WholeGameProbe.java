package kr.infernal.test;

import kr.infernal.*;
import org.bukkit.*;
import org.bukkit.attribute.Attribute;
import org.bukkit.damage.*;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.entity.*;
import org.bukkit.event.entity.*;
import org.bukkit.event.player.PlayerItemDamageEvent;
import org.bukkit.inventory.*;
import org.bukkit.persistence.*;
import org.bukkit.potion.*;
import java.lang.reflect.*;
import java.util.*;

/** Real world/entity integration plus isolated player-event fixtures inside the running Paper server. */
final class WholeGameProbe {
    static void run(InfernalProbe test){
        test.command("difficulty hard");
        World world=test.world;
        int cap=world.getSpawnLimit(SpawnCategory.MONSTER);
        long ticks=world.getTicksPerSpawns(SpawnCategory.MONSTER);
        int sleep=world.getGameRuleValue(GameRules.PLAYERS_SLEEPING_PERCENTAGE);
        DifficultyEvents handlers=new DifficultyEvents(test.target);
        ArmorStand state=world.spawn(new Location(world,20,100,0),ArmorStand.class);
        PotionEffect[] applied={null};GameMode[] mode={GameMode.SURVIVAL};
        UUID uuid=UUID.randomUUID();
        Player player=(Player)Proxy.newProxyInstance(WholeGameProbe.class.getClassLoader(),new Class[]{Player.class},(proxy,method,args)->{
            return switch(method.getName()){
                case "getWorld"->world;
                case "getGameMode"->mode[0];
                case "getUniqueId"->uuid;
                case "getType"->EntityType.PLAYER;
                case "getName"->"SurvivalEventFixture";
                case "getLocation"->new Location(world,20,100,0);
                case "getPersistentDataContainer"->state.getPersistentDataContainer();
                case "getServer"->test.getServer();
                case "addPotionEffect"->{applied[0]=(PotionEffect)args[0];yield true;}
                case "isDead"->false;
                case "isValid","isOnline"->true;
                case "toString"->"SurvivalEventFixture";
                case "hashCode"->uuid.hashCode();
                case "equals"->proxy==args[0];
                default->throw new UnsupportedOperationException("Unimplemented player fixture method: "+method.getName());
            };
        });
        DamageSource generic=DamageSource.builder(DamageType.GENERIC).build();
        for(var preset:InfernalDifficulties.Preset.values()){
            test.command("difficulty "+preset.name().toLowerCase(Locale.ROOT));
            var p=test.target.profile(world);
            double hunger=preset.custom()?p.value("exhaustion"):1;
            var exhaustion=new EntityExhaustionEvent(player,EntityExhaustionEvent.ExhaustionReason.SPRINT,4f);
            handlers.exhaustion(exhaustion);test.near(exhaustion.getExhaustion(),4*hunger,"exhaustion "+preset);
            var healing=new EntityRegainHealthEvent(player,4,EntityRegainHealthEvent.RegainReason.SATIATED);
            handlers.regain(healing);test.near(healing.getAmount(),4*(preset.custom()?p.value("natural-healing"):1),"natural healing "+preset);
            var potionHealing=new EntityRegainHealthEvent(player,4,EntityRegainHealthEvent.RegainReason.MAGIC);
            handlers.regain(potionHealing);test.near(potionHealing.getAmount(),4,"potion healing preserved "+preset);
            var fall=new EntityDamageEvent(player,EntityDamageEvent.DamageCause.FALL,generic,10);
            handlers.damage(fall);test.near(fall.getDamage(),10*(preset.custom()?p.value("environment-damage"):1),"environment damage "+preset);
            var voidDamage=new EntityDamageEvent(player,EntityDamageEvent.DamageCause.VOID,generic,4);
            handlers.damage(voidDamage);test.near(voidDamage.getDamage(),4,"void unchanged "+preset);
            state.getPersistentDataContainer().remove(new NamespacedKey(test.target,"wear_fraction"));
            int wear=0;
            for(int n=0;n<20;n++){
                var event=new PlayerItemDamageEvent(player,new ItemStack(Material.IRON_PICKAXE),1);handlers.durability(event);wear+=event.getDamage();
            }
            test.near(wear,Math.floor(20*(preset.custom()?p.value("durability"):1)+.00001),"fractional durability "+preset);
            if(preset.custom()){
                test.check(world.getSpawnLimit(SpawnCategory.MONSTER)==(int)Math.ceil(cap*p.value("spawn-cap")),"spawn cap "+preset);
                test.check(world.getTicksPerSpawns(SpawnCategory.MONSTER)==(ticks==0?0:Math.max(1,(int)Math.floor(ticks/p.value("spawn-rate")))),"spawn interval "+preset);
                test.check(world.getGameRuleValue(GameRules.PLAYERS_SLEEPING_PERCENTAGE)==Math.max(sleep,p.integer("sleep-percentage")),"sleep rule "+preset);
            }else{
                test.check(world.getSpawnLimit(SpawnCategory.MONSTER)==cap,"native spawn cap "+preset);
                test.check(world.getGameRuleValue(GameRules.PLAYERS_SLEEPING_PERCENTAGE)==sleep,"native sleep rule "+preset);
            }
        }
        test.command("difficulty nightmare");
        var p=test.target.profile(world);
        Skeleton skeleton=world.spawn(new Location(world,22,100,0),Skeleton.class,e->e.setAI(false));
        Zombie zombie=world.spawn(new Location(world,24,100,0),Zombie.class,e->e.setAI(false));
        Creeper creeper=world.spawn(new Location(world,26,100,0),Creeper.class,e->e.setAI(false));
        Witch witch=world.spawn(new Location(world,28,100,0),Witch.class,e->e.setAI(false));
        Warden warden=world.spawn(new Location(world,30,100,0),Warden.class,e->e.setAI(false));
        for(LivingEntity e:List.of(skeleton,zombie,creeper,witch,warden))test.target.reconcile(e);
        var arrow=world.spawnArrow(new Location(world,22,100,0),new org.bukkit.util.Vector(0,0,1),1,0);arrow.setShooter(skeleton);
        DamageSource arrowSource=DamageSource.builder(DamageType.ARROW).withCausingEntity(skeleton).withDirectEntity(arrow).build();
        var ranged=new EntityDamageByEntityEvent(arrow,player,EntityDamageEvent.DamageCause.PROJECTILE,arrowSource,10);
        handlers.damage(ranged);test.near(ranged.getDamage(),10*p.value("projectile-damage"),"hostile arrows scale once");
        var melee=new EntityDamageByEntityEvent(zombie,player,EntityDamageEvent.DamageCause.ENTITY_ATTACK,DamageSource.builder(DamageType.MOB_ATTACK).withCausingEntity(zombie).withDirectEntity(zombie).build(),10);
        handlers.damage(melee);test.near(melee.getDamage(),10,"attribute-scaled melee not doubled");
        var magic=new EntityDamageByEntityEvent(witch,player,EntityDamageEvent.DamageCause.MAGIC,DamageSource.builder(DamageType.INDIRECT_MAGIC).withCausingEntity(witch).withDirectEntity(witch).build(),10);
        handlers.damage(magic);test.near(magic.getDamage(),10*p.value("magic-damage"),"hostile magic scales");
        var blast=new EntityDamageByEntityEvent(creeper,player,EntityDamageEvent.DamageCause.ENTITY_EXPLOSION,DamageSource.builder(DamageType.EXPLOSION).withCausingEntity(creeper).withDirectEntity(creeper).build(),10);
        handlers.damage(blast);test.near(blast.getDamage(),10*p.value("explosion-damage"),"hostile blast scales");
        creeper.addScoreboardTag("infernal.exclude");
        var excludedBlast=new EntityDamageByEntityEvent(creeper,player,EntityDamageEvent.DamageCause.ENTITY_EXPLOSION,DamageSource.builder(DamageType.EXPLOSION).withCausingEntity(creeper).withDirectEntity(creeper).build(),10);
        handlers.damage(excludedBlast);test.near(excludedBlast.getDamage(),10,"excluded mob explosion not treated as environment");
        creeper.removeScoreboardTag("infernal.exclude");
        test.check(creeper.getExplosionRadius()==4,"creeper radius enlarged");test.target.restore(creeper);test.check(creeper.getExplosionRadius()==3,"creeper radius restored");
        var sonic=new EntityDamageByEntityEvent(warden,player,EntityDamageEvent.DamageCause.SONIC_BOOM,DamageSource.builder(DamageType.SONIC_BOOM).withCausingEntity(warden).withDirectEntity(warden).build(),10);
        handlers.damage(sonic);test.near(sonic.getDamage(),10*p.value("boss-damage"),"warden sonic damage scales");
        var pvp=new EntityDamageByEntityEvent(player,player,EntityDamageEvent.DamageCause.ENTITY_ATTACK,generic,10);
        handlers.damage(pvp);test.near(pvp.getDamage(),10,"PvP unchanged");
        applied[0]=null;
        var poison=new EntityPotionEffectEvent(player,null,new PotionEffect(PotionEffectType.POISON,80,0),witch,EntityPotionEffectEvent.Cause.ATTACK,EntityPotionEffectEvent.Action.ADDED,true);
        handlers.effect(poison);test.check(poison.isCancelled()&&applied[0]!=null&&applied[0].getDuration()==140&&applied[0].getAmplifier()==0,"hostile poison duration scales without new amplifier");
        var food=new EntityPotionEffectEvent(player,null,new PotionEffect(PotionEffectType.HUNGER,80,0),null,EntityPotionEffectEvent.Cause.FOOD,EntityPotionEffectEvent.Action.ADDED,true);
        handlers.effect(food);test.check(!food.isCancelled(),"food effects unchanged");
        mode[0]=GameMode.CREATIVE;
        var creative=new EntityExhaustionEvent(player,EntityExhaustionEvent.ExhaustionReason.SPRINT,4);handlers.exhaustion(creative);test.near(creative.getExhaustion(),4,"creative player untouched");
        mode[0]=GameMode.SURVIVAL;
        var cancelled=new EntityExhaustionEvent(player,EntityExhaustionEvent.ExhaustionReason.SPRINT,4);cancelled.setCancelled(true);
        // Real event dispatch honors ignoreCancelled, unlike a direct formula invocation.
        test.getServer().getPluginManager().callEvent(cancelled);test.near(cancelled.getExhaustion(),4,"cancelled events untouched");
        for(Entity e:List.of(skeleton,zombie,creeper,witch,warden,arrow,state))e.remove();
        test.command("difficulty hard");
        test.check(world.getSpawnLimit(SpawnCategory.MONSTER)==cap&&world.getTicksPerSpawns(SpawnCategory.MONSTER)==ticks&&world.getGameRuleValue(GameRules.PLAYERS_SLEEPING_PERCENTAGE)==sleep,"all modified world rules restored");
        equipmentRoles(test);
    }
    private static void equipmentRoles(InfernalProbe test){
        test.command("difficulty nightmare");World world=test.world;
        for(EntityType type:List.of(EntityType.WITHER_SKELETON,EntityType.PIGLIN,EntityType.PIGLIN_BRUTE,EntityType.ZOMBIFIED_PIGLIN,EntityType.PILLAGER,EntityType.VINDICATOR)){
            LivingEntity mob=(LivingEntity)world.spawnEntity(new Location(world,20,100,2),type);mob.setAI(false);
            EntityEquipment eq=mob.getEquipment();eq.clear();
            boolean crossbow=type==EntityType.PILLAGER||type==EntityType.PIGLIN;
            eq.setItemInMainHand(new ItemStack(crossbow?Material.CROSSBOW:type==EntityType.PIGLIN_BRUTE||type==EntityType.VINDICATOR?Material.IRON_AXE:Material.STONE_SWORD));
            test.target.reconcile(mob);
            ItemStack hand=eq.getItemInMainHand();
            if(crossbow)test.check(hand.getType()==Material.CROSSBOW&&hand.getEnchantmentLevel(Enchantment.QUICK_CHARGE)==3&&hand.getEnchantmentLevel(Enchantment.PIERCING)==4,"native crossbow role "+type);
            else test.check((hand.getType().name().startsWith("DIAMOND_")||hand.getType().name().startsWith("NETHERITE_"))&&hand.getEnchantmentLevel(Enchantment.SHARPNESS)==5,"native melee weapon upgrade "+type);
            if(type==EntityType.PILLAGER||type==EntityType.VINDICATOR)test.check(Arrays.stream(eq.getArmorContents()).allMatch(ItemStack::isEmpty),"no invisible illager armor "+type);
            else test.check(Arrays.stream(eq.getArmorContents()).allMatch(i->!i.isEmpty()),"full armor for humanoid "+type);
            test.target.restore(mob);test.check(eq.getItemInMainHand().getType()==(crossbow?Material.CROSSBOW:type==EntityType.PIGLIN_BRUTE||type==EntityType.VINDICATOR?Material.IRON_AXE:Material.STONE_SWORD),"native weapon restored "+type);
            mob.remove();
        }
    }
}
