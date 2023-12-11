import tkinter as tk
from tkinter import ttk

def zarejestruj():
    email = pole_email.get()
    login = pole_login.get()
    haslo = pole_haslo.get()
    pytanie_pomocnicze = lista_pytan.get()
    odpowiedz = pole_odpowiedzi.get()

    # Tutaj możesz dodać kod do obsługi rejestracji
    print(f"Zarejestrowano:\nEmail: {email}\nLogin: {login}\nHasło: {haslo}\n"
          f"Pytanie pomocnicze: {pytanie_pomocnicze}\nOdpowiedź: {odpowiedz}")

def zaloguj():
    # Tutaj możesz dodać kod do obsługi logowania
    print("Przejście do ekranu logowania")

# Utwórz okno główne
root = tk.Tk()
#root.geometry("450x250")
root.title("Rejestracja")

# Utwórz etykiety i pola do wprowadzania danych
etykieta_email = ttk.Label(root, text="Email:")
etykieta_login = ttk.Label(root, text="Login:")
etykieta_haslo = ttk.Label(root, text="Hasło:")
etykieta_pytanie = ttk.Label(root, text="Pytanie pomocnicze:")
etykieta_odpowiedz = ttk.Label(root, text="Odpowiedź:")

pole_email = ttk.Entry(root)
pole_login = ttk.Entry(root)
pole_haslo = ttk.Entry(root, show="*")  # show="*" ukrywa wprowadzone hasło
lista_pytan = ttk.Combobox(root, values=["Jakie jest imię twojego zwierzaka?", "Gdzie urodziłeś się?", "Ulubiona książka?"])
pole_odpowiedzi = ttk.Entry(root)

# Utwórz przyciski do rejestracji i logowania
przycisk_zarejestruj = ttk.Button(root, text="Zarejestruj", command=zarejestruj)
przycisk_zaloguj = ttk.Button(root, text="Masz już konto? Zaloguj się", command=zaloguj)

# Rozmieszcz elementy na siatce
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


# Uruchom pętlę główną
root.mainloop()
