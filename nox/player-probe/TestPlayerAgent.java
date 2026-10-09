import java.lang.instrument.*;
import java.security.ProtectionDomain;
import org.objectweb.asm.*;

/** Test-only: network is disabled and an in-process ServerPlayer is registered. */
public class TestPlayerAgent {
    public static void premain(String args, Instrumentation inst) {
        TestNetworkAgent.premain(args, inst);
        inst.addTransformer(new ClassFileTransformer() {
            public byte[] transform(ClassLoader loader, String name, Class<?> redef,
                                    ProtectionDomain domain, byte[] data) {
                if (!name.equals("net/minecraft/server/MinecraftServer")) return null;
                ClassReader reader = new ClassReader(data);
                ClassWriter writer = new ClassWriter(reader, ClassWriter.COMPUTE_MAXS);
                reader.accept(new ClassVisitor(Opcodes.ASM9, writer) {
                    public MethodVisitor visitMethod(int access, String method, String desc,
                                                     String signature, String[] exceptions) {
                        MethodVisitor base = super.visitMethod(access, method, desc, signature, exceptions);
                        if (!method.equals("tickChildren")) return base;
                        return new MethodVisitor(Opcodes.ASM9, base) {
                            public void visitInsn(int opcode) {
                                if (opcode == Opcodes.RETURN) {
                                    visitVarInsn(Opcodes.ALOAD, 0);
                                    visitMethodInsn(Opcodes.INVOKESTATIC, "PlayerProbe", "tick",
                                        "(Lnet/minecraft/server/MinecraftServer;)V", false);
                                }
                                super.visitInsn(opcode);
                            }
                        };
                    }
                }, 0);
                return writer.toByteArray();
            }
        });
    }
}
