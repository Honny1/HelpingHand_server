
import socket
import sys
import argparse

parser = argparse.ArgumentParser()

parser.set_defaults(listmode=0)
parser.add_argument("--name",default="ON", action="store")
options = parser.parse_args()



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.2.148', 8882)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

    # Send data
    message = str.encode(options.name)
    print('sending {!r}'.format(message))
    sock.sendall(message)

finally:
    print('closing socket')
    sock.close()
