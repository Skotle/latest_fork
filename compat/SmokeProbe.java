import org.bukkit.*;
import org.bukkit.entity.*;
import org.bukkit.attribute.Attribute;
import org.bukkit.event.entity.CreatureSpawnEvent.SpawnReason;
import org.bukkit.plugin.java.JavaPlugin;
import io.lumine.mythic.bukkit.MythicBukkit;
import io.lumine.mythic.bukkit.utils.version.*;

/** Test-only plugin; never shipped in the deployment bundle. */
public final class SmokeProbe extends JavaPlugin {
    @Override public void onEnable() {
        getServer().getScheduler().runTaskLater(this, () -> {
            try {
                var mythic = MythicBukkit.inst();
                check(mythic.isEnabled(), "Mythic enabled");
                var loader = mythic.getClass().getClassLoader();
                Class<?> removePacket = Class.forName("net.minecraft.network.protocol.game.ClientboundRemoveEntitiesPacket");
                Object packet = removePacket.getConstructor(int[].class).newInstance((Object)new int[]{12345, 12346});
                var listener = Class.forName("io.lumine.mythic.core.volatilecode.v26_2.packets.VolatileChannelHandler", true, loader)
                    .getDeclaredMethod("lambda$new$0", removePacket);
                listener.setAccessible(true);
                listener.invoke(null, packet);
                check(true, "entity removal packet callback executes");
                var handler = mythic.getVolatileCodeHandler().getEntityHandler();
                try {
                    handler.initTeams(null);
                    throw new AssertionError("Expected missing test player");
                } catch (NullPointerException expected) {
                    // No player is connected in this test. Encoding and decoding run before player adaptation.
                    boolean reachedPlayer = java.util.Arrays.stream(expected.getStackTrace())
                        .anyMatch(frame -> frame.getClassName().equals("io.lumine.mythic.bukkit.BukkitAdapter") && frame.getMethodName().equals("adapt"))
                        || String.valueOf(expected.getMessage()).contains("CraftPlayer.getHandle()");
                    getLogger().info("Expected missing-player boundary: " + expected.getMessage());
                    check(reachedPlayer, "glow team packet serialization reaches player send stage");
                }
                check(NMSVersion.forMinecraftVersion(MinecraftVersion.of(26,3,0)).orElseThrow() == NMSVersion.v26_2, "26.3 mapping");
                check(NMSVersion.forMinecraftVersion(MinecraftVersion.of(26,2,0)).orElseThrow() == NMSVersion.v26_2, "26.2 mapping preserved");
                check(NMSVersion.forMinecraftVersion(MinecraftVersion.of(26,4,0)).isEmpty(), "future versions rejected");
                var manager = mythic.getRandomSpawningManager();
                for (String name : new String[]{"spawnFiles", "spawnLoaders", "randomSpawnersReplace"}) {
                    var diagnostic = manager.getClass().getDeclaredField(name);
                    diagnostic.setAccessible(true);
                    getLogger().info(name + "=" + diagnostic.get(manager));
                }
                var field = manager.getClass().getDeclaredField("randomSpawnersReplace");
                field.setAccessible(true);
                var rules = (java.util.List<io.lumine.mythic.core.spawning.random.RandomSpawner>) field.get(manager);
                check(rules.stream().map(r -> r.getName()).distinct().count() == 5, "five unique REPLACE rules loaded");
                var world = getServer().getWorlds().getFirst();
                var location = new Location(world, 0, 150, 0);
                world.getChunkAt(location).load();
                String[] names = {"Revenant", "Reaper", "Stalker", "Executioner", "VoidHunter"};
                double[] hp = {120, 90, 100, 180, 200};
                for (int i=0; i<names.length; i++) {
                    var mob = (LivingEntity) mythic.getAPIHelper().spawnMythicMob("Extreme" + names[i], location, 1);
                    check(mythic.getAPIHelper().isMythicMob(mob), names[i] + " registered");
                    check(mob.getAttribute(Attribute.MAX_HEALTH).getValue() == hp[i], names[i] + " health");
                    mob.remove();
                }
                for (int i=0; i<30; i++) world.spawn(location, Zombie.class, SpawnReason.NATURAL);
                getServer().getScheduler().runTaskLater(this, () -> {
                    try {
                        long replaced = world.getEntities().stream().filter(e -> mythic.getAPIHelper().isMythicMob(e)).count();
                        check(replaced > 0, "NATURAL spawn replacement");
                        getLogger().info("SMOKE PASS: mapping, activation, five mob types, health and natural replacement");
                    } catch (Throwable failure) {
                        getLogger().log(java.util.logging.Level.SEVERE, "SMOKE FAIL", failure);
                    } finally { getServer().shutdown(); }
                }, 40);
            } catch (Throwable failure) {
                getLogger().log(java.util.logging.Level.SEVERE, "SMOKE FAIL", failure);
                getServer().shutdown();
            }
        }, 40);
    }
    private void check(boolean condition, String label) {
        if (!condition) throw new AssertionError(label);
        getLogger().info("PASS: " + label);
    }
}
