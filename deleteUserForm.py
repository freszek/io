import tkinter as tk
import customtkinter as ctk
from SessionController import SessionController


def confirm():
    password = entry_password.get()
    if session.delete_user(password):
        print("User deleted")


root = tk.Tk()
root.title("GreenGame")
root.resizable(False, False)

label_password = ctk.CTkLabel(root, text="Password:", corner_radius=8, width=150)
label_password.pack(pady=10)
entry_password = ctk.CTkEntry(root, show="*", corner_radius=8)
entry_password.pack(pady=10)

confirm_button = ctk.CTkButton(root, text="Confirm", command=confirm, corner_radius=8)
confirm_button.pack()

session = SessionController()
root.mainloop()

session.close()
