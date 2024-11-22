import tkinter as tk
from tkinter import filedialog, messagebox
from view import View, LoginView
import socket
from cryptography.fernet import Fernet

BUFFER_SIZE = 1024

class Controller:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.view = View(self.root, self)
        self.loginView = LoginView(self.root, self)
        self.host = socket.gethostbyname(socket.gethostname()) # Replace with server IP address
        self.port = 8000 # Replace with server's port number
        self.socket = None
        self.fernet = None
        
    def run(self) -> None:
        self.root.title("Computer Networks Project")
        self.root.geometry("600x350")
        self.loginView.pack_widgets()
        self.root.mainloop()

    def login(self) -> None:
        if self.loginView.usernameInput.get() == "username" and self.loginView.passwordInput.get() == "password":
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.loginView.unpack_widgets()
            self.view.pack_widgets()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def download(self, filename, savepath):
        self.socket.send(self.fernet.encrypt(f'DOWNLOAD {filename}'.encode("utf-8")))
        response = self.fernet.decrypt(self.socket.recv(BUFFER_SIZE)).decode("utf-8")
        if response.startswith("FILE FOUND"):
            with open(f"{savepath}/{filename}", "wb") as f:
                while True:
                    data = self.socket.recv(BUFFER_SIZE)
                    if not data:
                        break
                    f.write(data)
            print(f"File '{filename}' downloaded successfully.")
        else:
            print(f"File '{filename}' not found on the server.")

    def logout(self) -> None:
        self.socket.send(self.fernet.encrypt("LOGOUT".encode("utf-8")))

    def setup_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        key = self.socket.recv(BUFFER_SIZE)
        self.fernet = Fernet(key)
        self.socket.send(self.fernet.encrypt(f"LOGIN:{self.loginView.usernameInput.get()}:{self.loginView.passwordInput.get()}".encode("utf-8")))
        response = self.fernet.decrypt(self.socket.recv(BUFFER_SIZE)).decode("utf-8")
        if response.startswith("Login successful"):
            self.loginView.unpack_widgets()
            self.view.pack_widgets()

if __name__ == "__main__":
    c = Controller()
    c.run()