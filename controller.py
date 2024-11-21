import tkinter as tk
from tkinter import filedialog, messagebox
from view import View, LoginView

# download additions
from client_operations import download_file
from tkinter import filedialog
# end additions

class Controller:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.view = View(self.root, self)
        self.loginView = LoginView(self.root, self)

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

    # download additions
    def download_file(self):
        server_ip = filedialog.askstring("Server IP", "Enter the server IP:")
        port = 9999  # Default port; you can make it configurable
        filename = filedialog.askstring("Filename", "Enter the filename to download:")
        save_path = filedialog.askdirectory(title="Select Save Directory")

        if server_ip and filename and save_path:
            try:
                download_file(server_ip, port, filename, save_path)
                messagebox.showinfo("Download", f"{filename} downloaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Missing", "Please provide all required inputs.")
    #end additions

if __name__ == "__main__":
    c = Controller()
    c.run()
