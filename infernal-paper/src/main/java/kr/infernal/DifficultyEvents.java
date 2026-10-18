package kr.infernal;

import org.bukkit.*;
import org.bukkit.attribute.Attribute;
import org.bukkit.entity.*;
import org.bukkit.event.*;
import org.bukkit.event.entity.*;
import org.bukkit.event.player.PlayerItemDamageEvent;
import org.bukkit.potion.*;
import java.util.*;

/** Scales existing vanilla events; never adds attacks, spawns or damage ticks. */
public final class DifficultyEvents implements Listener {
    private final InfernalDifficulties plugin;
    private final Set<UUID> applyingEffect=new HashSet<>();
    private static final Set<String> NEGATIVE=Set.of("poison","wither","slowness","weakness","hunger","mining_fatigue","blindness","darkness","levitation","nausea");
    private static final Set<String> ENVIRONMENT=Set.of("CONTACT","SUFFOCATION","FALL","FIRE","FIRE_TICK","MELTING","LAVA","DROWNING","BLOCK_EXPLOSION","ENTITY_EXPLOSION","LIGHTNING","HOT_FLOOR","CRAMMING","FLY_INTO_WALL","FREEZE","FALLING_BLOCK");
    public DifficultyEvents(InfernalDifficulties plugin){this.plugin=plugin;}
    private boolean survival(Entity entity){return entity instanceof Player player&&(player.getGameMode()==GameMode.SURVIVAL||player.getGameMode()==GameMode.ADVENTURE);}
    private boolean active(Entity entity){return survival(entity)&&plugin.current(entity.getWorld()).custom();}
    private LivingEntity owner(Entity entity,int depth){
        if(entity==null||depth>4)return null;
        if(entity instanceof Projectile projectile&&projectile.getShooter() instanceof Entity shooter)return owner(shooter,depth+1);
        if(entity instanceof AreaEffectCloud cloud&&cloud.getSource() instanceof Entity source)return owner(source,depth+1);
        if(entity instanceof EvokerFangs fangs)return owner(fangs.getOwner(),depth+1);
        if(entity instanceof TNTPrimed tnt)return owner(tnt.getSource(),depth+1);
        if(entity instanceof EnderDragonPart part)return part.getParent();
        return entity instanceof LivingEntity le?le:null;
    }
    @EventHandler(priority=EventPriority.HIGH,ignoreCancelled=true) public void damage(EntityDamageEvent event){
        if(!active(event.getEntity()))return;
        var profile=plugin.profile(event.getEntity().getWorld());
        Entity causing=event.getDamageSource().getCausingEntity();
        LivingEntity attacker=owner(causing,0);
        if(attacker==null&&event instanceof EntityDamageByEntityEvent by)attacker=owner(by.getDamager(),0);
        if(attacker instanceof Player)return; // PvP damage is unchanged, including player projectiles.
        if(attacker!=null&&plugin.managedEnemy(attacker)){
            String cause=event.getCause().name();
            double factor;
            if(plugin.boss(attacker))factor=profile.value("boss-damage");
            else if(cause.equals("ENTITY_EXPLOSION")||cause.equals("BLOCK_EXPLOSION"))factor=profile.value("explosion-damage");
            else if(cause.equals("PROJECTILE"))factor=profile.value("projectile-damage");
            else if(cause.equals("MAGIC")||cause.equals("DRAGON_BREATH")||cause.equals("SONIC_BOOM"))factor=profile.value("magic-damage");
            else {
                var attack=attacker.getAttribute(Attribute.ATTACK_DAMAGE);
                boolean alreadyScaled=attack!=null&&attack.getModifier(new NamespacedKey(plugin,"attribute/attack_damage"))!=null;
                factor=alreadyScaled?1:profile.value("melee-damage");
            }
            event.setDamage(event.getDamage()*factor);
        }else if(attacker==null&&plugin.survivalScaling()&&ENVIRONMENT.contains(event.getCause().name())){
            event.setDamage(event.getDamage()*profile.value("environment-damage"));
        }
    }
    @EventHandler(priority=EventPriority.HIGH,ignoreCancelled=true) public void exhaustion(EntityExhaustionEvent event){
        if(plugin.survivalScaling()&&active(event.getEntity()))event.setExhaustion((float)(event.getExhaustion()*plugin.profile(event.getEntity().getWorld()).value("exhaustion")));
    }
    @EventHandler(priority=EventPriority.HIGH,ignoreCancelled=true) public void regain(EntityRegainHealthEvent event){
        if(plugin.survivalScaling()&&active(event.getEntity())&&event.getRegainReason()==EntityRegainHealthEvent.RegainReason.SATIATED)
            event.setAmount(event.getAmount()*plugin.profile(event.getEntity().getWorld()).value("natural-healing"));
    }
    @EventHandler(priority=EventPriority.HIGH,ignoreCancelled=true) public void durability(PlayerItemDamageEvent event){
        if(!plugin.survivalScaling()||!active(event.getPlayer())||event.getDamage()<=0)return;
        // Fractional wear is carried per player, avoiding rounding every one-point hit up to two.
        var data=event.getPlayer().getPersistentDataContainer();var key=new NamespacedKey(plugin,"wear_fraction");
        double carry=data.getOrDefault(key,org.bukkit.persistence.PersistentDataType.DOUBLE,0d);
        double scaled=event.getDamage()*plugin.profile(event.getPlayer().getWorld()).value("durability")+carry;
        double integral=Math.floor(scaled+1e-9);
        int whole=(int)Math.min(Integer.MAX_VALUE,integral);
        data.set(key,org.bukkit.persistence.PersistentDataType.DOUBLE,Math.max(0,scaled-integral));
        event.setDamage(whole);
    }
    @EventHandler(priority=EventPriority.HIGH,ignoreCancelled=true) public void effect(EntityPotionEffectEvent event){
        if(!active(event.getEntity())||applyingEffect.contains(event.getEntity().getUniqueId()))return;
        PotionEffect effect=event.getNewEffect();
        LivingEntity source=owner(event.getSource(),0);
        if(effect==null||effect.getDuration()<=0||!NEGATIVE.contains(effect.getType().getKey().getKey())||source==null||!plugin.managedEnemy(source))return;
        if(event.getOldEffect()!=null&&!event.isOverride())return;
        int duration=(int)Math.min(Integer.MAX_VALUE,Math.round(effect.getDuration()*plugin.profile(event.getEntity().getWorld()).value("status-duration")));
        if(duration==effect.getDuration())return;
        // Replace the same vanilla effect at the same amplifier; the guard prevents recursive scaling.
        event.setCancelled(true);
        applyingEffect.add(event.getEntity().getUniqueId());
        try{event.getEntity().addPotionEffect(new PotionEffect(effect.getType(),duration,effect.getAmplifier(),effect.isAmbient(),effect.hasParticles(),effect.hasIcon()));}
        finally{applyingEffect.remove(event.getEntity().getUniqueId());}
    }
    @EventHandler(priority=EventPriority.HIGH,ignoreCancelled=true) public void burn(EntityCombustByEntityEvent event){
        LivingEntity source=owner(event.getCombuster(),0);
        if(active(event.getEntity())&&source!=null&&plugin.managedEnemy(source))event.setDuration((float)(event.getDuration()*plugin.profile(event.getEntity().getWorld()).value("status-duration")));
    }
    @EventHandler(priority=EventPriority.HIGH,ignoreCancelled=true) public void prime(ExplosionPrimeEvent event){
        LivingEntity source=owner(event.getEntity(),0);
        if(source==null||source instanceof Creeper||!plugin.managedEnemy(source)||!plugin.current(source.getWorld()).custom())return;
        event.setRadius((float)(event.getRadius()*plugin.profile(source.getWorld()).value("explosion-radius")));
    }
}
