import com.google.gson.*;
import java.awt.image.BufferedImage;
import java.nio.file.*;
import java.util.*;
import javax.imageio.ImageIO;
import net.minecraft.server.MinecraftServer;
import net.minecraft.core.registries.Registries;
import net.minecraft.tags.BiomeTags;
import net.minecraft.world.level.biome.*;
import net.minecraft.world.level.levelgen.*;
import net.minecraft.world.level.levelgen.densityfunction.*;

/** Test-only server agent. Never included in the distributed datapack. */
public class OceanProbe {
    private static boolean started;
    public static synchronized void onTick(Object object) {
        if (started) return;
        var server = (MinecraftServer)object;
        if (server.overworld() == null) return;
        started = true;
        new Thread(() -> {
            try { verify(server); }
            catch (Throwable error) {
                error.printStackTrace();
                try { Files.writeString(Path.of(System.getProperty("ocean70.output"), "probe-error.txt"), error.toString()); }
                catch (Exception ignored) {}
            }
        }, "Ocean70-verification").start();
    }
    private static JsonObject components(boolean[] land, boolean target) {
        boolean[] visited = new boolean[land.length];
        int[] queue = new int[land.length];
        int total = 0, substantial = 0, largest = 0, largestX = 0, largestZ = 0, maxSpan = 0;
        for (int start = 0; start < land.length; start++) {
            if (visited[start] || land[start] != target) continue;
            int head = 0, tail = 0, minX = 625, maxX = 0, minZ = 625, maxZ = 0;
            queue[tail++] = start;
            visited[start] = true;
            while (head < tail) {
                int i = queue[head++], x = i % 625, z = i / 625;
                minX = Math.min(minX, x); maxX = Math.max(maxX, x);
                minZ = Math.min(minZ, z); maxZ = Math.max(maxZ, z);
                // Eight neighbours count diagonal land contacts conservatively.
                for (int dz = -1; dz <= 1; dz++) for (int dx = -1; dx <= 1; dx++) {
                    int nx = x + dx, nz = z + dz;
                    if (nx < 0 || nx >= 625 || nz < 0 || nz >= 625) continue;
                    int next = nz * 625 + nx;
                    if (!visited[next] && land[next] == target) {
                        visited[next] = true; queue[tail++] = next;
                    }
                }
            }
            total++;
            maxSpan = Math.max(maxSpan, Math.max(maxX - minX + 1, maxZ - minZ + 1) * 16);
            if (tail >= 1000) substantial++;
            if (tail > largest) {
                largest = tail; largestX = (maxX - minX + 1) * 16; largestZ = (maxZ - minZ + 1) * 16;
            }
        }
        JsonObject out = new JsonObject();
        out.addProperty("components", total);
        out.addProperty("components_over_256000_blocks2", substantial);
        out.addProperty("largest_sampled_area_blocks2", largest * 256L);
        out.addProperty("largest_sampled_fraction_of_region", (double)largest / land.length);
        out.addProperty("largest_component_span_x", largestX);
        out.addProperty("largest_component_span_z", largestZ);
        out.addProperty("maximum_span_across_all_components", maxSpan);
        return out;
    }
    private static void verify(MinecraftServer server) throws Exception {
        Path out = Path.of(System.getProperty("ocean70.output"));
        var level = server.overworld();
        var generator = (NoiseBasedChunkGenerator)level.getChunkSource().getGenerator();
        var settings = generator.generatorSettings().value();
        var source = generator.getBiomeSource();
        var lookup = server.registryAccess();
        long[] seeds = {0, 1, 42, 12345, 73102631, -1, 20261012, 8675309,
                        314159265, -987654321, 2026, 987654321};
        JsonObject report = new JsonObject();
        report.addProperty("engine", "Official Minecraft Java 26.3 server with distributed datapack loaded");
        report.addProperty("method", "Every 16 blocks, chunk centres; x,z in [-5000,5000); biome y=64; 8-neighbour connectivity");
        report.addProperty("samples_per_seed", 625 * 625);
        JsonArray rows = new JsonArray();
        double mean = 0;
        for (long seed : seeds) {
            var state = RandomState.create(lookup.lookupOrThrow(Registries.NOISE), seed, settings);
            var climate = state.createClimateSampler(SamplerContext.EMPTY_UNCACHED);
            var resolver = source.createResolver(climate);
            boolean[] land = new boolean[625 * 625];
            int ocean = 0;
            BufferedImage image = new BufferedImage(625, 625, BufferedImage.TYPE_INT_RGB);
            for (int iz = 0; iz < 625; iz++) for (int ix = 0; ix < 625; ix++) {
                int x = -5000 + ix * 16, z = -5000 + iz * 16;
                var biome = resolver.getNoiseBiome(x >> 2, 16, z >> 2);
                boolean sea = biome.is(BiomeTags.IS_OCEAN);
                land[iz * 625 + ix] = !sea;
                if (sea) ocean++;
                String name = biome.unwrapKey().orElseThrow().identifier().getPath();
                int color = sea ? (name.startsWith("deep_") ? 0x123758 : 0x236185)
                    : name.contains("beach") ? 0xdcca89
                    : name.contains("desert") ? 0xc9b77e
                    : name.contains("snow") || name.contains("frozen") ? 0xd6e3df
                    : name.contains("river") ? 0x548faf : 0x6d965c;
                image.setRGB(ix, iz, color);
            }
            JsonObject row = new JsonObject();
            row.addProperty("seed", seed);
            row.addProperty("ocean_fraction", (double)ocean / land.length);
            row.addProperty("land_fraction", 1 - (double)ocean / land.length);
            row.add("land_components", components(land, true));
            row.add("ocean_components", components(land, false));
            rows.add(row);
            mean += (double)ocean / land.length;
            if (seed == 73102631 || seed == 42) ImageIO.write(image, "PNG", out.resolve("biomes-seed-" + seed + ".png").toFile());
            System.out.println("OCEAN70 seed=" + seed + " ocean=" + (double)ocean / land.length);
        }
        report.add("seeds", rows);
        report.addProperty("mean_ocean_fraction", mean / seeds.length);
        // Independent terrain-column sample: actual solid terrain below sea level.
        var state = level.getChunkSource().randomState();
        var resolver = source.createResolver(state.createClimateSampler(SamplerContext.EMPTY_UNCACHED));
        var continentalness = state.getSampler(settings.noiseRouter().continents()).bind(SamplerContext.EMPTY_UNCACHED);
        int belowSea = 0, oceanBiome = 0, mismatches = 0, samples = 0, deep = 0, dryDeep = 0;
        for (int z = -4920; z < 5000; z += 160) for (int x = -4920; x < 5000; x += 160) {
            int height = generator.getBaseHeight(x, z, Heightmap.Types.OCEAN_FLOOR_WG, level, state);
            boolean sea = height < settings.seaLevel();
            boolean biomeSea = resolver.getNoiseBiome(x >> 2, 16, z >> 2).is(BiomeTags.IS_OCEAN);
            if (sea) belowSea++;
            if (biomeSea) oceanBiome++;
            if (sea != biomeSea) mismatches++;
            if (continentalness.sampleValue(x, 64, z) < -.7) {
                deep++;
                if (!sea) dryDeep++;
            }
            samples++;
        }
        JsonObject terrain = new JsonObject();
        terrain.addProperty("seed", level.getSeed());
        terrain.addProperty("samples", samples);
        terrain.addProperty("solid_terrain_below_sea_fraction", (double)belowSea / samples);
        terrain.addProperty("ocean_biome_fraction", (double)oceanBiome / samples);
        terrain.addProperty("classification_disagreements", mismatches);
        terrain.addProperty("deep_ocean_samples", deep);
        terrain.addProperty("deep_ocean_columns_above_sea", dryDeep);
        report.add("terrain_columns", terrain);
        Files.writeString(out.resolve("engine-validation.json"), new GsonBuilder().setPrettyPrinting().create().toJson(report));
        System.out.println("OCEAN70 verification complete");
    }
}
