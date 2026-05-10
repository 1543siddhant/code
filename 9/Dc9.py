# HotelBooking.java

# import java.rmi.Remote;
# import java.rmi.RemoteException;

# public interface HotelBooking extends Remote {
#     // Book a room for a specific guest
#     String bookRoom(String guestName, int roomNumber) throws RemoteException;
    
#     // Cancel a booking for a specific guest
#     String cancelBooking(String guestName) throws RemoteException;
    
#     // Get current bookings (for demonstration)
#     String listBookings() throws RemoteException;
# }


# // Steps to run
# // javac *.java
# // rmiregistry
# // start rmiregistry
# // java HotelBookingServer
# // java HotelBookingClient






# ------------------------------------------------------------

# import java.rmi.Naming;
# import java.util.Scanner;

# public class HotelBookingClient {
#     public static void main(String[] args) {
#         try {
#             // Look up the remote object in the RMI registry
#             HotelBooking hotel = (HotelBooking) Naming.lookup("rmi://localhost/HotelBookingService");
            
#             Scanner scanner = new Scanner(System.in);
            
#             while (true) {
#                 System.out.println("\nHotel Booking System");
#                 System.out.println("1. Book a room");
#                 System.out.println("2. Cancel booking");
#                 System.out.println("3. View current bookings");
#                 System.out.println("4. Exit");
#                 System.out.print("Enter your choice: ");
                
#                 int choice = scanner.nextInt();
#                 scanner.nextLine(); // consume newline
                
#                 switch (choice) {
#                     case 1:
#                         System.out.print("Enter guest name: ");
#                         String guestName = scanner.nextLine();
#                         System.out.print("Enter room number (1-10): ");
#                         int roomNumber = scanner.nextInt();
#                         System.out.println(hotel.bookRoom(guestName, roomNumber));
#                         break;
#                     case 2:
#                         System.out.print("Enter guest name to cancel booking: ");
#                         String cancelName = scanner.nextLine();
#                         System.out.println(hotel.cancelBooking(cancelName));
#                         break;
#                     case 3:
#                         System.out.println(hotel.listBookings());
#                         break;
#                     case 4:
#                         System.out.println("Exiting...");
#                         scanner.close();
#                         System.exit(0);
#                     default:
#                         System.out.println("Invalid choice");
#                 }
#             }
#         } catch (Exception e) {
#             System.err.println("Client exception: " + e.toString());
#             e.printStackTrace();
#         }
#     }
# }




# -------------------------------------------------------


# import java.rmi.RemoteException;
# import java.rmi.server.UnicastRemoteObject;
# import java.util.HashMap;
# import java.util.Map;

# public class HotelBookingServer extends UnicastRemoteObject implements HotelBooking {
#     private Map<Integer, String> bookings; // room number to guest name mapping
#     private static final int TOTAL_ROOMS = 10; // assuming hotel has 10 rooms
    
#     public HotelBookingServer() throws RemoteException {
#         super();
#         bookings = new HashMap<>();
#     }
    
#     @Override
#     public String bookRoom(String guestName, int roomNumber) throws RemoteException {
#         if (roomNumber < 1 || roomNumber > TOTAL_ROOMS) {
#             return "Invalid room number. Please choose between 1 and " + TOTAL_ROOMS;
#         }
        
#         if (bookings.containsKey(roomNumber)) {
#             return "Room " + roomNumber + " is already booked by " + bookings.get(roomNumber);
#         }
        
#         bookings.put(roomNumber, guestName);
#         return "Room " + roomNumber + " successfully booked for " + guestName;
#     }
    
#     @Override
#     public String cancelBooking(String guestName) throws RemoteException {
#         for (Map.Entry<Integer, String> entry : bookings.entrySet()) {
#             if (entry.getValue().equals(guestName)) {
#                 bookings.remove(entry.getKey());
#                 return "Booking canceled for " + guestName;
#             }
#         }
#         return "No booking found for " + guestName;
#     }
    
#     @Override
#     public String listBookings() throws RemoteException {
#         if (bookings.isEmpty()) {
#             return "No current bookings";
#         }
        
#         StringBuilder sb = new StringBuilder();
#         sb.append("Current Bookings:\n");
#         for (Map.Entry<Integer, String> entry : bookings.entrySet()) {
#             sb.append("Room ").append(entry.getKey()).append(": ").append(entry.getValue()).append("\n");
#         }
#         return sb.toString();
#     }
    
#     public static void main(String[] args) {
#         try {
#             // Create and export the server object
#             HotelBookingServer server = new HotelBookingServer();
            
#             // Bind the server object to the RMI registry
#             java.rmi.Naming.rebind("HotelBookingService", server);
            
#             System.out.println("Hotel Booking Server is ready...");
#         } catch (Exception e) {
#             System.err.println("Server exception: " + e.toString());
#             e.printStackTrace();
#         }
#     }
# }