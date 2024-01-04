import tkinter as tk
import customtkinter as ctk
from tkinter import simpledialog
from SessionController import SessionController


def register():
    email = email_field.get()
    login = login_field.get()
    password = password_field.get()
    question = questions_field.get()
    answer = answer_field.get()

    if "" in (email, login, password, question, answer):
        print("Brak wszystkich danych")
        return

    if len(password) < 8:
        print("Haslo nie spelnia wymagan (8 znakow)")
        return

    session.register(login, password, email, question, answer)


def login():
    login_window = simpledialog.Toplevel(root)
    login_window.title("GreenGame")

    login_log = ctk.CTkLabel(login_window, text="Login:", fg_color=("white", "gray75"), corner_radius=8,
                             text_color="black", width=150)
    password_log = ctk.CTkLabel(login_window, text="Password:", fg_color=("white", "gray75"), corner_radius=8,
                                text_color="black", width=150)
    answer_log = ctk.CTkLabel(login_window, text="Answer:", fg_color=("white", "gray75"), corner_radius=8,
                              text_color="black", width=150)

    login_field_log = ctk.CTkEntry(login_window)
    password_field_log = ctk.CTkEntry(login_window, show="*")
    answer_field_log = ctk.CTkEntry(login_window)

    login_button_log = ctk.CTkButton(login_window, text="Login",
                                     command=lambda: log_in(login_field_log.get(), password_field_log.get(),
                                                            answer_field_log.get()),fg_color=("#60A060"), hover_color=("#006400"))

    login_log.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    password_log.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    answer_log.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    login_field_log.grid(row=0, column=1, padx=10, pady=5)
    password_field_log.grid(row=1, column=1, padx=10, pady=5)
    answer_field_log.grid(row=2, column=1, padx=10, pady=5)

    login_button_log.grid(row=3, column=0, pady=10, columnspan=3)


def log_in(login, password, answer):
    session.log_in(login, password, answer)


root = tk.Tk()
root.title("GreenGame")
root.resizable(False, False)

email_string = ctk.CTkLabel(root, text="Email:", fg_color=("white", "gray75"), corner_radius=8, text_color="black",
                            width=150)
login_string = ctk.CTkLabel(root, text="Login:", fg_color=("white", "gray75"), corner_radius=8, text_color="black",
                            width=150)
password_string = ctk.CTkLabel(root, text="Password:", fg_color=("white", "gray75"), corner_radius=8,
                               text_color="black", width=150)
question_string = ctk.CTkLabel(root, text="Question:", fg_color=("white", "gray75"), corner_radius=8,
                               text_color="black", width=150)
answer_string = ctk.CTkLabel(root, text="Answer:", fg_color=("white", "gray75"), corner_radius=8, text_color="black",
                             width=150)

email_field = ctk.CTkEntry(root)
login_field = ctk.CTkEntry(root)
password_field = ctk.CTkEntry(root, show="*")
questions_field = ctk.CTkComboBox(root, values=["What is your pet's name?", "Where you were born?", "Favourite book?"])
answer_field = ctk.CTkEntry(root)

register_button = ctk.CTkButton(root, text="Register", command=register, fg_color=("#60A060"), hover_color=("#006400"))
login_button = ctk.CTkButton(root, text="Already have an account? Log in", command=login, fg_color=("#60A060"), hover_color=("#006400"))

email_string.grid(row=0, column=0, padx=10, pady=5, sticky="e")
login_string.grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_string.grid(row=2, column=0, padx=10, pady=5, sticky="e")
question_string.grid(row=3, column=0, padx=10, pady=5, sticky="e")
answer_string.grid(row=4, column=0, padx=10, pady=5, sticky="e")

email_field.grid(row=0, column=1, padx=10, pady=5)
login_field.grid(row=1, column=1, padx=10, pady=5)
password_field.grid(row=2, column=1, padx=10, pady=5)
questions_field.grid(row=3, column=1, padx=10, pady=5)
answer_field.grid(row=4, column=1, padx=10, pady=5)

register_button.grid(row=5, column=0, pady=10, columnspan=3)
login_button.grid(row=6, column=0, pady=10, columnspan=3)

session = SessionController()
root.mainloop()

session.close()
