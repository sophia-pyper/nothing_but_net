import socket, sys

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = sys.argv[1]
    requestInfo = parseURL(addr)
    response = getMessageFromServer(client, requestInfo[0], requestInfo[1],requestInfo[2])
    statusCode = int(getStatusCode(response))

    #Handle redirect statuses first
    redirectCounter = 0
    while (statusCode == 301) or (statusCode == 302):
        #increment counter and kill function if there are too many redirects
        redirectCounter += 1
        if (redirectCounter >= 10):
            sys.stderr.write("Error: too many redirects.")
            client.close()
            sys.exit(-1)
        #Otherwise, get new URL and try again
        else:
            newIndex = response.find("Location:")
            newURL = ""
            for i in response[newIndex+10:]:
                if i not in [" ","\\","\n","\r"]:
                    newURL += i
                else:
                    break
            newMessage = "Redirecting to "+ newURL+"\n"
            sys.stdout.write(newMessage)
            client.close()
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            newRequest = parseURL(newURL)
            response = getMessageFromServer(client, newRequest[0], newRequest[1],newRequest[2])
            statusCode = int(getStatusCode(response))

    #Once redirects are handled, if we get a good page, process text
    if (statusCode == 200):
        #If content type is correct, output html and close
        if "Content-Type: text/html" in response:
            startIndex = response.find("<")
            sys.stdout.write(response[startIndex:])
            client.close()
            sys.exit(0)
        #Otherwise, output error message and close
        else:
            sys.stderr.write("Error: Page returned a non-text/html content-type")
            client.close()
            sys.exit(-1)

    elif (statusCode >= 400):
        sys.stdout.write(response)
        client.close()
        sys.exit(-1)

    else:
        errMessage = "Received unexpected error code "+ str(statusCode)
        sys.stderr.write(errMessage)
        client.close()
        sys.exit(-1)


#Takes in URL and returns tuple containing [parsed URL, port, get message]
def parseURL(url):
    #establishes default port and get request
    port = 80
    getMessage = "GET / HTTP/1.0\r\nHost: "
    #Check whether address is http, kill program if not
    if "http://" not in url:
        sys.stderr.write("Error: address does not begin with 'http://'")
        sys.exit(-1)

    #Next, removes http from address string
    url = url[7:]

    #Checks whether address has page specified
    slash = url.find("/")
    if (slash != -1):
        pageRequest = url[slash:]
        url = url[:slash]
        if (len(pageRequest) > 1):
            getMessage = "GET "+pageRequest+" HTTP/1.0\r\nHost: "

    #Checks whether address has port and saves port
    hasPort = url.find(":")
    if (hasPort != -1):
        port = int(url[hasPort+1:])
        url = url[:hasPort]

    #Adds parsed address as host
    newMessage = getMessage+url+"\r\n\r\n"
    return [url, port, newMessage]

#Sends get message to the server via socket. Returns server response
def getMessageFromServer(sock, url, port, message):
    #Connects to server and sends get request
    sock.connect((url, port))
    sock.send(message)

    #Keeps receiving as long as the server keeps sending
    response = ""
    while True:
        servRes = sock.recv(1024)
        if not servRes:
            break
        response += servRes
    return response

def getStatusCode(res):
    return res[9:12]

main()
