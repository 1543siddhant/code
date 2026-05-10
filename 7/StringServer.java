import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class StringServer {
    public static void main(String[] args) {
        try {
            LocateRegistry.createRegistry(1099);   // Start RMI registry

            StringService service = new StringServiceImpl();
            Registry registry = LocateRegistry.getRegistry();

            registry.rebind("StringService", service);

            System.out.println("Server is running...");
        } catch (Exception e) {
            System.out.println("Server error: " + e);
        }
    }
}

// Explanation
// Starts the RMI registry on port 1099
// Creates the remote object
// Registers it with the name StringService
// Server waits for client requests

// javac StringService.java StringServiceImpl.java StringServer.java StringClient.java

// Design a distributed application using RMI for remote computation where client submits two
// strings to the server and server returns the concatenation of the given strings
// Definition of RPC
// RPC (Remote Procedure Call) is a distributed computing technique where a client calls a function on a remote server as if it were a local function.
// Example:
// Client sends a number
// Server calculates factorial
// Server returns result
// Definition of RMI

// RMI (Remote Method Invocation) is Java’s distributed computing mechanism that allows one Java program to invoke methods of another Java object located remotely.
// Example:
// Client sends two strings
// Server concatenates strings
// Returns result
// Difference Between RPC and RMI
// Feature	RPC	RMI
// Full Form	Remote Procedure Call	Remote Method Invocation
// Language Support	Multiple languages	Only Java
// Communication	Function based	Object based
// Complexity	Simple	More advanced
// Object Passing	Not supported directly	Supports objects
// Platform	Cross-platform	Java platform
// Usage	Procedural programming	Object-oriented programming
// Why RMI is Only for Java?
// RMI uses:
// Java classes
// Java objects
// JVM (Java Virtual Machine)
// Java serialization
// Since other languages do not understand Java bytecode and serialization directly, RMI works mainly between Java applications.

// Which is Better?
// RPC

// Better when:

// Simple applications
// Cross-language communication needed
// Faster and lightweight systems
// RMI

// Better when:

// Pure Java applications
// Object-oriented distributed systems
// Need to transfer objects remotely