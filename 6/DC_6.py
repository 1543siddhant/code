
# Design a distributed application using RPC for remote computation where client submits an
# integer value to the server and server calculates factorial and returns the result to the client
# program

from xmlrpc.server import SimpleXMLRPCServer
server = SimpleXMLRPCServer(("localhost", 54657))

@server.register_function
def factorial(n):
    if n < 0:
        return "Error: Factorial of negative number not possible"

    result = 1
    for i in range(1, n + 1):
        result *= i

    return str(result)

print("RPC Server running on port 1234...")
server.serve_forever()

# Checkports-netstat -ano


import xmlrpc.client
server = xmlrpc.client.ServerProxy("http://localhost:54657/")

num = int(input("Enter a number: "))
result = server.factorial(num)
print("Factorial received from server:", result)