# We will need the following module to generate randomized lost packets
   # import random
from socket import *

    # Create a UDP socket
    # Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

    # Assign IP address and port number to socket
serverSocket.bind(('', 4444))
#serverSocket.listen(1)
conn,addr=serverSocket.accept()
print ('TEST',addr)
while True:
        # Generate random number in the range of 0 to 10
        # rand = random.randint(0, 10)

        # Receive the client packet along with the address it is coming from
	message = conn.recv(1024)
        # Capitalize the message from the client
        #message = message.upper()
        # If rand is less is than 4, we consider the packet lost and do notrespond
       # if rand < 4:
         #   continue

        # Otherwise, the server responds
        #serverSocket.sendto(message, address)
	print (message)
	print ('hello')
conn.close()
