import socket
import os

def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        if request.startswith('DOWNLOAD'):
            filename = request.split()[1]
            if os.path.exists(filename):
                client_socket.send(b'FILE_FOUND')
                with open(filename, 'rb') as f:
                    while chunk := f.read(1024):
                        client_socket.send(chunk)
            else:
                client_socket.send(b'FILE_NOT_FOUND')
        elif request == 'QUIT':
            break
    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(5)
print("Server listening on port 9999...")

while True:
    client_sock, addr = server.accept()
    print(f"Connection from {addr}")
    handle_client(client_sock)
