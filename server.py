import socket
from threading import Thread
from cryptography.fernet import Fernet

BUFFER_SIZE = 1024

class Server:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname()) # Change to server host
        self.port = 8000 # Change to server port
        
        self.key = Fernet.generate_key()
        self.cipherSuite = Fernet(self.key)

    def handle_client(self, client_socket, client_addr):
        print(f"[*] New Connection: {client_addr} connected.")
        while True:
            data = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            if not data:
                break
            username, password = data.split(":")
            if username == "username" and password == "password":
                client_socket.send("True").encode("utf-8")
            else:
                client_socket.send("False").encode("utf-8")
        client_socket.close()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp:
            server_tcp.bind((self.host, self.port))
            server_tcp.listen(6)
            print('[*] Waiting for connection')
            while True:
                connection, addr = server_tcp.accept()
                print(f'[*] Established connection from IP {addr[0]} port : {addr[1]}')
                thread = Thread(target=self.handle_client, args=(connection, addr))
                thread.start()

if __name__ == "__main__":
    s = Server()
    s.start()
