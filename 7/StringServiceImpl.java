import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class StringServiceImpl extends UnicastRemoteObject implements StringService {

    public StringServiceImpl() throws RemoteException {
        super();
    }

    public String concatenate(String a, String b) throws RemoteException {
        return a + b;
    }
}

// Explanation
// This class provides the actual logic
// It extends UnicastRemoteObject so it can work as a remote object
// The concatenate() method joins both strings