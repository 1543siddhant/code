# # StringClient.java

# import java.rmi.registry.LocateRegistry;
# import java.rmi.registry.Registry;
# import java.util.Scanner;

# public class StringClient {
#     public static void main(String[] args) {
#         try {
#             Registry registry = LocateRegistry.getRegistry("localhost", 1099);
#             StringService service = (StringService) registry.lookup("StringService");

#             Scanner sc = new Scanner(System.in);
#             System.out.print("Enter first string: ");
#             String s1 = sc.nextLine();

#             System.out.print("Enter second string: ");
#             String s2 = sc.nextLine();

#             String result = service.concatenate(s1, s2);
#             System.out.println("Concatenated String: " + result);

#             sc.close();
#         } catch (Exception e) {
#             System.out.println("Client error: " + e);
#         }
#     }
# }

# // Explanation
# // Connects to the server registry
# // Finds the remote service
# // Sends two strings
# // Receives the concatenated result

# ------------------------------------------------------------------

# # StringServer.java

# import java.rmi.registry.LocateRegistry;
# import java.rmi.registry.Registry;

# public class StringServer {
#     public static void main(String[] args) {
#         try {
#             LocateRegistry.createRegistry(1099);   // Start RMI registry

#             StringService service = new StringServiceImpl();
#             Registry registry = LocateRegistry.getRegistry();

#             registry.rebind("StringService", service);

#             System.out.println("Server is running...");
#         } catch (Exception e) {
#             System.out.println("Server error: " + e);
#         }
#     }
# }

# # // Explanation
# # // Starts the RMI registry on port 1099
# # // Creates the remote object
# # // Registers it with the name StringService
# # // Server waits for client requests

# # // javac StringService.java StringServiceImpl.java StringServer.java StringClient.java

# # // Design a distributed application using RMI for remote computation where client submits two
# # // strings to the server and server returns the concatenation of the given strings
# # // Definition of RPC
# # // RPC (Remote Procedure Call) is a distributed computing technique where a client calls a function on a remote server as if it were a local function.
# # // Example:
# # // Client sends a number
# # // Server calculates factorial
# # // Server returns result
# # // Definition of RMI

# # // RMI (Remote Method Invocation) is Java’s distributed computing mechanism that allows one Java program to invoke methods of another Java object located remotely.
# # // Example:
# # // Client sends two strings
# # // Server concatenates strings
# # // Returns result
# # // Difference Between RPC and RMI
# # // Feature	RPC	RMI
# # // Full Form	Remote Procedure Call	Remote Method Invocation
# # // Language Support	Multiple languages	Only Java
# # // Communication	Function based	Object based
# # // Complexity	Simple	More advanced
# # // Object Passing	Not supported directly	Supports objects
# # // Platform	Cross-platform	Java platform
# # // Usage	Procedural programming	Object-oriented programming
# # // Why RMI is Only for Java?
# # // RMI uses:
# # // Java classes
# # // Java objects
# # // JVM (Java Virtual Machine)
# # // Java serialization
# # // Since other languages do not understand Java bytecode and serialization directly, RMI works mainly between Java applications.

# # // Which is Better?
# # // RPC

# # // Better when:

# # // Simple applications
# # // Cross-language communication needed
# # // Faster and lightweight systems
# # // RMI

# # // Better when:

# # // Pure Java applications
# # // Object-oriented distributed systems
# # // Need to transfer objects remotely

# ------------------------------------------------------------------

# # StringService.java
# import java.rmi.Remote;
# import java.rmi.RemoteException;

# public interface StringService extends Remote {
#     String concatenate(String a, String b) throws RemoteException;
# }

# // Explanation
# // This is the remote interface
# // It contains the method the client can call remotely
# // RemoteException is required in RMI

# --------------------------------------------------------------------------

# StringServiceImpl.java

# import java.rmi.RemoteException;
# import java.rmi.server.UnicastRemoteObject;

# public class StringServiceImpl extends UnicastRemoteObject implements StringService {

#     public StringServiceImpl() throws RemoteException {
#         super();
#     }

#     public String concatenate(String a, String b) throws RemoteException {
#         return a + b;
#     }
# }

# # // Explanation
# # // This class provides the actual logic
# # // It extends UnicastRemoteObject so it can work as a remote object
# # // The concatenate() method joins both strings
