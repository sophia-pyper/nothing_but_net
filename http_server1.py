# HTTP Server 
import sys
from socket import *
serverPort = int(sys.argv[1])

# (1) Create a TCP socket on which to listen for new connections
serverSocket = socket(AF_INET,SOCK_STREAM)
# (2) Bind that socket to the port provided on the command line
serverSocket.bind(('', serverPort))
# (3) Listen on the accept socket
serverSocket.listen(1)
print('The server is ready to receive')

# (4) Do the following repeatedly:
while True:
    # (a) Accept a new connection on the accept socket
    connectionSocket, addr = serverSocket.accept()
    if not connectionSocket:
        break 
    # (b) Read the HTTP request from the connection socket and parse it
    sentence = connectionSocket.recv(1024).decode()
    # (c) Check to see if the requested file requested exists (and ends with ".htm" or ".html")
    
    
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    # (f) Close the connection socket
    connectionSocket.close()
