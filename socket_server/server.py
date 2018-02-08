import socket
import sys
import threading

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            connection, client_address = self.sock.accept()
            connection.settimeout(60)
            data = connection.recv(16)
            threading.Thread(target = self.listenToClient,args = (connection)).start()

    def listenToClient(self, client):
        size = 1024
        while True:
            try:
                if data:
                    if data == b'ON':
                        print("ON")
                        connection.sendall(b'o')
                    elif data == b'OFF':
                        print("OFF")
                        connection.sendall(b'f')

            except:
                client.close()
                return False

if __name__ == "__main__":
    while True:
        ThreadedServer('192.168.2.148',8882).listen()


