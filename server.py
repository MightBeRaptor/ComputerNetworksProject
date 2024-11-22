import socket
from threading import Thread
from cryptography.fernet import Fernet
import os
import ssl
import shutil

BUFFER_SIZE = 1024

USER_DB = {
    "username": "password"
}

SESSIONS = {}
FILE_STORAGE_PATH = "./file_storage" # Directory to store files on server

class Server:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())  # Change to server host
        self.port = 8000  # Change to server port

        self.key = Fernet.generate_key()
        self.cipherSuite = Fernet(self.key)
        if not os.path.exists(FILE_STORAGE_PATH):
            os.makedirs(FILE_STORAGE_PATH)  # Ensure storage directory exists

    def authenticate(self, username, password):
        return USER_DB.get(username) == password

    def handle_client(self, client_socket, client_addr):
        session_id = None
        authenticated = False

        while True:
            data = self.cipherSuite.decrypt(client_socket.recv(BUFFER_SIZE)).decode("utf-8")
            print(data)
            if not data:
                break
            if data.startswith("LOGIN"):
                _, username, password = data.split(":")
                if self.authenticate(username, password):
                    session_id = os.urandom(16).hex()
                    SESSIONS[session_id] = username
                    client_socket.send(f"Login successful, session ID: {session_id}".encode("utf-8"))
                    authenticated = True
                else:
                    client_socket.send("Login failed".encode("utf-8"))
            elif data.startswith("UPLOAD"):
                return
            elif data.startswith("DOWNLOAD"):
                return
            else:
                break
        client_socket.close()
        if session_id:
            del SESSIONS[session_id]

    def handle_delete(self, client_socket, data):
        _, file_name = data.split(":") # Handle file delete request.
        file_path = os.path.join(FILE_STORAGE_PATH, file_name)

        if os.path.exists(file_path):
            os.remove(file_path)
            client_socket.send(f"File {file_name} deleted successfully".encode("utf-8"))
        else:
            client_socket.send(f"File {file_name} not found.".encode("utf-8"))


    def handle_dir(self, client_socket):
        files = os.listdir(FILE_STORAGE_PATH) #List files in server directory.
        files_list = "\n".join(files)
        client_socket.send(f"Files in directory:\n{files_list}".encode("utf-8"))



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