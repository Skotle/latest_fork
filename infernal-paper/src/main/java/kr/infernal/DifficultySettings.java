package kr.infernal;

import org.bukkit.configuration.file.YamlConfiguration;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

/** Validated, editable preset matrix. Vanilla tiers delegate their rules to Minecraft. */
public final class DifficultySettings {
    public record Profile(Map<String,Double> values,String revision) {
        public double value(String key){return Objects.requireNonNull(values.get(key),key);}
        public int integer(String key){return (int)Math.round(value(key));}
    }
    private final EnumMap<InfernalDifficulties.Preset,Profile> profiles=new EnumMap<>(InfernalDifficulties.Preset.class);
    public final boolean survival;
    private static final Set<String> PERCENT=Set.of("armor-chance","armor-enchant-chance","armor-iron","armor-diamond","armor-netherite","weapon-chance","weapon-diamond","weapon-netherite","bow-chance");
    private static final Set<String> INTEGER=Set.of("armor-min","armor-max","protection","sharpness","power","quick-charge","piercing","sleep-percentage","creeper-fuse");
    public DifficultySettings(InfernalDifficulties plugin)throws IOException,org.bukkit.configuration.InvalidConfigurationException {
        File file=new File(plugin.getDataFolder(),"profiles.yml");
        if(!file.exists())plugin.saveResource("profiles.yml",false);
        YamlConfiguration config=new YamlConfiguration();config.load(file);
        YamlConfiguration defaults;
        try(var stream=Objects.requireNonNull(plugin.getResource("profiles.yml"));var reader=new InputStreamReader(stream,StandardCharsets.UTF_8)){
            defaults=YamlConfiguration.loadConfiguration(reader);
        }
        config.setDefaults(defaults);config.options().copyDefaults(true);
        survival=config.getBoolean("survival-scaling",true);
        for(var preset:InfernalDifficulties.Preset.values()){
            String prefix="profiles."+preset.name().toLowerCase(Locale.ROOT);
            var section=Objects.requireNonNull(defaults.getConfigurationSection(prefix),prefix);
            Map<String,Double> values=new HashMap<>();
            for(String key:section.getKeys(false)){
                Object raw=config.get(prefix+"."+key);
                if(!(raw instanceof Number number))throw new IllegalArgumentException(prefix+"."+key+" must be numeric");
                double v=number.doubleValue();
                double min=PERCENT.contains(key)||INTEGER.contains(key)?0:.05;
                double max=PERCENT.contains(key)?100:INTEGER.contains(key)?101:5;
                if(!Double.isFinite(v)||v<min||v>max||(PERCENT.contains(key)||INTEGER.contains(key))&&v!=Math.rint(v))throw new IllegalArgumentException("Invalid "+prefix+"."+key+"="+v);
                values.put(key,v);
            }
            String revision;
            try{revision=HexFormat.of().formatHex(java.security.MessageDigest.getInstance("SHA-256").digest(new TreeMap<>(values).toString().getBytes(StandardCharsets.UTF_8))).substring(0,16);}
            catch(java.security.NoSuchAlgorithmException impossible){throw new IllegalStateException(impossible);}
            Profile p=new Profile(Map.copyOf(values),revision);
            if(p.integer("armor-max")>4||p.integer("armor-min")>p.integer("armor-max")||p.integer("protection")>4||p.integer("power")>5||p.integer("sharpness")>5||p.integer("quick-charge")>3||p.integer("piercing")>4||p.integer("creeper-fuse")<10||p.integer("armor-iron")+p.integer("armor-diamond")+p.integer("armor-netherite")>100||p.integer("weapon-diamond")+p.integer("weapon-netherite")>100)throw new IllegalArgumentException("Invalid equipment combination in "+prefix);
            profiles.put(preset,p);
        }
        config.save(file);
    }
    public Profile get(InfernalDifficulties.Preset preset){return profiles.get(preset);}
}
