import socket
from threading import Thread
from cryptography.fernet import Fernet
import os

BUFFER_SIZE = 1024

USER_DB = {
    "username": "password"
}

SESSIONS = {}

class Server:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname()) # Change to server host
        self.port = 8000 # Change to server port
        
        self.key = Fernet.generate_key()
        self.cipherSuite = Fernet(self.key)

    def authenticate(self, username, password):
        return USER_DB.get(username) == password

    def handle_client(self, client_socket, client_addr):
        session_id = None
        authenticated = False

        while True:
            data = self.cipherSuite.decrypt(client_socket.recv(BUFFER_SIZE)).decode("utf-8")
            if not data:
                break
            if data.startswith("LOGIN"):
                _, username, password = data.split(":")
                if self.authenticate(username, password):
                    session_id = os.urandom(16).hex()
                    SESSIONS[session_id] = username
                    client_socket.send(self.cipherSuite.encrypt(f"Login successful, session ID: {session_id}".encode("utf-8")))
                    authenticated = True
                else:
                    client_socket.send("Login failed".encode("utf-8"))
            elif data.startswith("UPLOAD"):
                return
            elif data.startswith("DOWNLOAD"):
                filename = data.split()[1]
                if os.path.exists(filename):
                    client_socket.send(b'FILE FOUND')
                    with open(filename, 'rb') as f:
                        while chunk := f.read(1024):
                            client_socket.send(chunk)
                else:
                    client_socket.send(b'FILE NOT FOUND')
            elif data.startswith("DELETE"):
                return
            else:
                break
        print(f'[*] Terminated connection from IP {client_addr[0]} port : {client_addr[1]}')
        client_socket.close()
        if session_id:
            del SESSIONS[session_id]

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp:
            server_tcp.bind((self.host, self.port))
            server_tcp.listen(6)
            print('[*] Waiting for connection')
            while True:
                connection, addr = server_tcp.accept()
                connection.send(self.key)
                print(f'[*] Established connection from IP {addr[0]} port : {addr[1]}')
                thread = Thread(target=self.handle_client, args=(connection, addr))
                thread.start()

if __name__ == "__main__":
    s = Server()
    s.start()
