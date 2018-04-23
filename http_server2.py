import select
from socket import *
import os.path
import sys
import Queue

serverPort = int(sys.argv[1])


# (1) Create a TCP socket on which to listen for new connections
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setblocking(0)
# (2) Bind that socket to the port provided on the command line
serverSocket.bind(('', serverPort))
# (3) Listen on the accept socket
serverSocket.listen(5)

print('The server is ready to receive')

sockIn = [serverSocket]
sockOut = []

# (4) Do the following repeatedly:
while True:
    readable, writable, exceptions = select.select(sockIn, sockOut, sockIn)

    for r in readable:
        if r is serverSocket:
            # (a) Accept a new connection on the accept socket
            connectionSocket, addr = serverSocket.accept()
            print >> sys.stderr, "New connection from ", connectionSocket
            connectionSocket.setblocking(0)
            sockIn.append(connectionSocket)
        else:
            # (b) Read the HTTP request from the connection socket and parse it
            response = r.recv(1024).decode()
            index = response.find("GET")
            #Prevents requests from being processed if response is empty
            if (response):
                newResponse = ""
                for i in response[index+5:]:
                    if i not in [" ","\\","\n","\r"]:
                        newResponse += i
                    else:
                        break
                # (c) Check to see if the requested file requested exists (and ends with ".htm" or ".html")

                # (d) If the file exists, construct the appropriate HTTP response, write the HTTP header to the connection
                # socket, and then open the file and write its contents to the connection socket

                # (e) If the file doesn't exist, construct a HTTP error response (404 Not Found) and write
                # it to the connection socket.  If the file does exist, but does not end with ".htm" or "html",
                # then write a "403 Forbidden" error response
                header = ""
                if os.path.exists((newResponse.encode())):
                    if not(newResponse.endswith("html") or newResponse.endswith("htm")):
                        # 403
                        header = "HTTP/1.1 403 Forbidden\n" + "Content-Type: text/html\r\n\r\n"
                        r.send(header)
                        print('ERROR: 403 Forbidden')
                    else:
                        # 200
                        header = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\r\n\r\n"
                        data = open(newResponse.encode(), 'r')
                        everything = ""
                        for d in data:
                            everything = everything + d
                        everything = header + everything
                        r.send(everything)
                        print('200 OK')
                elif not(os.path.exists((newResponse.encode()))):
                    # 404
                    header = "HTTP/1.1 404 Not Found\n" + "Content-Type: text/html\r\n\r\n"
                    r.send(header)
                    print('ERROR: 404 Not Found')
            # (f) Close the connection socket
            sockIn.remove(r)
            r.close()