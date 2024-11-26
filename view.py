import tkinter as tk
from tkinter import filedialog, messagebox

class View:
    def __init__(self, root, controller) -> None:
        self.frame = tk.Frame(master=root)
        self.controller = controller

        self.titleLabel = tk.Label(master=root, font=("Helvetica", 22, "bold"), text="Computer Networks Project")
        self.uploadButton = tk.Button(master=root, text="Upload", command=self.controller.upload)
        self.downloadButton = tk.Button(master=root, text="Download", command=lambda: self.controller.download(self.downloadFileName.get()))
        self.downloadFileName = tk.Entry(master=root)
        self.deleteFileButton = tk.Button(master=root, text="Delete File in Server", command=lambda: self.controller.delete(self.deleteFileName.get()))
        self.deleteFileName = tk.Entry(master=root)
        self.viewDirectoryButton = tk.Button(master=root, text="View Directories", command=self.controller.view_directory)
        self.viewDirectories = tk.Text(master=root, width=50, height=5)
        self.createSubfolderButton = tk.Button(master=root, text="Create Subfolder", command=self.controller.create_subfolder)
        self.createSubfolderName = tk.Entry(master=root)
        self.deleteSubfolderButton = tk.Button(master=root, text="Delete Subfolder", command=self.controller.delete_subfolder)
        self.deleteSubfolderName = tk.Entry(master=root)
        self.logoutButton = tk.Button(master=root, text="LogOut", command=self.controller.logout)
        
    def pack_widgets(self) -> None:
        self.titleLabel.pack(pady=5)
        self.uploadButton.pack(pady=5)
        self.downloadButton.pack(pady=5)
        self.downloadFileName.pack(pady=5)
        self.deleteFileButton.pack(pady=5)
        self.deleteFileName.pack(pady=5)
        self.viewDirectoryButton.pack(pady=5)
        self.viewDirectories.pack(pady=5)
        self.createSubfolderButton.pack(pady=5)
        self.createSubfolderName.pack(pady=5)
        self.deleteSubfolderButton.pack(pady=5)
        self.deleteSubfolderName.pack(pady=5)
        self.logoutButton.pack(pady=5)
    
    def unpack_widgets(self) -> None:
        self.titleLabel.pack_forget()
        self.uploadButton.pack_forget()
        self.downloadButton.pack_forget()
        self.deleteFileButton.pack_forget()
        self.viewDirectoryButton.pack_forget()
        self.createSubfolderButton.pack_forget()
        self.deleteSubfolderButton.pack_forget()
        self.logoutButton.pack_forget()
        

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