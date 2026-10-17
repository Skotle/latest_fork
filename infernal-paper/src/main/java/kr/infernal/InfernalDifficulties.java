package kr.infernal;

import com.destroystokyo.paper.event.entity.EntityAddToWorldEvent;
import io.papermc.paper.command.brigadier.Commands;
import io.papermc.paper.plugin.lifecycle.event.types.LifecycleEvents;
import io.papermc.paper.event.world.WorldDifficultyChangeEvent;
import org.bukkit.*;
import org.bukkit.attribute.*;
import org.bukkit.command.CommandSender;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.entity.*;
import org.bukkit.event.*;
import org.bukkit.event.entity.*;
import org.bukkit.event.world.WorldLoadEvent;
import org.bukkit.inventory.*;
import org.bukkit.persistence.*;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

/** Standalone Paper API implementation. No NMS, datapack or external plugin dependency. */
public final class InfernalDifficulties extends JavaPlugin implements Listener {
    public enum Preset {
        PEACEFUL, EASY, NORMAL, HARD,
        HARDER(1.2,1.15,1,1.1,10,5,0,1,0,30),
        INSANE(1.4,1.3,1.03,1.2,20,10,10,2,1,30),
        DEMON(1.6,1.5,1.05,1.3,30,15,20,3,2,25),
        NIGHTMARE(2,1.8,1.1,1.5,50,35,40,4,3,20);
        final double hp,attack,speed,follow;
        final int armor,weapon,bow,parts,enchant,fuse;
        Preset(){this(1,1,1,1,0,0,0,0,0,30);}
        Preset(double h,double a,double s,double f,int ar,int w,int b,int p,int e,int fu){
            hp=h;attack=a;speed=s;follow=f;armor=ar;weapon=w;bow=b;parts=p;enchant=e;fuse=fu;
        }
        public boolean custom(){return ordinal()>3;}
        public Difficulty base(){return Difficulty.values()[Math.min(ordinal(),3)];}
    }
    private static final Set<String> MELEE=Set.of(("ZOMBIE HUSK DROWNED ZOMBIE_VILLAGER ZOMBIFIED_PIGLIN PIGLIN PIGLIN_BRUTE WITHER_SKELETON SPIDER CAVE_SPIDER SILVERFISH ENDERMITE ENDERMAN HOGLIN ZOGLIN VINDICATOR VEX RAVAGER").split(" "));
    private static final Set<String> OTHER=Set.of(("SKELETON STRAY BOGGED PILLAGER EVOKER WITCH CREEPER BLAZE GHAST PHANTOM GUARDIAN SHULKER BREEZE SLIME MAGMA_CUBE").split(" "));
    private static final Set<String> ARMOR=Set.of("ZOMBIE","HUSK","DROWNED","ZOMBIE_VILLAGER","SKELETON","STRAY","BOGGED");
    private static final Set<String> ZOMBIES=Set.of("ZOMBIE","HUSK","DROWNED","ZOMBIE_VILLAGER");
    private static final Set<String> ARCHERS=Set.of("SKELETON","STRAY","BOGGED");
    private static final Set<String> BOSSES=Set.of("ENDER_DRAGON","WITHER","ELDER_GUARDIAN");
    private static final EquipmentSlot[] SLOTS={EquipmentSlot.FEET,EquipmentSlot.LEGS,EquipmentSlot.CHEST,EquipmentSlot.HEAD,EquipmentSlot.HAND};
    private static final Map<EquipmentSlot,String> PIECES=Map.of(EquipmentSlot.FEET,"BOOTS",EquipmentSlot.LEGS,"LEGGINGS",EquipmentSlot.CHEST,"CHESTPLATE",EquipmentSlot.HEAD,"HELMET");
    private static final Attribute[] ATTRS={Attribute.MAX_HEALTH,Attribute.ATTACK_DAMAGE,Attribute.MOVEMENT_SPEED,Attribute.FOLLOW_RANGE};
    private Preset selected;
    private boolean settingWorlds;
    private final Set<UUID> pending=new HashSet<>();
    private NamespacedKey key(String path){return new NamespacedKey(this,path);}
    private NamespacedKey modifier(Attribute a){return key("attribute/"+a.getKey().getKey());}
    private NamespacedKey slotKey(String prefix,EquipmentSlot s){return key(prefix+"_"+s.name().toLowerCase(Locale.ROOT));}
    private String fingerprint(){return selected!=null&&selected.custom()?"v1:"+selected.name():"native";}

    @Override public void onEnable(){
        saveDefaultConfig();
        String preset=getConfig().getString("preset","auto");
        if(!preset.equalsIgnoreCase("auto")){
            try{selected=Preset.valueOf(preset.toUpperCase(Locale.ROOT));}
            catch(IllegalArgumentException ex){getLogger().warning("Invalid preset: "+preset+"; preserving native world difficulties.");}
        }
        getServer().getPluginManager().registerEvents(this,this);
        getLifecycleManager().registerEventHandler(LifecycleEvents.COMMANDS,event->{
            var root=Commands.literal("difficulty")
                .requires(s->s.getSender().hasPermission("minecraft.command.difficulty")||s.getSender().hasPermission("infernal.admin"))
                .executes(c->{
                    Preset p=current(c.getSource().getLocation().getWorld());
                    c.getSource().getSender().sendMessage("난이도: "+p.name().toLowerCase(Locale.ROOT));return p.ordinal();
                });
            for(Preset p:Preset.values())root.then(Commands.literal(p.name().toLowerCase(Locale.ROOT)).executes(c->select(p,c.getSource().getSender())));
            event.registrar().register(root.build(),"바닐라 및 Infernal 난이도 8단계 선택",List.of());
        });
        if(selected!=null)applyWorldDifficulties();
        getServer().getScheduler().runTask(this,()->getServer().getWorlds().forEach(w->w.getLivingEntities().forEach(this::reconcile)));
        getLogger().info("Standalone presets enabled. /difficulty peaceful|easy|normal|hard|harder|insane|demon|nightmare");
    }
    @Override public void onDisable(){
        // Keep the same rolls and restoration data across restarts and chunk unloads.
        // To remove the plugin, first select hard and load the chunks to restore.
        pending.clear();
    }
    public Preset current(World world){return selected!=null?selected:Preset.values()[world.getDifficulty().ordinal()];}
    public int select(Preset preset,CommandSender sender){
        if(selected==preset){sender.sendMessage("난이도가 이미 "+preset.name().toLowerCase(Locale.ROOT)+"입니다.");return 0;}
        selected=preset;
        getConfig().set("preset",preset.name().toLowerCase(Locale.ROOT));saveConfig();
        applyWorldDifficulties();
        getServer().getWorlds().forEach(w->w.getLivingEntities().forEach(this::reconcile));
        sender.sendMessage("난이도를 "+preset.name().toLowerCase(Locale.ROOT)+"(으)로 설정했습니다.");
        return preset.ordinal();
    }
    private void applyWorldDifficulties(){
        settingWorlds=true;
        try{for(World w:getServer().getWorlds())w.setDifficulty(selected.base());}
        finally{settingWorlds=false;}
    }
    @EventHandler public void worldLoad(WorldLoadEvent e){if(selected!=null){settingWorlds=true;try{e.getWorld().setDifficulty(selected.base());}finally{settingWorlds=false;}}}
    @EventHandler(priority=EventPriority.MONITOR) public void externalDifficulty(WorldDifficultyChangeEvent e){
        if(settingWorlds||selected==null||e.getDifficulty()==selected.base())return;
        // Honor changes made through minecraft:difficulty or another plugin rather than silently undoing them.
        Preset target=Preset.values()[e.getDifficulty().ordinal()];
        getServer().getScheduler().runTask(this,()->select(target,getServer().getConsoleSender()));
    }
    @EventHandler(priority=EventPriority.MONITOR,ignoreCancelled=true) public void spawned(CreatureSpawnEvent e){queue(e.getEntity());}
    @EventHandler(priority=EventPriority.MONITOR) public void added(EntityAddToWorldEvent e){if(e.getEntity() instanceof LivingEntity le)queue(le);}
    @EventHandler(priority=EventPriority.MONITOR,ignoreCancelled=true) public void transformed(EntityTransformEvent e){e.getTransformedEntities().forEach(x->{if(x instanceof LivingEntity le)queue(le);});}
    private void queue(LivingEntity e){
        if(!eligible(e)&&!marked(e))return;
        if(!pending.add(e.getUniqueId()))return;
        getServer().getScheduler().runTask(this,()->{pending.remove(e.getUniqueId());if(e.isValid()&&!e.isDead())reconcile(e);});
    }
    private boolean marked(LivingEntity e){return e.getPersistentDataContainer().has(key("preset"));}
    private boolean eligible(LivingEntity e){String t=e.getType().name();return MELEE.contains(t)||OTHER.contains(t)||BOSSES.contains(t);}
    private boolean excluded(LivingEntity e){
        return e.getScoreboardTags().contains("infernal.exclude")||e.getScoreboardTags().contains("inf.active")||e.getPersistentDataContainer().getOrDefault(key("exclude"),PersistentDataType.BYTE,(byte)0)!=0;
    }
    public void reconcile(LivingEntity e){
        if(e.isDead()||e.getHealth()<=0)return;
        var data=e.getPersistentDataContainer();
        String old=data.get(key("preset"),PersistentDataType.STRING);
        boolean active=selected!=null&&selected.custom()&&eligible(e)&&!excluded(e);
        boolean needsHealthModifier=!BOSSES.contains(e.getType().name())||selected==Preset.NIGHTMARE;
        var health=e.getAttribute(Attribute.MAX_HEALTH);
        if(active&&fingerprint().equals(old)&&(!needsHealthModifier||health!=null&&health.getModifier(modifier(Attribute.MAX_HEALTH))!=null))return;
        if(old!=null)restore(e);
        if(!active)return;
        double ratio=healthRatio(e);
        String type=e.getType().name();
        if(BOSSES.contains(type)){
            if(selected==Preset.NIGHTMARE)scale(e,Attribute.MAX_HEALTH,1.5);
        }else{
            scale(e,Attribute.MAX_HEALTH,selected.hp);
            if(MELEE.contains(type)){
                scale(e,Attribute.ATTACK_DAMAGE,selected.attack);
                if(!(e instanceof Ageable age&&!age.isAdult()))scale(e,Attribute.MOVEMENT_SPEED,selected.speed);
            }
            scale(e,Attribute.FOLLOW_RANGE,selected.follow);
            var range=e.getAttribute(Attribute.FOLLOW_RANGE);
            if(range!=null&&range.getValue()>64){
                remove(e,Attribute.FOLLOW_RANGE);
                // Solve a total multiplier for the existing value; preserve other plugins' modifiers.
                double current=range.getValue();
                if(current>0)range.addModifier(new AttributeModifier(modifier(Attribute.FOLLOW_RANGE),64/current-1,AttributeModifier.Operation.MULTIPLY_SCALAR_1));
            }
            if(e instanceof Creeper creeper){data.set(key("fuse"),PersistentDataType.INTEGER,creeper.getMaxFuseTicks());creeper.setMaxFuseTicks(selected.fuse);}
            if(ARMOR.contains(type))equip(e);
        }
        data.set(key("preset"),PersistentDataType.STRING,fingerprint());
        setHealthRatio(e,ratio);
    }
    private double healthRatio(LivingEntity e){var a=e.getAttribute(Attribute.MAX_HEALTH);return a==null||a.getValue()<=0?1:Math.min(1,e.getHealth()/a.getValue());}
    private void setHealthRatio(LivingEntity e,double ratio){var a=e.getAttribute(Attribute.MAX_HEALTH);if(a!=null&&!e.isDead()&&ratio>0)e.setHealth(Math.min(a.getValue(),Math.max(.001,a.getValue()*ratio)));}
    private void scale(LivingEntity e,Attribute a,double factor){var instance=e.getAttribute(a);if(instance!=null&&factor!=1)instance.addModifier(new AttributeModifier(modifier(a),factor-1,AttributeModifier.Operation.MULTIPLY_SCALAR_1));}
    private void remove(LivingEntity e,Attribute a){var instance=e.getAttribute(a);if(instance!=null){var m=instance.getModifier(modifier(a));if(m!=null)instance.removeModifier(m);}}
    public void restore(LivingEntity e){
        double ratio=healthRatio(e);
        for(Attribute a:ATTRS)remove(e,a);
        var data=e.getPersistentDataContainer();
        Integer fuse=data.get(key("fuse"),PersistentDataType.INTEGER);
        if(fuse!=null&&e instanceof Creeper c)c.setMaxFuseTicks(fuse);
        data.remove(key("fuse"));
        EntityEquipment equipment=e.getEquipment();
        if(equipment!=null)for(EquipmentSlot s:SLOTS){
            byte[] original=data.get(slotKey("original",s),PersistentDataType.BYTE_ARRAY);
            byte[] applied=data.get(slotKey("applied",s),PersistentDataType.BYTE_ARRAY);
            if(original!=null&&applied!=null){
                // Do not overwrite gear subsequently replaced by pickups or another plugin.
                ItemStack current=equipment.getItem(s);
                boolean owned=current.getPersistentDataContainer().has(key("issued"));
                if(owned)
                    equipment.setItem(s,original.length==0?null:ItemStack.deserializeBytes(original));
                Float chance=data.get(slotKey("drop",s),PersistentDataType.FLOAT);
                if(chance!=null&&(owned||current.isEmpty()&&equipment.getDropChance(s)==0))equipment.setDropChance(s,chance);
            }
            data.remove(slotKey("original",s));data.remove(slotKey("applied",s));data.remove(slotKey("drop",s));
        }
        data.remove(key("preset"));
        setHealthRatio(e,ratio);
    }
    private boolean chance(int percent){return percent>0&&ThreadLocalRandom.current().nextInt(100)<percent;}
    private void equip(LivingEntity e){
        EntityEquipment eq=e.getEquipment();if(eq==null)return;
        if(chance(selected.armor)){
            List<EquipmentSlot> slots=new ArrayList<>(List.of(EquipmentSlot.FEET,EquipmentSlot.LEGS,EquipmentSlot.CHEST,EquipmentSlot.HEAD));
            Collections.shuffle(slots);
            int min=selected.ordinal()>=6?2:1;
            int count=ThreadLocalRandom.current().nextInt(min,selected.parts+1);
            for(int i=0;i<count;i++){
                EquipmentSlot s=slots.get(i);if(!eq.getItem(s).isEmpty())continue;
                String material=switch(selected){
                    case HARDER->chance(50)?"LEATHER":"CHAINMAIL";
                    case INSANE->chance(75)?"CHAINMAIL":"IRON";
                    case DEMON->chance(40)?"CHAINMAIL":"IRON";
                    default->"IRON";
                };
                ItemStack item=new ItemStack(Material.valueOf(material+"_"+PIECES.get(s)));
                if(selected.enchant>0&&chance(40))item.addEnchantment(Enchantment.PROTECTION,selected.enchant);
                if(selected==Preset.NIGHTMARE&&s==EquipmentSlot.CHEST&&chance(5)){
                    item=new ItemStack(Material.DIAMOND_CHESTPLATE);item.addEnchantment(Enchantment.PROTECTION,2);
                }
                give(e,s,item);
            }
        }
        String type=e.getType().name();
        if(ZOMBIES.contains(type)&&eq.getItemInMainHand().isEmpty()&&chance(selected.weapon)){
            Material material=selected==Preset.HARDER?Material.IRON_SHOVEL:Material.IRON_SWORD;
            if(selected==Preset.NIGHTMARE&&chance(5))material=Material.DIAMOND_SWORD;
            ItemStack item=new ItemStack(material);
            if(selected==Preset.DEMON)item.addEnchantment(Enchantment.SHARPNESS,1);
            if(selected==Preset.NIGHTMARE)item.addEnchantment(Enchantment.SHARPNESS,2);
            give(e,EquipmentSlot.HAND,item);
        }
        if(ARCHERS.contains(type)&&chance(selected.bow)){
            ItemStack existing=eq.getItemInMainHand();
            if(existing.getType()==Material.BOW&&existing.getEnchantments().isEmpty()){
                ItemStack bow=existing.clone();bow.addEnchantment(Enchantment.POWER,selected.enchant);
                give(e,EquipmentSlot.HAND,bow);
            }
        }
    }
    void give(LivingEntity e,EquipmentSlot s,ItemStack item){
        var eq=e.getEquipment();if(eq==null)return;
        var data=e.getPersistentDataContainer();
        if(!data.has(slotKey("original",s))){
            ItemStack original=eq.getItem(s);
            data.set(slotKey("original",s),PersistentDataType.BYTE_ARRAY,original.isEmpty()?new byte[0]:original.serializeAsBytes());
            data.set(slotKey("drop",s),PersistentDataType.FLOAT,eq.getDropChance(s));
        }
        item=item.clone();
        // Invisible ownership metadata, with no custom item behavior or visual assets.
        item.editPersistentDataContainer(p->p.set(key("issued"),PersistentDataType.BYTE,(byte)1));
        data.set(slotKey("applied",s),PersistentDataType.BYTE_ARRAY,item.serializeAsBytes());
        eq.setItem(s,item);eq.setDropChance(s,0);
    }
    @EventHandler(priority=EventPriority.LOWEST,ignoreCancelled=true) public void death(EntityDeathEvent event){
        LivingEntity e=event.getEntity();if(!marked(e))return;
        event.getDrops().removeIf(item->item.getPersistentDataContainer().has(key("issued")));
        // Preserve the vanilla XP distribution for the equipment the mob originally had.
        if(event.getDroppedExp()>0&&e instanceof Mob mob&&e.getEquipment()!=null){
            var data=e.getPersistentDataContainer();var eq=e.getEquipment();
            Map<EquipmentSlot,ItemStack> temporary=new EnumMap<>(EquipmentSlot.class);
            Map<EquipmentSlot,Float> temporaryChances=new EnumMap<>(EquipmentSlot.class);
            for(EquipmentSlot s:SLOTS){
                byte[] original=data.get(slotKey("original",s),PersistentDataType.BYTE_ARRAY);
                if(original!=null&&eq.getItem(s).getPersistentDataContainer().has(key("issued"))){
                    temporary.put(s,eq.getItem(s).clone());
                    temporaryChances.put(s,eq.getDropChance(s));
                    eq.setItem(s,original.length==0?null:ItemStack.deserializeBytes(original));
                    Float originalChance=data.get(slotKey("drop",s),PersistentDataType.FLOAT);
                    if(originalChance!=null)eq.setDropChance(s,originalChance);
                }
            }
            if(!temporary.isEmpty()){
                event.setDroppedExp(mob.getPossibleExperienceReward());
                temporary.forEach(eq::setItem);
                temporaryChances.forEach(eq::setDropChance);
            }
        }
    }
}
