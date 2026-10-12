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

/** Calibration uses Minecraft's own noise implementation, not an approximate noise library. */
public class ContinentsSample {
    public static void main(String[] args) throws Exception {
        SharedConstants.tryDetectVersion();
        Bootstrap.bootStrap();
        var lookup = VanillaRegistries.createWorldLookup();
        var settings = lookup.lookupOrThrow(Registries.NOISE_SETTINGS)
            .getOrThrow(NoiseGeneratorSettings.OVERWORLD).value();
        var df = DensityFunction.CODEC.parse(lookup.createSerializationContext(JsonOps.INSTANCE),
            JsonParser.parseString(Files.readString(Path.of(args[0])))).getOrThrow();
        long[] seeds = {0, 1, 42, 12345, 73102631, -1, 20261012, 8675309,
                        314159265, -987654321, 2026, 987654321};
        int perSeed = 625 * 625;
        var maskDf = DensityFunction.CODEC.parse(lookup.createSerializationContext(JsonOps.INSTANCE),
            JsonParser.parseString(Files.readString(Path.of(args[1])))).getOrThrow();
        var config = JsonParser.parseString(Files.readString(Path.of(args[3]))).getAsJsonObject();
        double targetOcean = config.get("target_ocean_fraction").getAsDouble();
        var masks = new ArrayList<float[]>();
        var samples = new ArrayList<float[]>();
        for (int s = 0; s < seeds.length; s++) {
            var state = RandomState.create(lookup.lookupOrThrow(Registries.NOISE), seeds[s], settings);
            var sampler = state.getSampler(df).bind(SamplerContext.EMPTY_UNCACHED);
            var maskSampler = state.getSampler(maskDf).bind(SamplerContext.EMPTY_UNCACHED);
            float[] values = new float[perSeed];
            float[] maskValues = new float[perSeed];
            int n = 0;
            for (int z = -5000; z < 5000; z += 16)
                for (int x = -5000; x < 5000; x += 16)
                {
                    values[n] = sampler.sampleValue(x, 63, z);
                    maskValues[n++] = maskSampler.sampleValue(x, 63, z);
                }
            samples.add(values);
            masks.add(maskValues);
            System.out.println("Sampled seed " + seeds[s]);
        }
        double low = -1, high = 1;
        for (int iteration = 0; iteration < 25; iteration++) {
            double mid = (low + high) / 2;
            long ocean = 0;
            for (int s = 0; s < 8; s++)
                for (int i = 0; i < perSeed; i++)
                    if (Math.min(samples.get(s)[i] + mid, masks.get(s)[i]) < -.19) ocean++;
            if ((double)ocean / (perSeed * 8) > targetOcean) low = mid; else high = mid;
        }
        double bias = Math.round((low + high) / 2 * 1000000) / 1000000.0;
        JsonObject report = new JsonObject();
        report.addProperty("engine", "Minecraft Java 26.3 official noise sampler");
        report.addProperty("bias", bias);
        report.add("settings", config);
        report.addProperty("samples_per_seed", perSeed);
        report.addProperty("calibration_seed_count", 8);
        report.addProperty("holdout_seed_count", 4);
        report.addProperty("classification", "continentalness < -0.19, before actual biome validation");
        JsonArray rows = new JsonArray();
        for (int s = 0; s < seeds.length; s++) {
            int ocean = 0;
            for (int i = 0; i < perSeed; i++)
                if (Math.min(samples.get(s)[i] + bias, masks.get(s)[i]) < -.19) ocean++;
            JsonObject row = new JsonObject();
            row.addProperty("seed", seeds[s]);
            row.addProperty("holdout", s >= 8);
            row.addProperty("ocean_fraction", (double)ocean / perSeed);
            rows.add(row);
        }
        report.add("seeds", rows);
        Files.writeString(Path.of(args[2]), new GsonBuilder().setPrettyPrinting().create().toJson(report));
    }
}
