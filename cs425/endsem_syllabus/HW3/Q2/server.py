from socket import *

# Server configuration
serverPort = 12000

# Create UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Bind socket to localhost and port
serverSocket.bind(("localhost", serverPort))

print("UDP Server is ready to receive...")

while True:
    # Receive message from client
    message, clientAddress = serverSocket.recvfrom(1024)

    print("Connection established with:", clientAddress)
    print("Received from client:", message.decode())

    # Process message (convert to uppercase)
    modifiedMessage = message.decode().upper()

    # Send response back to client
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)

