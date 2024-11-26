import socket
from threading import Thread
from cryptography.fernet import Fernet
import os
import shutil
from network_analysis import start_time, initialize_stats_dataframe, log_statistics

USER_DB = {  # Login information stored in a dictionary
    "username": "password"
}

BUFFER_SIZE = 1024
SESSIONS = {}
FILE_STORAGE_PATH = "./file_storage"  # Directory to store files on server
TEXT_FILE_LIMIT = 25 * 1024 * 1024  # 25 MB
AUDIO_FILE_LIMIT = 0.5 * 1024 * 1024 * 1024  # 0.5 GB
VIDEO_FILE_LIMIT = 2 * 1024 * 1024 * 1024  # 2 GB


class Server:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())  # Change to server host
        self.port = 8000  # Change to server port

        self.key = Fernet.generate_key()  # Encryption key
        self.cipherSuite = Fernet(self.key)

        if not os.path.exists(FILE_STORAGE_PATH):
            os.makedirs(FILE_STORAGE_PATH)  # Ensure storage directory exists

        initialize_stats_dataframe()

    def authenticate(self, username, password):
        return USER_DB.get(username) == password

    def handle_client(self, client_socket, client_addr):
        session_id = None

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
                    client_socket.send(
                        self.cipherSuite.encrypt(f"Login successful, session ID: {session_id}".encode("utf-8")))
                else:
                    client_socket.send("Login failed".encode("utf-8"))
            elif data.startswith("UPLOAD"):
                _, file_name, file_size = data.split(
                    ":")  # Get file details from the data (e.g., filename and file size)
                file_size = int(file_size)

                # Determine the file type and check size restrictions
                file_extension = file_name.split('.')[-1].lower()
                if file_extension in ["txt", "csv"]:  # Text file types
                    if file_size <= TEXT_FILE_LIMIT:
                        client_socket.send(self.cipherSuite.encrypt(
                            f"Error: Text file size doesn't meet 25 MB requirement.".encode("utf-8")))
                        return
                elif file_extension in ["mp3", "wav"]:  # Audio file types
                    if file_size <= AUDIO_FILE_LIMIT:
                        client_socket.send(self.cipherSuite.encrypt(
                            f"Error: Audio file size doesn't meet 0.5 GB requirement.".encode("utf-8")))
                        return
                elif file_extension in ["mp4", "avi", "mkv"]:  # Video file types
                    if file_size <= VIDEO_FILE_LIMIT:
                        client_socket.send(self.cipherSuite.encrypt(
                            f"Error: Video file size doesn't meet 2 GB requirement.".encode("utf-8")))
                        return
                else:
                    client_socket.send(self.cipherSuite.encrypt(f"Error: Unsupported file type.".encode("utf-8")))
                    return
                client_socket.send(self.cipherSuite.encrypt(f"File type supported".encode("utf-8")))
                # Proceed with file upload if size is valid
                try:
                    starting_time = start_time()
                    file_path = os.path.join(FILE_STORAGE_PATH, file_name)
                    with open(file_path, "wb") as f:
                        remaining_size = file_size
                        while remaining_size > 0:
                            chunk = client_socket.recv(min(BUFFER_SIZE, remaining_size))
                            if not chunk:
                                break
                            f.write(chunk)
                            remaining_size -= len(chunk)
                    if remaining_size == 0:
                        client_socket.send(f"File {file_name} uploaded successfully.".encode("utf-8"))
                        log_statistics(starting_time, file_path)
                    else:
                        os.remove(file_path)
                        client_socket.send(
                            self.cipherSuite.encrypt(f"Error: Incomplete file was uploaded".encode("utf-8")))
                except Exception as e:
                    client_socket.send(
                        self.cipherSuite.encrypt(f"Error: Failed to upload the file {str(e)}".encode("utf-8")))
            elif data.startswith("DOWNLOAD"):
                starting_time = start_time()
                _, file_name = data.split(":")
                if os.path.exists(f"./{FILE_STORAGE_PATH}/{file_name}"):
                    client_socket.send(self.cipherSuite.encrypt("FILE FOUND".encode("utf-8")))
                    file_path = os.path.join(FILE_STORAGE_PATH, file_name)
                    with open(file_path, "rb") as f:
                        while chunk := f.read(BUFFER_SIZE):
                            client_socket.sendall(chunk)
                    client_socket.send(b"END")
                    log_statistics(starting_time, file_path)
                else:
                    client_socket.send(self.cipherSuite.encrypt("FILE NOT FOUND".encode("utf-8")))
            elif data.startswith("DELETE"):
                _, file_name = data.split(":")  # Handle file delete request.
                file_path = None
                for root, dirs, files in os.walk(FILE_STORAGE_PATH):
                    if file_name in files:
                        file_path = os.path.join(root, file_name)
                        break
                if os.path.exists(file_path):
                    os.remove(file_path)
                    client_socket.send(
                        self.cipherSuite.encrypt(f"File {file_name} deleted successfully".encode("utf-8")))
                else:
                    client_socket.send(self.cipherSuite.encrypt(f"File {file_name} not found.".encode("utf-8")))

            elif data.startswith("DIR"):
                file_list = []
                for dirpath, dirnames, filenames in os.walk(FILE_STORAGE_PATH):
                    for filename in filenames:
                        file_list.append(os.path.realpath(os.path.join(dirpath, filename)))
                if file_list:
                    files_list = "\n".join(file_list)
                    client_socket.send(self.cipherSuite.encrypt(f"Files in directory:\n{files_list}".encode("utf-8")))
                else:
                    client_socket.send(self.cipherSuite.encrypt("No files found".encode("utf-8")))

            elif data.startswith("SUBFOLDERCREATE"):
                command, folder_name = data.split(":")
                try:
                    folder_path = os.path.join(FILE_STORAGE_PATH, folder_name)
                    os.makedirs(folder_path)
                    client_socket.send(
                        self.cipherSuite.encrypt(f"Success, {folder_name} subfolder created".encode("utf-8")))
                except Exception as e:
                    client_socket.send(
                        self.cipherSuite.encrypt(f"Failure: {folder_name} could not be created".encode("utf-8")))
            elif data.startswith("SUBFOLDERDELETE"):
                command, folder_name = data.split(":")
                try:
                    folder_path = os.path.join(FILE_STORAGE_PATH, folder_name)
                    shutil.rmtree(folder_path)
                    client_socket.send(
                        self.cipherSuite.encrypt(f"Success: {folder_name} subfolder deleted".encode("utf-8")))
                except Exception as e:
                    client_socket.send(
                        self.cipherSuite.encrypt(f"Failure: {folder_name} could not be deleted".encode("utf-8")))
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