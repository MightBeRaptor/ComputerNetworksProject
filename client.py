import socket

def download_file(server_ip, port, filename, save_path):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, port))
        client.send(f'DOWNLOAD {filename}'.encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        if response == 'FILE_FOUND':
            with open(f"{save_path}/{filename}", 'wb') as f:
                while True:
                    data = client.recv(1024)
                    if not data:
                        break
                    f.write(data)
            print(f"File '{filename}' downloaded successfully.")
        else:
            print(f"File '{filename}' not found on the server.")
        client.close()
    except Exception as e:
        print(f"Error: {e}")
