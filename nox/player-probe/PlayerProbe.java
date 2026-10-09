import java.util.UUID;
import java.net.SocketAddress;
import java.net.InetSocketAddress;
import com.mojang.authlib.GameProfile;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.server.level.ClientInformation;
import net.minecraft.server.network.ServerGamePacketListenerImpl;
import net.minecraft.server.network.CommonListenerCookie;
import net.minecraft.network.Connection;
import net.minecraft.network.protocol.PacketFlow;
import net.minecraft.network.protocol.Packet;
import net.minecraft.world.level.GameType;
import io.netty.channel.ChannelFutureListener;

/** Actual vanilla player entity, with packet sends suppressed; never a client render test. */
public class PlayerProbe {
    private static int ticks;
    private static boolean attempted;
    public static void tick(MinecraftServer server) {
        ++ticks;
        if (attempted) {
            ServerPlayer p=server.getPlayerList().getPlayerByName("CombatProbe");
            // Isolate the scripted damage measurement from earlier ambush hurt cooldown.
            if (p!=null) p.setInvulnerableTime(0);
            if (p!=null && p.entityTags().contains("probe.armor_sample")) p.getFoodData().setFoodLevel(17);
            if (p!=null && p.entityTags().contains("probe.heal")) {p.setHealth(p.getMaxHealth());p.removeTag("probe.heal");}
            // The probe has no packet listener tick; advance real item-use timers for shield tests.
            if (p!=null && p.entityTags().contains("probe.shield")) {
                p.getFoodData().setFoodLevel(17); // Prevent natural regeneration from masking measured damage.
                p.doTick();
            }
            if (p!=null && p.entityTags().contains("probe.shield") && !p.isUsingItem())
                p.startUsingItem(net.minecraft.world.InteractionHand.OFF_HAND);
            if (p!=null && !p.entityTags().contains("probe.shield") && p.isUsingItem()) p.stopUsingItem();
            if (p!=null && p.entityTags().contains("probe.native")) {
                p.removeTag("probe.native");
                for (var entity : server.overworld().getAllEntities()) {
                    if (entity.entityTags().contains("fw.boss") && entity instanceof net.minecraft.world.entity.monster.skeleton.AbstractSkeleton skeleton) {
                        skeleton.performRangedAttack(p,1f);
                        int piercing=-1;
                        for (var candidate : server.overworld().getAllEntities()) {
                            if (candidate instanceof net.minecraft.world.entity.projectile.arrow.AbstractArrow arrow && arrow.getOwner()==entity)
                                piercing=Math.max(piercing,arrow.getPierceLevel());
                        }
                        server.getCommands().performPrefixedCommand(server.createCommandSourceStack(),"scoreboard players set #native_birth fw.tmp "+piercing);
                        break;
                    }
                }
            }
            if (p!=null && p.entityTags().contains("probe.attack")) {
                p.removeTag("probe.attack");
                for (var entity : server.overworld().getAllEntities()) {
                    if (entity.entityTags().contains("db.boss")) {p.attack(entity);System.out.println("PLAYER_PROBE_ATTACK");break;}
                }
            }
            return;
        }
        if (ticks < 20) return;
        attempted = true;
        try {
            GameProfile profile = new GameProfile(UUID.fromString("12345678-1234-1234-1234-123456789abc"), "CombatProbe");
            ServerPlayer player = new ServerPlayer(server, server.overworld(), profile, ClientInformation.createDefault());
            Connection connection = new Connection(PacketFlow.SERVERBOUND) {
                public void send(Packet<?> p) {}
                public void send(Packet<?> p, ChannelFutureListener listener) {}
                public void send(Packet<?> p, ChannelFutureListener listener, boolean flush) {}
                public SocketAddress getRemoteAddress() {return new InetSocketAddress("127.0.0.1",0);}
                public boolean isConnected() {return true;}
                public void flushChannel() {}
                public void tick() {}
            };
            player.connection = new ServerGamePacketListenerImpl(server, connection, player, CommonListenerCookie.createInitial(profile,false));
            player.setGameMode(GameType.SURVIVAL);
            player.getAttribute(net.minecraft.world.entity.ai.attributes.Attributes.MAX_HEALTH).setBaseValue(1024);
            player.setHealth(1024);
            player.snapTo(128,81,12);
            player.setNoGravity(true);
            player.setOnGround(true);
            player.addTag("probe.player");
            server.getPlayerList().getPlayers().add(player);
            server.getPlayerList().getPlayersByUUID().put(player.getUUID(),player);
            server.overworld().addNewPlayer(player);
            player.initInventoryMenu();
            System.out.println("PLAYER_PROBE_READY");
        } catch (Throwable error) {
            System.out.println("PLAYER_PROBE_FAILED");
            error.printStackTrace();
        }
    }
}
