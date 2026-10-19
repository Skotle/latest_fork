import com.google.gson.*;
import com.mojang.serialization.JsonOps;
import java.nio.file.*;
import java.util.*;
import net.minecraft.SharedConstants;
import net.minecraft.server.Bootstrap;
import net.minecraft.core.registries.Registries;
import net.minecraft.data.registries.VanillaRegistries;
import net.minecraft.world.level.levelgen.*;
import net.minecraft.world.level.levelgen.densityfunction.*;

public class ConnectedSample {
    public static void main(String[] args) throws Exception {
        SharedConstants.tryDetectVersion();
        Bootstrap.bootStrap();
        var lookup = VanillaRegistries.createWorldLookup();
        var settings = lookup.lookupOrThrow(Registries.NOISE_SETTINGS).getOrThrow(NoiseGeneratorSettings.OVERWORLD).value();
        var df = DensityFunction.CODEC.parse(lookup.createSerializationContext(JsonOps.INSTANCE),
            JsonParser.parseString(Files.readString(Path.of(args[0])))).getOrThrow();
        int width = 321, step = 32;
        JsonArray rows = new JsonArray();
        for (long seed : new long[]{0, 1, 42, 12345, 73102631, -1, 20261019, 8675309, 314159265, -987654321, 2026, 987654321}) {
            var state = RandomState.create(lookup.lookupOrThrow(Registries.NOISE), seed, settings);
            var sampler = state.getSampler(df).bind(SamplerContext.EMPTY_UNCACHED);
            boolean[] sea = new boolean[width * width], seen = new boolean[sea.length];
            int ocean = 0;
            for (int z = 0; z < width; z++) for (int x = 0; x < width; x++) {
                sea[z * width + x] = sampler.sampleValue((x - width / 2) * step, 63, (z - width / 2) * step) < -.19;
                if (sea[z * width + x]) ocean++;
            }
            int[] queue = new int[sea.length];
            int components = 0, enclosed = 0;
            for (int start = 0; start < sea.length; start++) {
                if (!sea[start] || seen[start]) continue;
                int head = 0, tail = 0;
                boolean boundary = false;
                queue[tail++] = start; seen[start] = true;
                while (head < tail) {
                    int current = queue[head++], x = current % width, z = current / width;
                    if (x == 0 || z == 0 || x == width - 1 || z == width - 1) boundary = true;
                    for (int[] d : new int[][]{{1,0},{-1,0},{0,1},{0,-1}}) {
                        int nx = x + d[0], nz = z + d[1];
                        if (nx < 0 || nz < 0 || nx >= width || nz >= width) continue;
                        int next = nz * width + nx;
                        if (sea[next] && !seen[next]) {seen[next] = true; queue[tail++] = next;}
                    }
                }
                components++;
                if (!boundary) enclosed++;
            }
            JsonObject row = new JsonObject();
            row.addProperty("seed", seed); row.addProperty("ocean_fraction", (double)ocean / sea.length);
            row.addProperty("ocean_components", components); row.addProperty("enclosed_ocean_components", enclosed);
            rows.add(row);
            System.out.println("Seed " + seed + ": ocean components=" + components + ", enclosed=" + enclosed);
            if (enclosed != 0) throw new IllegalStateException("Enclosed ocean sample: " + seed);
        }
        JsonObject report = new JsonObject();
        report.addProperty("method", "Official 26.3 density codec and noise sampler; four-neighbour flood fill; not actual blocks or biome validation");
        report.addProperty("step_blocks", step); report.addProperty("samples_per_seed", width * width);
        report.add("seeds", rows);
        Files.writeString(Path.of(args[1]), new GsonBuilder().setPrettyPrinting().create().toJson(report));
    }
}
