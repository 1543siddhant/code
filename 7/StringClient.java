import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Scanner;

public class StringClient {
    public static void main(String[] args) {
        try {
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
            StringService service = (StringService) registry.lookup("StringService");

            Scanner sc = new Scanner(System.in);
            System.out.print("Enter first string: ");
            String s1 = sc.nextLine();

            System.out.print("Enter second string: ");
            String s2 = sc.nextLine();

            String result = service.concatenate(s1, s2);
            System.out.println("Concatenated String: " + result);

            sc.close();
        } catch (Exception e) {
            System.out.println("Client error: " + e);
        }
    }
}

// Explanation
// Connects to the server registry
// Finds the remote service
// Sends two strings
// Receives the concatenated result