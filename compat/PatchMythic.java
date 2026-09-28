import java.nio.file.*;
import java.util.zip.*;
import org.objectweb.asm.*;

/** Reproducible, narrowly scoped binary compatibility patch for the supplied JAR. */
public final class PatchMythic {
    static final String NMS = "io/lumine/mythic/bukkit/utils/version/NMSVersion";
    static final String MC = "io/lumine/mythic/bukkit/utils/version/MinecraftVersion";
    public static void main(String[] args) throws Exception {
        String sha = java.util.HexFormat.of().formatHex(java.security.MessageDigest.getInstance("SHA-256")
            .digest(Files.readAllBytes(Path.of(args[0]))));
        if (!sha.equals("0906a5d1e7927b1f628e3b36bda4c0ea155ec6da2d3997b88e3e41455c2ee05a"))
            throw new IllegalArgumentException("Input does not match the tested upstream JAR.");
        int[] changes = {0, 0, 0};
        try (ZipFile input = new ZipFile(args[0]);
             ZipOutputStream output = new ZipOutputStream(Files.newOutputStream(Path.of(args[1])))) {
            var entries = input.entries();
            while (entries.hasMoreElements()) {
                var entry = entries.nextElement();
                byte[] bytes = input.getInputStream(entry).readAllBytes();
                if (entry.getName().equals(NMS + ".class")) {
                    ClassReader reader = new ClassReader(bytes);
                    ClassWriter writer = new ClassWriter(reader, ClassWriter.COMPUTE_MAXS);
                    reader.accept(new ClassVisitor(Opcodes.ASM9, writer) {
                        @Override public MethodVisitor visitMethod(int a, String n, String d, String s, String[] e) {
                            MethodVisitor base = super.visitMethod(a, n, d, s, e);
                            if (!n.equals("<clinit>")) return base;
                            return new MethodVisitor(Opcodes.ASM9, base) {
                                @Override public void visitInsn(int opcode) {
                                    if (opcode == Opcodes.RETURN) {
                                        // Only the observed 26.3.0 is mapped; unknown future versions still fail closed.
                                        super.visitTypeInsn(Opcodes.NEW, "java/util/HashMap");
                                        super.visitInsn(Opcodes.DUP);
                                        super.visitFieldInsn(Opcodes.GETSTATIC, NMS, "MC_TO_NMS", "Ljava/util/Map;");
                                        super.visitMethodInsn(Opcodes.INVOKESPECIAL, "java/util/HashMap", "<init>", "(Ljava/util/Map;)V", false);
                                        super.visitFieldInsn(Opcodes.PUTSTATIC, NMS, "MC_TO_NMS", "Ljava/util/Map;");
                                        super.visitFieldInsn(Opcodes.GETSTATIC, NMS, "MC_TO_NMS", "Ljava/util/Map;");
                                        super.visitIntInsn(Opcodes.BIPUSH, 26);
                                        super.visitInsn(Opcodes.ICONST_3);
                                        super.visitInsn(Opcodes.ICONST_0);
                                        super.visitMethodInsn(Opcodes.INVOKESTATIC, MC, "of", "(III)L" + MC + ";", false);
                                        super.visitFieldInsn(Opcodes.GETSTATIC, NMS, "v26_2", "L" + NMS + ";");
                                        super.visitMethodInsn(Opcodes.INVOKEINTERFACE, "java/util/Map", "put", "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;", true);
                                        super.visitInsn(Opcodes.POP);
                                        super.visitFieldInsn(Opcodes.GETSTATIC, NMS, "MC_TO_NMS", "Ljava/util/Map;");
                                        super.visitMethodInsn(Opcodes.INVOKESTATIC, "java/util/Collections", "unmodifiableMap", "(Ljava/util/Map;)Ljava/util/Map;", false);
                                        super.visitFieldInsn(Opcodes.PUTSTATIC, NMS, "MC_TO_NMS", "Ljava/util/Map;");
                                        changes[0]++;
                                    }
                                    super.visitInsn(opcode);
                                }
                            };
                        }
                    }, 0);
                    bytes = writer.toByteArray();
                }
                if (entry.getName().startsWith("io/lumine/mythic/core/volatilecode/v26_2/") && entry.getName().endsWith(".class")) {
                    int before = changes[1] + changes[2];
                    ClassReader reader = new ClassReader(bytes);
                    ClassWriter writer = new ClassWriter(reader, 0);
                    reader.accept(new ClassVisitor(Opcodes.ASM9, writer) {
                        @Override public MethodVisitor visitMethod(int a, String n, String d, String s, String[] e) {
                            return new MethodVisitor(Opcodes.ASM9, super.visitMethod(a,n,d,s,e)) {
                                @Override public void visitMethodInsn(int op, String owner, String name, String desc, boolean itf) {
                                    if (owner.equals("net/minecraft/network/protocol/game/ClientboundRemoveEntitiesPacket") && name.equals("getEntityIds")) {
                                        name = "entityIds";
                                        changes[1]++;
                                    }
                                    if (owner.equals("net/minecraft/network/RegistryFriendlyByteBuf") && name.equals("writeCollection")
                                        && desc.equals("(Ljava/util/Collection;Lnet/minecraft/network/codec/StreamEncoder;)V")) {
                                        op = Opcodes.INVOKESTATIC;
                                        owner = "local/mythic/compat/BufferCompat";
                                        desc = "(Lnet/minecraft/network/RegistryFriendlyByteBuf;Ljava/util/Collection;Lnet/minecraft/network/codec/StreamEncoder;)V";
                                        itf = false;
                                        changes[2]++;
                                    }
                                    super.visitMethodInsn(op, owner, name, desc, itf);
                                }
                            };
                        }
                    }, 0);
                    if (changes[1] + changes[2] != before) bytes = writer.toByteArray();
                }
                if (entry.getName().equals("plugin.yml")) {
                    bytes = new String(bytes, java.nio.charset.StandardCharsets.UTF_8)
                        .replace("5.13.0-aad3f1c9", "5.13.0-local263-r2")
                        .getBytes(java.nio.charset.StandardCharsets.UTF_8);
                }
                ZipEntry result = new ZipEntry(entry.getName());
                result.setTime(0);
                output.putNextEntry(result);
                output.write(bytes);
                output.closeEntry();
            }
            ZipEntry helper = new ZipEntry("local/mythic/compat/BufferCompat.class");
            helper.setTime(0);
            output.putNextEntry(helper);
            output.write(Files.readAllBytes(Path.of(".tools/compat-classes/local/mythic/compat/BufferCompat.class")));
            output.closeEntry();
        }
        if (changes[0] != 1 || changes[1] != 1 || changes[2] < 1) throw new IllegalStateException("Unexpected upstream structure: " + java.util.Arrays.toString(changes));
        System.out.println("Patched mapping, removal accessor, collection writes: " + java.util.Arrays.toString(changes));
        System.out.println("Created experimental 26.3 compatibility JAR; runtime validation required.");
    }
}
