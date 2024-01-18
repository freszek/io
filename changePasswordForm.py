import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from SessionController import SessionController


def confirm():
    password = entry_password.get()
    new_password = entry_new_password.get()
    if len(new_password) >= 8:
        if not session.change_password(password, new_password):
            messagebox.showwarning(title="Error", message="Wrong old password.")
        else:
            messagebox.showinfo(title="Notification", message="Password has been changed.")
    else:
        messagebox.showwarning(title="Error", message="New password is too weak(8 characters).")

root = tk.Tk()
root.title("GreenGame")
root.resizable(False, False)
root.geometry("800x600+560+240")

image = Image.open("background.jpg")
background_image = ImageTk.PhotoImage(image)

background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

label_password = ctk.CTkLabel(root, text="Old password:", fg_color=("white", "gray75"),
                             text_color="black", width=150,corner_radius=0)
label_password.place(x=240,y=150)
entry_password = ctk.CTkEntry(root,corner_radius=0,width=150,show="*")
entry_password.place(x=410,y=150)

label_new_password = ctk.CTkLabel(root, text="New password:", fg_color=("white", "gray75"),
                             text_color="black", width=150,corner_radius=0)
label_new_password.place(x=240,y=200)
entry_new_password = ctk.CTkEntry(root, show="*", corner_radius=0,width=150)
entry_new_password.place(x=410,y=200)

confirm_button = ctk.CTkButton(root, text="Change password", command=confirm, corner_radius=0,fg_color=("#60A060"),
                                 hover_color=("#006400"),)
confirm_button.place(x=325,y=250)

session = SessionController()
root.mainloop()

session.close()