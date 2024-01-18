import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
from SessionController import SessionController
from PIL import Image, ImageTk


def confirm():
    password = entry_password.get()
    if session.delete_user(password):
        messagebox.showwarning(title="Error", message="User deleted.")
    else:
        messagebox.showwarning(title="Error", message="Wrong password.")



root = tk.Tk()
root.title("GreenGame")
root.resizable(False, False)
root.geometry("800x600+560+240")

image = Image.open("background.jpg")
background_image = ImageTk.PhotoImage(image)

background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

label_password = ctk.CTkLabel(root, text="Password:", corner_radius=0, width=150,fg_color=("white", "gray75"), text_color="black")
label_password.place(x=240,y=200)
entry_password = ctk.CTkEntry(root, show="*", corner_radius=0, width=150)
entry_password.place(x=410,y=200)

confirm_button = ctk.CTkButton(root, text="Delete user", command=confirm, corner_radius=0, width=150,fg_color=("#60A060"),
                                 hover_color=("#006400"))
confirm_button.place(x=325,y=250)

session = SessionController()
root.mainloop()

session.close()
