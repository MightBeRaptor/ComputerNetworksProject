import tkinter as tk
from tkinter import filedialog, messagebox
from view import View, LoginView
import socket
import os
from cryptography.fernet import Fernet

BUFFER_SIZE = 1024
FILE_STORAGE = "./client_file_downloads"

class Controller:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.view = View(self.root, self)
        self.loginView = LoginView(self.root, self)
        self.host = socket.gethostbyname(socket.gethostname()) # Replace with server IP address
        self.port = 8000 # Replace with server's port number
        self.socket = None
        self.fernet = None

        if not os.path.exists(FILE_STORAGE):
            os.makedirs(FILE_STORAGE)  # Ensure storage directory exists
        
    def run(self) -> None:
        self.root.title("Computer Networks Project")
        self.root.geometry("700x400")
        self.loginView.pack_widgets()
        self.root.mainloop()

    def upload(self) -> None:
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # Prepare the upload command
        command = f"UPLOAD:{file_name}:{file_size}"
        self.socket.sendall(self.fernet.encrypt(command.encode("utf-8")))

        # Receive server response
        response = self.fernet.decrypt(self.socket.recv(BUFFER_SIZE)).decode("utf-8")
        print(response)
        if response.startswith("Error"):
            messagebox.showerror("Upload Failed", response)
            return

        # Send file content if validation passes
        with open(file_path, 'rb') as f:
            while chunk := f.read(BUFFER_SIZE):
                self.socket.sendall(chunk)

        messagebox.showinfo("Upload Successful", f"File '{file_name}' uploaded successfully.")

    def download(self, filename):
        self.socket.send(self.fernet.encrypt(f'DOWNLOAD:{filename}'.encode("utf-8")))
        response = self.fernet.decrypt(self.socket.recv(BUFFER_SIZE)).decode("utf-8")
        print(response)
        if response.startswith("FILE FOUND"):
            try:
                file_path = os.path.join(FILE_STORAGE, filename)
                with open(file_path, "wb") as f:
                    while True:
                        data = self.socket.recv(BUFFER_SIZE)
                        print(data.decode())
                        if b"END" in data:
                            data = data.split(b"END")[0]
                            f.write(data)
                            break
                        f.write(data)
                messagebox.showinfo(f"File '{filename}' downloaded successfully.")
            except Exception as e:
                messagebox.showerror(f"Error: File could not download successfully {str(e)}")
        else:
            print(f"File '{filename}' not found on the server.")

    def delete(self, filename):
        self.socket.send(self.fernet.encrypt(f'DELETE:{filename}'.encode("utf-8")))
        response = self.fernet.decrypt(self.socket.recv(BUFFER_SIZE)).decode("utf-8")
        if response.startswith(f"File {filename} deleted"):
            messagebox.showinfo("Delete Successful", f"File '{filename}' deleted successfully.")
        else:
            messagebox.showerror("Delete Failed", f"Error: {response}")

    def view_directory(self) -> None:
        # Send the "DIR" command to request the directory listing from the server
        self.socket.send(self.fernet.encrypt("DIR".encode("utf-8")))

        # Receive the response from the server
        response = self.fernet.decrypt(self.socket.recv(BUFFER_SIZE)).decode("utf-8")

        # If the response starts with "Files in directory", show the file list
        if response.startswith("Files in directory"):
            file_list = response.split("Files in directory:\n")[1]
            print(file_list)
            self.view.viewDirectories.insert(tk.END, file_list)
            # messagebox.showinfo("File Directory", f"Files in the server directory:\n{file_list}")
        else:
            messagebox.showerror("Error", "Failed to retrieve directory list")

    def logout(self) -> None:
        self.socket.send(self.fernet.encrypt("LOGOUT".encode("utf-8")))
        self.view.unpack_widgets()
        self.loginView.pack_widgets()

    def setup_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        key = self.socket.recv(BUFFER_SIZE)
        self.fernet = Fernet(key)
        self.socket.send(self.fernet.encrypt(f"LOGIN:{self.loginView.usernameInput.get()}:{self.loginView.passwordInput.get()}".encode("utf-8")))
        response = self.fernet.decrypt(self.socket.recv(BUFFER_SIZE)).decode("utf-8")
        if response.startswith("Login successful"):
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.loginView.unpack_widgets()
            self.view.pack_widgets()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

if __name__ == "__main__":
    c = Controller()
    c.run()