import tkinter as tk
import customtkinter as ctk
from tkinter import simpledialog, messagebox
from SessionController import SessionController
from PIL import Image, ImageTk


def register_in(email, login, password, answer, question):
    global session
    if "" in (email, login, password, question, answer):
        messagebox.showwarning(title="Error", message="All data is missing.")
        return

    if len(password) < 8:
        messagebox.showwarning(title="Error", message="Password is too weak(8 characters).")
        return
    if session.check_login(login):
        messagebox.showwarning(title="Error", message="User exists. Please log in.")
    session.register(login, password, email, answer, question)
    messagebox.showinfo(title="Notification", message="User created.")

def register(frame):
    frame.destroy()
    temp = tk.Tk()
    temp.title("GreenGame")
    temp.resizable(False, False)
    temp.geometry("800x600+560+240")

    image = Image.open("background.jpg")
    background_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(temp, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    email_string = ctk.CTkLabel(temp, text="Email:", fg_color=("white", "gray75"), text_color="black",
                                width=150)
    login_string = ctk.CTkLabel(temp, text="Login:", fg_color=("white", "gray75"), text_color="black",
                                width=150)
    password_string = ctk.CTkLabel(temp, text="Password:", fg_color=("white", "gray75"),
                                   text_color="black", width=150)
    question_string = ctk.CTkLabel(temp, text="Question:", fg_color=("white", "gray75"),
                                   text_color="black", width=150)
    answer_string = ctk.CTkLabel(temp, text="Answer:", fg_color=("white", "gray75"),
                                 text_color="black",
                                 width=150)

    email_field = ctk.CTkEntry(temp,corner_radius=0,width=150)
    login_field = ctk.CTkEntry(temp,corner_radius=0,width=150)
    password_field = ctk.CTkEntry(temp, show="*",corner_radius=0,width=150)
    questions_field = ctk.CTkComboBox(temp,
                                      values=["What is your pet's name?", "Where you were born?", "Favourite book?"],corner_radius=0,width=150)
    answer_field = ctk.CTkEntry(temp,corner_radius=0,width=150)

    register_button = ctk.CTkButton(temp, text="Register", command=lambda: register_in(email_field.get(), login_field.get(),
                                                        password_field.get(), answer_field.get(), questions_field.get()), fg_color=("#60A060"),
                                    hover_color=("#006400"),corner_radius=0,width=150)
    back_button = ctk.CTkButton(temp, text="Back to login",
                                    command=lambda: main_window(temp), fg_color=("#60A060"),
                                    hover_color=("#006400"), corner_radius=0,width=150)

    email_string.place(x=240,y=50)
    login_string.place(x=240,y=100)
    password_string.place(x=240,y=150)
    question_string.place(x=240,y=200)
    answer_string.place(x=240,y=250)

    email_field.place(x=410, y=50)
    login_field.place(x=410, y=100)
    password_field.place(x=410, y=150)
    questions_field.place(x=410, y=200)
    answer_field.place(x=410, y=250)

    register_button.place(x=240, y=300)

    back_button.place(x=410, y=300)

    temp.mainloop()


def log_in(login, password, answer):
    global session
    if session.counter >= 5:
        messagebox.showwarning(title="Error", message="You are blocked.")
    if session.counter < 5 and (login == "" or password == ""):
        messagebox.showwarning(title="Error", message="Enter credentials.")
    session.log_in(login, password, answer)

def answer_log_in(login, password, answer):
    global session
    if login == "" or answer == "":
        messagebox.showwarning(title="Error", message="Enter credentials.")
    session.log_in(login, password, answer)

def answer_login(frame):
    frame.destroy()
    temp = tk.Tk()
    temp.title("GreenGame")
    temp.resizable(False, False)
    temp.geometry("800x600+560+240")

    image = Image.open("background.jpg")
    background_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(temp, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    login_log = ctk.CTkLabel(temp, text="Login:", fg_color=("white", "gray75"),
                             text_color="black", width=150)
    answer_log = ctk.CTkLabel(temp, text="Answer:", fg_color=("white", "gray75"),
                                text_color="black", width=150)

    login_field_log = ctk.CTkEntry(temp,corner_radius=0, width=150)
    answer_field_log = ctk.CTkEntry(temp, show="*",corner_radius=0, width=150)

    login_button_log = ctk.CTkButton(temp, text="Login",
                                     command=lambda: answer_log_in(login_field_log.get(), "",
                                                            answer_field_log.get()), fg_color=("#60A060"), hover_color=("#006400"),corner_radius=0, width=150)
    back_button = ctk.CTkButton(temp, text="Back",
                                     command=lambda: main_window(temp), fg_color=("#60A060"),
                                     hover_color=("#006400"), corner_radius=0, width=150)

    login_log.place(x=240, y=150)
    answer_log.place(x=240, y=200)

    login_field_log.place(x=410, y=150)
    answer_field_log.place(x=410, y=200)

    login_button_log.place(x=240, y=250)
    back_button.place(x=410, y=250)

    temp.mainloop()

def main_window(frame):
    if frame is not None:
        frame.destroy()
    root = tk.Tk()
    root.title("GreenGame")
    root.resizable(False, False)
    root.geometry("800x600+560+240")

    image = Image.open("background.jpg")
    background_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    login_log = ctk.CTkLabel(root, text="Login:", fg_color=("white", "gray75"),
                             text_color="black", width=150,corner_radius=0)
    password_log = ctk.CTkLabel(root, text="Password:", fg_color=("white", "gray75"),
                                text_color="black", width=150,corner_radius=0)

    login_field_log = ctk.CTkEntry(root,corner_radius=0,width=150)
    password_field_log = ctk.CTkEntry(root, show="*",corner_radius=0,width=150)

    login_button_log = ctk.CTkButton(root, text="Login",
                                     command=lambda: log_in(login_field_log.get(), password_field_log.get(),
                                                            ""),fg_color=("#60A060"), hover_color=("#006400"),corner_radius=0,width=150)

    login_log.place(x=240, y=150)
    password_log.place(x=240, y=200)

    login_field_log.place(x=410, y=150)
    password_field_log.place(x=410, y=200)

    login_button_log.place(x=240, y=250)

    register_button = ctk.CTkButton(root, text="Register", command=lambda: register(root), fg_color=("#60A060"),
                                 hover_color=("#006400"),corner_radius=0,width=150)

    forgot_password_button = ctk.CTkButton(root, text="Forgot password?", command=lambda: answer_login(root), fg_color=("#60A060"),
                                 hover_color=("#006400"),corner_radius=0,width=150)

    register_button.place(x=410, y=250)

    forgot_password_button.place(x=325, y=300)

    session = SessionController()
    root.mainloop()

    session.close()

session = SessionController()
main_window(None)
