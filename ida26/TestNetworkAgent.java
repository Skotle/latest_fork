import java.lang.instrument.*;
import java.security.ProtectionDomain;
import org.objectweb.asm.*;

/** Test-only: run the real server's world and console without opening a TCP listener. */
public class TestNetworkAgent {
 public static void premain(String args, Instrumentation inst) {
  inst.addTransformer(new ClassFileTransformer() {
   public byte[] transform(ClassLoader loader, String name, Class<?> c, ProtectionDomain pd, byte[] bytes) {
    if (!name.equals("net/minecraft/server/network/ServerConnectionListener")) return null;
    ClassReader r=new ClassReader(bytes); ClassWriter w=new ClassWriter(0);
    r.accept(new ClassVisitor(Opcodes.ASM9,w) {
     public MethodVisitor visitMethod(int access,String n,String d,String s,String[] ex) {
      if (n.equals("startTcpServerListener")) {
       MethodVisitor m=super.visitMethod(access,n,d,s,ex);m.visitCode();m.visitInsn(Opcodes.RETURN);m.visitMaxs(0,3);m.visitEnd();return null;
      }
      return super.visitMethod(access,n,d,s,ex);
     }
    },0);
    System.out.println("[IDA test] TCP listener disabled by test agent");return w.toByteArray();
   }
  });
 }
}
