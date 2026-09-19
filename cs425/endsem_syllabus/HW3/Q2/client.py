from socket import *

# Server details
serverName = "localhost"
serverPort = 12000

# Create UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

try:
    while True:
        # Take input from user
        message = input("Enter a sentence (type 'exit' to quit): ")

        if message.lower() == "exit":
            break

        # Send message to server
        clientSocket.sendto(message.encode(), (serverName, serverPort))

        # Receive response from server
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)

        print("Reply from server:", modifiedMessage.decode())

finally:
    # Close socket
    clientSocket.close()
    print("Client socket closed.")

