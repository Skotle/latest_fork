package kr.infernal.test;

import com.mojang.authlib.GameProfile;
import io.netty.channel.ChannelFutureListener;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.server.level.ClientInformation;
import net.minecraft.server.network.ServerGamePacketListenerImpl;
import net.minecraft.server.network.CommonListenerCookie;
import net.minecraft.network.Connection;
import net.minecraft.network.protocol.PacketFlow;
import net.minecraft.network.protocol.Packet;
import net.minecraft.world.level.GameType;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import org.bukkit.*;
import org.bukkit.craftbukkit.CraftServer;
import org.bukkit.craftbukkit.entity.CraftWitch;
import org.bukkit.entity.Witch;
import org.bukkit.event.entity.*;
import java.net.*;
import java.util.UUID;

/** Actual server-side vanilla player. No client/socket or gameplay agent is installed. */
final class NativePlayerProbe {
    static void run(InfernalProbe test){
        test.command("difficulty nightmare");
        var server=((CraftServer)Bukkit.getServer()).getServer();
        GameProfile profile=new GameProfile(UUID.randomUUID(),"NativeSurvivalProbe");
        ServerPlayer player=new ServerPlayer(server,server.overworld(),profile,ClientInformation.createDefault());
        Connection connection=new Connection(PacketFlow.SERVERBOUND){
            public void send(Packet<?> p){}
            public void send(Packet<?> p,ChannelFutureListener listener){}
            public void send(Packet<?> p,ChannelFutureListener listener,boolean flush){}
            public SocketAddress getRemoteAddress(){return new InetSocketAddress("127.0.0.1",0);}
            public boolean isConnected(){return true;}
            public void flushChannel(){}
            public void tick(){}
        };
        player.connection=new ServerGamePacketListenerImpl(server,connection,player,CommonListenerCookie.createInitial(profile,false));
        player.setGameMode(GameType.SURVIVAL);
        player.snapTo(32,100,0);
        player.setNoGravity(true);
        server.overworld().addNewPlayer(player); // Real event dispatch requires a valid, world-registered entity.
        var bukkit=player.getBukkitEntity();
        bukkit.setExhaustion(0);
        player.causeFoodExhaustion(4,EntityExhaustionEvent.ExhaustionReason.SPRINT);
        test.near(bukkit.getExhaustion(),7,"native player exhaustion event chain");
        player.setHealth(10);
        player.heal(4,EntityRegainHealthEvent.RegainReason.SATIATED);
        test.near(player.getHealth(),11,"native player natural healing event chain");
        player.heal(4,EntityRegainHealthEvent.RegainReason.MAGIC);
        test.near(player.getHealth(),15,"native player magic healing unchanged");
        Witch witch=test.world.spawn(new Location(test.world,34,100,0),Witch.class,e->e.setAI(false));
        var source=((CraftWitch)witch).getHandle();
        player.addEffect(new MobEffectInstance(MobEffects.POISON,80,0),source);
        var poison=player.getEffect(MobEffects.POISON);
        test.check(poison!=null&&poison.getDuration()==140&&poison.getAmplifier()==0,"native potion effect applies once with scaled duration");
        player.removeAllEffects(EntityPotionEffectEvent.Cause.MILK);
        test.check(!player.hasEffect(MobEffects.POISON),"native milk removal not reversed by effect hook");
        witch.remove();
        test.command("difficulty hard");
        bukkit.setExhaustion(0);
        player.causeFoodExhaustion(4,EntityExhaustionEvent.ExhaustionReason.SPRINT);
        test.near(bukkit.getExhaustion(),4,"native player restores base exhaustion");
        player.discard();
    }
}
