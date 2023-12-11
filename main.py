import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from SessionController import SessionController


def zarejestruj():
    email = pole_email.get()
    login = pole_login.get()
    haslo = pole_haslo.get()
    pytanie_pomocnicze = lista_pytan.get()
    odpowiedz = pole_odpowiedzi.get()

    if "" not in (email, login, haslo, pytanie_pomocnicze, odpowiedz) and len(haslo) >= 8:
        session.register(login, haslo, email, pytanie_pomocnicze, odpowiedz)


def zaloguj():
    login_window = simpledialog.Toplevel(root)
    login_window.title("Logowanie")

    etykieta_login_log = ttk.Label(login_window, text="Login:")
    etykieta_haslo_log = ttk.Label(login_window, text="Hasło:")
    etykieta_odpowiedz_log = ttk.Label(login_window, text="Odpowiedź:")

    pole_login_log = ttk.Entry(login_window)
    pole_haslo_log = ttk.Entry(login_window, show="*")
    pole_odpowiedz_log = ttk.Entry(login_window)

    przycisk_zaloguj_log = ttk.Button(login_window, text="Zaloguj się",
                                      command=lambda: zaloguj_log(pole_login_log.get(), pole_haslo_log.get(),
                                                                  pole_odpowiedz_log.get()))

    etykieta_login_log.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    etykieta_haslo_log.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    etykieta_odpowiedz_log.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    pole_login_log.grid(row=0, column=1, padx=10, pady=5)
    pole_haslo_log.grid(row=1, column=1, padx=10, pady=5)
    pole_odpowiedz_log.grid(row=2, column=1, padx=10, pady=5)

    przycisk_zaloguj_log.grid(row=3, column=1, pady=10)


def zaloguj_log(login, haslo, odpowiedz):
    session.log_in(login, haslo, odpowiedz)


root = tk.Tk()
root.title("Rejestracja")

etykieta_email = ttk.Label(root, text="Email:")
etykieta_login = ttk.Label(root, text="Login:")
etykieta_haslo = ttk.Label(root, text="Hasło:")
etykieta_pytanie = ttk.Label(root, text="Pytanie pomocnicze:")
etykieta_odpowiedz = ttk.Label(root, text="Odpowiedź:")

pole_email = ttk.Entry(root)
pole_login = ttk.Entry(root)
pole_haslo = ttk.Entry(root, show="*")
lista_pytan = ttk.Combobox(root,
                           values=["Jakie jest imię twojego zwierzaka?", "Gdzie urodziłeś się?", "Ulubiona książka?"])
pole_odpowiedzi = ttk.Entry(root)

przycisk_zarejestruj = ttk.Button(root, text="Zarejestruj", command=zarejestruj)
przycisk_zaloguj = ttk.Button(root, text="Masz już konto? Zaloguj się", command=zaloguj)

etykieta_email.grid(row=0, column=0, padx=10, pady=5, sticky="e")
etykieta_login.grid(row=1, column=0, padx=10, pady=5, sticky="e")
etykieta_haslo.grid(row=2, column=0, padx=10, pady=5, sticky="e")
etykieta_pytanie.grid(row=3, column=0, padx=10, pady=5, sticky="e")
etykieta_odpowiedz.grid(row=4, column=0, padx=10, pady=5, sticky="e")

pole_email.grid(row=0, column=1, padx=10, pady=5)
pole_login.grid(row=1, column=1, padx=10, pady=5)
pole_haslo.grid(row=2, column=1, padx=10, pady=5)
lista_pytan.grid(row=3, column=1, padx=10, pady=5)
pole_odpowiedzi.grid(row=4, column=1, padx=10, pady=5)

przycisk_zarejestruj.grid(row=5, column=1, pady=10, columnspan=2, sticky="nsew")
przycisk_zaloguj.grid(row=6, column=1, pady=10, columnspan=2, sticky="nsew")

session = SessionController()
root.mainloop()

session.close()
