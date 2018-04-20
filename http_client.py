import socket, sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = sys.argv[1]
port = 80
getMessage = "GET /index.html HTTP/1.0"


if ("http://" not in addr):
    print "Error: please pass a valid address beginning with 'http://'"
    sys.exit(-1)

addr = addr[7:]
hasPort = addr.find(":")
if (hasPort != -1):
    port = int(addr[hasPort+1:])
    addr = addr[:hasPort]

slash = addr.find("/")
if (slash != -1):
    pageRequest = addr[slash:]
    addr = addr[:slash]
    if (len(pageRequest) > 1):
        getMessage = "GET "+pageRequest+" HTTP/1.0"

s.connect(addr, port)

s.send(getMessage)

