class RoundRobin:
    def __init__(self, servers):
        self.servers = servers
        self.index = 0

    def get_server(self, request):
        server = self.servers[self.index]
        self.index = (self.index + 1) % len(self.servers)
        return server

# Usage
servers = ["Server_A", "Server_B", "Server_C"]
lb = RoundRobin(servers)
for i in range(5):
    print(f"Request {i} -> {lb.get_server(i)}")
    

#Weighted RR   
class WeightedRoundRobin:
    def __init__(self, server_weights):
        self.pool = []
        for server, weight in server_weights.items():
            self.pool.extend([server] * weight)
        self.index = 0

    def get_server(self, request):
        server = self.pool[self.index]
        self.index = (self.index + 1) % len(self.pool)
        return server

# Usage
lb = WeightedRoundRobin({"Powerhouse": 3, "Old_PC": 1})
for i in range(4):
    print(f"Request {i} -> {lb.get_server(i)}")
    
    
#3. Least Connections
class LeastConnections:
    def __init__(self, servers):
        # Tracking {server_name: active_connections}
        self.connections = {server: 0 for server in servers}

    def get_server(self, request):
        # Pick the server with the minimum current connections
        best_server = min(self.connections, key=self.connections.get)
        self.connections[best_server] += 1
        return best_server

    def release_server(self, server):
        self.connections[server] -= 1

# Usage
lb = LeastConnections(["Server_1", "Server_2"])
selected = lb.get_server("req1")
print(f"Routing to: {selected}")


#4. IP Hashing
import hashlib

class IPHashing:
    def __init__(self, servers):
        self.servers = servers

    def get_server(self, client_ip):
        # Hash the IP and map it to a server index
        hash_val = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        index = hash_val % len(self.servers)
        return self.servers[index]

# Usage
lb = IPHashing(["Server_X", "Server_Y"])
print(f"User 192.168.1.1 -> {lb.get_server('192.168.1.1')}")
print(f"User 192.168.1.1 -> {lb.get_server('192.168.1.1')}") # Always the same   
