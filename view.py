import tkinter as tk
from tkinter import filedialog, messagebox

class View:
    def __init__(self, root, controller) -> None:
        self.frame = tk.Frame(master=root)
        self.controller = controller

        self.titleLabel = tk.Label(master=root, font=("Helvetica", 22, "bold"), text="Computer Networks Project")

    def pack_widgets(self) -> None:
        self.titleLabel.place(x=125, y=25)

class LoginView:
    def __init__(self, root, controller) -> None:
        self.frame = tk.Frame(master=root)
        self.controller = controller

        self.titleLabel = tk.Label(master=root, font=("Helvetica", 22, "bold"), text="Enter Login Information")
        self.usernameLabel = tk.Label(master=root, font=("Helvetica", 12, "normal"), text="User ID:")
        self.usernameInput = tk.Entry(master=root)
        self.passwordLabel = tk.Label(master=root, font=("Helvetica", 12, "normal"), text="Password:")
        self.passwordInput = tk.Entry(master=root, show="*")
        self.loginButton = tk.Button(master=root, text="Login", command=self.controller.setup_connection)
    
    def pack_widgets(self) -> None:
        self.titleLabel.pack()
        self.usernameLabel.pack(pady=10)
        self.usernameInput.pack(pady=10)
        self.passwordLabel.pack(pady=10)
        self.passwordInput.pack(pady=10)
        self.loginButton.pack(pady=10)

    def unpack_widgets(self) -> None:
        self.titleLabel.pack_forget()
        self.usernameLabel.pack_forget()
        self.usernameInput.pack_forget()
        self.passwordLabel.pack_forget()
        self.passwordInput.pack_forget()
        self.loginButton.pack_forget()