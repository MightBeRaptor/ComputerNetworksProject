import tkinter as tk
from tkinter import filedialog, messagebox
from view import View, LoginView

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
        filename = filedialog.askstring("Download", "Enter the filename to download:")
        if filename:
            try:
                # Call the download logic here
                download_file(filename)
                messagebox.showinfo("Download", f"{filename} downloaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    #end additions

if __name__ == "__main__":
    c = Controller()
    c.run()
