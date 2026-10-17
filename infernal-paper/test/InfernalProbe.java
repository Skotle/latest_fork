package kr.infernal.test;

import kr.infernal.InfernalDifficulties;
import com.mojang.brigadier.CommandDispatcher;
import io.papermc.paper.command.brigadier.CommandSourceStack;
import io.papermc.paper.plugin.lifecycle.event.types.LifecycleEvents;
import org.bukkit.*;
import org.bukkit.attribute.*;
import org.bukkit.entity.*;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.inventory.*;
import org.bukkit.persistence.*;
import org.bukkit.plugin.java.JavaPlugin;
import java.util.*;
import java.nio.file.*;

/** Test-only plugin. Never included in the delivered JAR. */
public final class InfernalProbe extends JavaPlugin {
    InfernalDifficulties target;
    CommandDispatcher<CommandSourceStack> dispatcher;
    int passed;
    double originalFollow;
    double excludedHealth;
    World world;
    Zombie zombie,baby,excluded;
    Creeper creeper;
    LivingEntity boss,warden,animal;
    List<String> reports=new ArrayList<>();
    List<Runnable> steps=new ArrayList<>();
    int index;
    @Override public void onEnable(){
        target=(InfernalDifficulties)getServer().getPluginManager().getPlugin("InfernalDifficulties");
        getLifecycleManager().registerEventHandler(LifecycleEvents.COMMANDS,event->dispatcher=event.registrar().getDispatcher());
        getServer().getScheduler().runTaskLater(this,()->{
            try{
                world=getServer().getWorlds().getFirst();world.setTime(18000);world.getChunkAt(0,0).setForceLoaded(true);
                if(Files.exists(Path.of("restart-state.txt"))){restartChecks();return;}
                setup();
                getServer().getScheduler().runTaskTimer(this,()->{
                    try{if(index<steps.size())steps.get(index++).run();}
                    catch(Throwable failure){fail(failure);}
                },1,3);
            }catch(Throwable failure){fail(failure);}
        },30);
    }
    void command(String line){check(getServer().dispatchCommand(getServer().getConsoleSender(),line),"dispatch "+line);}
    void check(boolean condition,String name){if(!condition)throw new AssertionError(name);passed++;reports.add(name);getLogger().info("TEST_PASS "+name);}
    void near(double actual,double expected,String name){check(Math.abs(actual-expected)<.0001,name+" actual="+actual);}
    double attr(LivingEntity e,Attribute a){return e.getAttribute(a).getValue();}
    <T extends LivingEntity>T spawn(Class<T> clazz,double x){return world.spawn(new Location(world,x,100,0),clazz,e->{
        e.setAI(false);e.setPersistent(true);e.addScoreboardTag("probe");
        // Random vanilla leader-zombie health bonuses must not make fixed-fixture assertions flaky.
        if(e instanceof Zombie){var max=e.getAttribute(Attribute.MAX_HEALTH);for(var m:new ArrayList<>(max.getModifiers()))max.removeModifier(m);max.setBaseValue(20);e.setHealth(20);}
    });}
    void setup(){
        steps.add(()->{
            check(target!=null&&target.isEnabled(),"plugin enabled");
            var node=dispatcher.getRoot().getChild("difficulty");
            check(node!=null,"difficulty command exists");
            for(var p:InfernalDifficulties.Preset.values())check(node.getChild(p.name().toLowerCase(Locale.ROOT))!=null,"literal "+p);
            check(!node.canUse(nullSafeNoPermission()),"permission requirement");
            command("difficulty hard");
            zombie=spawn(Zombie.class,0);zombie.setAdult();zombie.getEquipment().clear();
            zombie.getEquipment().setHelmet(new ItemStack(Material.DIAMOND_HELMET));zombie.getEquipment().setHelmetDropChance(.75f);
            baby=spawn(Zombie.class,2);baby.setBaby();
            excluded=world.spawn(new Location(world,4,100,0),Zombie.class,e->{e.setAI(false);e.setAdult();e.addScoreboardTag("infernal.exclude");e.addScoreboardTag("probe");});
            excludedHealth=attr(excluded,Attribute.MAX_HEALTH);
            creeper=spawn(Creeper.class,6);creeper.setMaxFuseTicks(37);
            boss=spawn(ElderGuardian.class,8);warden=spawn(Warden.class,10);animal=spawn(Cow.class,12);
        });
        final double[] babySpeed={0};
        steps.add(()->{babySpeed[0]=attr(baby,Attribute.MOVEMENT_SPEED);command("difficulty nightmare");});
        steps.add(()->{
            near(attr(zombie,Attribute.MAX_HEALTH),40,"nightmare health");near(zombie.getHealth(),40,"full health scaling");
            near(attr(baby,Attribute.MOVEMENT_SPEED),babySpeed[0],"baby speed excluded");near(attr(excluded,Attribute.MAX_HEALTH),excludedHealth,"excluded mob");
            near(attr(boss,Attribute.MAX_HEALTH),120,"nightmare boss");near(attr(warden,Attribute.MAX_HEALTH),500,"warden unchanged");near(attr(animal,Attribute.MAX_HEALTH),10,"animal unchanged");
            check(creeper.getMaxFuseTicks()==20,"nightmare creeper fuse");
            Zombie reward=world.spawn(new Location(world,14,100,0),Zombie.class,e->{e.setAI(false);e.setAdult();e.getEquipment().clear();e.getEquipment().setItemInMainHand(new ItemStack(Material.BOW));e.getEquipment().setItemInMainHandDropChance(2);e.addScoreboardTag("probe");});
            target.reconcile(reward);
            try{
                var give=InfernalDifficulties.class.getDeclaredMethod("give",LivingEntity.class,EquipmentSlot.class,ItemStack.class);give.setAccessible(true);
                give.invoke(target,reward,EquipmentSlot.FEET,new ItemStack(Material.IRON_BOOTS));
                give.invoke(target,reward,EquipmentSlot.HAND,new ItemStack(Material.BOW));
            }catch(Exception e){throw new RuntimeException(e);}
            var drops=new ArrayList<ItemStack>();drops.add(reward.getEquipment().getBoots().clone());drops.add(new ItemStack(Material.ROTTEN_FLESH));
            var death=new org.bukkit.event.entity.EntityDeathEvent(reward,org.bukkit.damage.DamageSource.builder(org.bukkit.damage.DamageType.GENERIC).build(),drops,100);
            target.death(death);
            check(death.getDrops().size()==1&&death.getDrops().getFirst().getType()==Material.ROTTEN_FLESH,"issued drops filtered and natural drops retained");
            check(death.getDroppedExp()==5,"issued gear grants no bonus XP");
            near(reward.getEquipment().getItemInMainHandDropChance(),0,"death calculation restores issued drop suppression");
            reward.remove();
            command("execute run difficulty nightmare");command("difficulty");
            near(attr(zombie,Attribute.MAX_HEALTH),40,"same mode no stacking");
            zombie.setHealth(20);
            // Force one issued item using the production path to test deterministic restoration.
            try{
                var give=InfernalDifficulties.class.getDeclaredMethod("give",LivingEntity.class,EquipmentSlot.class,ItemStack.class);give.setAccessible(true);
                give.invoke(target,zombie,EquipmentSlot.FEET,new ItemStack(Material.IRON_BOOTS));
            }catch(Exception e){throw new RuntimeException(e);}
            check(zombie.getEquipment().getBootsDropChance()==0,"issued gear no drop");
            command("difficulty hard");
            near(attr(zombie,Attribute.MAX_HEALTH),20,"health restored");near(zombie.getHealth(),10,"health ratio preserved");
            check(zombie.getEquipment().getBoots().isEmpty(),"issued boots removed");
            check(zombie.getEquipment().getHelmet().getType()==Material.DIAMOND_HELMET,"natural helmet retained");
            near(zombie.getEquipment().getHelmetDropChance(),.75,"natural drop chance retained");
            check(creeper.getMaxFuseTicks()==37,"custom original fuse restored");
            command("difficulty nightmare");
            try{
                var give=InfernalDifficulties.class.getDeclaredMethod("give",LivingEntity.class,EquipmentSlot.class,ItemStack.class);give.setAccessible(true);
                give.invoke(target,zombie,EquipmentSlot.FEET,new ItemStack(Material.IRON_BOOTS));
            }catch(Exception e){throw new RuntimeException(e);}
            zombie.getEquipment().setBoots(new ItemStack(Material.DIAMOND_BOOTS));zombie.getEquipment().setBootsDropChance(1);
            command("difficulty hard");
            check(zombie.getEquipment().getBoots().getType()==Material.DIAMOND_BOOTS,"replacement gear preserved");
            near(zombie.getEquipment().getBootsDropChance(),1,"replacement drop chance preserved");
        });
        for(var p:InfernalDifficulties.Preset.values()){
            steps.add(()->{
                command("difficulty "+p.name().toLowerCase(Locale.ROOT));
                check(target.current(world)==p,"selected "+p);
                for(World w:getServer().getWorlds())check(w.getDifficulty()==p.base(),"base "+p+" "+w.getName());
            });
        }
        steps.add(()->{
            command("difficulty nightmare");
            zombie=spawn(Zombie.class,0);zombie.setAdult();zombie.getEquipment().clear();
            zombie.getAttribute(Attribute.FOLLOW_RANGE).setBaseValue(60);
            originalFollow=attr(zombie,Attribute.FOLLOW_RANGE);
        });
        steps.add(()->{
            near(attr(zombie,Attribute.FOLLOW_RANGE),64,"follow cap");
            command("difficulty hard");near(attr(zombie,Attribute.FOLLOW_RANGE),originalFollow,"follow restored");
            command("difficulty nightmare");
            // Every eligible entity type must support its own path without crashing.
            String[] types=("ZOMBIE HUSK DROWNED ZOMBIE_VILLAGER ZOMBIFIED_PIGLIN PIGLIN PIGLIN_BRUTE WITHER_SKELETON SPIDER CAVE_SPIDER SILVERFISH ENDERMITE ENDERMAN HOGLIN ZOGLIN VINDICATOR VEX RAVAGER SKELETON STRAY BOGGED PILLAGER EVOKER WITCH CREEPER BLAZE GHAST PHANTOM GUARDIAN SHULKER BREEZE SLIME MAGMA_CUBE WITHER ENDER_DRAGON").split(" ");
            int x=0;
            for(String name:types){
                var entity=(LivingEntity)world.spawnEntity(new Location(world,x++%8,110,8),EntityType.valueOf(name));
                entity.setAI(false);entity.addScoreboardTag("probe");
            }
        });
        steps.add(()->{
            for(LivingEntity e:world.getLivingEntities()){
                if(e.getScoreboardTags().contains("probe")&&e.getType()!=EntityType.WARDEN&&e.getType()!=EntityType.COW&&!e.getScoreboardTags().contains("infernal.exclude"))
                    check(e.getPersistentDataContainer().has(new NamespacedKey(target,"preset")),"applied "+e.getType());
            }
            command("minecraft:difficulty normal");
        });
        steps.add(()->{
            check(target.current(world)==InfernalDifficulties.Preset.NORMAL,"external vanilla command releases custom mode");
            near(attr(zombie,Attribute.MAX_HEALTH),20,"external vanilla restores attributes");
            command("difficulty nightmare");
            // Preserve stable entity state across a full server restart.
            for(LivingEntity e:new ArrayList<>(world.getLivingEntities()))if(e!=zombie)e.remove();
            zombie.setPersistent(true);zombie.setHealth(20);
            try{Files.writeString(Path.of("restart-state.txt"),zombie.getUniqueId()+"\n"+zombie.getEquipment().getItemInMainHand().getType()+"\n"+passed);}
            catch(Exception e){throw new RuntimeException(e);}
            saveReport("phase1.json");
            getLogger().info("INFERNAL_PHASE1_PASS");getServer().shutdown();
        });
    }
    CommandSourceStack nullSafeNoPermission(){
        return (CommandSourceStack)java.lang.reflect.Proxy.newProxyInstance(getClass().getClassLoader(),new Class[]{CommandSourceStack.class},(proxy,method,args)->{
            if(method.getName().equals("getSender"))return java.lang.reflect.Proxy.newProxyInstance(getClass().getClassLoader(),new Class[]{org.bukkit.command.CommandSender.class},(p,m,a)->m.getName().equals("hasPermission")?false:null);
            return null;
        });
    }
    void restartChecks()throws Exception{
        List<String> data=Files.readAllLines(Path.of("restart-state.txt"));
        zombie=(Zombie)getServer().getEntity(UUID.fromString(data.get(0)));
        check(zombie!=null,"persistent entity reloaded");
        check(target.current(world)==InfernalDifficulties.Preset.NIGHTMARE,"preset survives restart");
        near(attr(zombie,Attribute.MAX_HEALTH),40,"restart no health stacking");near(zombie.getHealth(),20,"restart health retained");
        check(zombie.getEquipment().getItemInMainHand().getType().name().equals(data.get(1)),"restart equipment unchanged");
        command("difficulty hard");near(attr(zombie,Attribute.MAX_HEALTH),20,"restart restore max health");near(zombie.getHealth(),10,"restart restore health ratio");
        saveReport("phase2.json");getLogger().info("INFERNAL_PHASE2_PASS");getServer().shutdown();
    }
    void saveReport(String filename){
        try{Files.writeString(Path.of(filename),"{\"passed\":"+passed+",\"checks\":["+String.join(",",reports.stream().map(s->"\""+s.replace("\\","\\\\").replace("\"","\\\"")+"\"").toList())+"]}");}
        catch(Exception e){throw new RuntimeException(e);}
    }
    void fail(Throwable failure){getLogger().log(java.util.logging.Level.SEVERE,"INFERNAL_TEST_FAIL",failure);getServer().shutdown();index=steps.size();}
}
