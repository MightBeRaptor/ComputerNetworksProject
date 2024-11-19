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
        self.host = 'localhost' # Reokace with server IP address
        self.port = 3300 # Replace with server's port number
        self.key = Fernet.generate_key()
        self.cipherSuite = Fernet(key)

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

    def setup_connection():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_tcp:
            client_tcp.connect((self.host, self.port))


if __name__ == "__main__":
    c = Controller()
    c.run()