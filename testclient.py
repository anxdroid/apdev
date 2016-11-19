import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 82)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
try:
    
    # Send data
    message = 'AUTH:f_Yhkoljlj43_.'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)
    
    #while amount_received < amount_expected:
    data = sock.recv(1024)
    print >>sys.stderr, 'received "%s"' % data

    while True:
        message = raw_input("Enter something: ")

        if (message != "") :
            # Send data
            #message = 'RELAY:LOW'
            print >>sys.stderr, 'sending "%s"' % message
            sock.sendall(message)
    
            #while amount_received < amount_expected:
            data = sock.recv(1024)
            print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()