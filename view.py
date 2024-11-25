import tkinter as tk
from tkinter import filedialog, messagebox

class View:
    def __init__(self, root, controller) -> None:
        self.frame = tk.Frame(master=root)
        self.controller = controller

        self.titleLabel = tk.Label(master=root, font=("Helvetica", 22, "bold"), text="Computer Networks Project")
        self.uploadButton = tk.Button(master=root, text="Upload")
        self.downloadButton = tk.Button(master=root, text="Download")
        self.logoutButton = tk.Button(master=root, text="LogOut", command=self.controller.logout)
        
    def pack_widgets(self) -> None:
        self.titleLabel.place(x=125, y=25)
        self.logoutButton.place(x=300, y=290)
    
    def unpack_widgets(self) -> None:
        self.titleLabel.place_forget()
        self.logoutButton.place_forget()
        

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
        self.usernameInput.delete(0, tk.END)
        self.usernameInput.pack_forget()
        self.passwordLabel.pack_forget()
        self.passwordInput.delete(0, tk.END)
        self.passwordInput.pack_forget()
        self.loginButton.pack_forget()