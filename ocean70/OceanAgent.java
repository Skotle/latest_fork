import java.lang.instrument.*;
import java.security.ProtectionDomain;
import org.objectweb.asm.*;

/** Kept separate so the target server class is not resolved before transformer registration. */
public class OceanAgent {
    public static void premain(String args, Instrumentation instrumentation) {
        instrumentation.addTransformer(new ClassFileTransformer() {
            public byte[] transform(ClassLoader loader, String name, Class<?> cls,
                                    ProtectionDomain pd, byte[] bytes) {
                if (!name.equals("net/minecraft/server/MinecraftServer")) return null;
                ClassReader reader = new ClassReader(bytes);
                ClassWriter writer = new ClassWriter(reader, ClassWriter.COMPUTE_MAXS);
                reader.accept(new ClassVisitor(Opcodes.ASM9, writer) {
                    public MethodVisitor visitMethod(int access, String name, String desc, String sig, String[] ex) {
                        MethodVisitor visitor = super.visitMethod(access, name, desc, sig, ex);
                        if (!name.equals("tickServer")) return visitor;
                        return new MethodVisitor(Opcodes.ASM9, visitor) {
                            public void visitCode() {
                                super.visitCode();
                                visitVarInsn(Opcodes.ALOAD, 0);
                                visitMethodInsn(Opcodes.INVOKESTATIC, "OceanProbe", "onTick", "(Ljava/lang/Object;)V", false);
                            }
                        };
                    }
                }, 0);
                System.out.println("OCEAN70 installed server sampler");
                return writer.toByteArray();
            }
        });
    }
}
