package local.mythic.compat;

import java.util.Collection;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.VarInt;
import net.minecraft.network.codec.StreamEncoder;

/** Preserves the former writeCollection wire format on Minecraft 26.3. */
public final class BufferCompat {
    public static <T> void writeCollection(RegistryFriendlyByteBuf buffer, Collection<T> values,
                                           StreamEncoder<RegistryFriendlyByteBuf, T> encoder) {
        VarInt.write(buffer, values.size());
        for (T value : values) encoder.encode(buffer, value);
    }
}
