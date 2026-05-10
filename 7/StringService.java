import java.rmi.Remote;
import java.rmi.RemoteException;

public interface StringService extends Remote {
    String concatenate(String a, String b) throws RemoteException;
}

// Explanation
// This is the remote interface
// It contains the method the client can call remotely
// RemoteException is required in RMI