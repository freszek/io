import tkinter as tk
from tkinter import ttk, messagebox
from database_setup import db


class StatsWindow:
    def __init__(self):
        self.player_stats = None
        self.root = tk.Tk()
        self.root.title("Statystyki gracza")
        self.root.geometry("800x200")
        self.player_name_entry = None

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        self.root.geometry("800x200")
        for widget in self.root.winfo_children():
            widget.destroy()
        event_id_label = tk.Label(self.root, text="Nazwa gracza:")
        event_id_label.pack(pady=10)

        self.player_name_entry = tk.Entry(self.root)
        self.player_name_entry.pack(pady=10)

        search_button = tk.Button(self.root, text="Szukaj", command=self.search_statistics)
        search_button.pack(pady=10)

    def search_statistics(self):
        player_name = self.player_name_entry.get()
        player_id = db.get_player_id(player_name)
        if player_id != -1:
            self.show_statistics(player_id)
        elif len(player_name) == 0:
            messagebox.showwarning("Błąd!", "Wpisz nazwę gracza!")
        else:
            messagebox.showwarning("Błąd!", "Nie ma takiego gracza!")

    def show_statistics(self, player_id):
        self.player_stats = db.get_statistics(player_id)
        if self.player_stats:
            last_row = len(self.player_stats)
            stats_window = tk.Toplevel(self.root)
            stats_window.resizable(False, False)
            stats_window.title("Statystyki gracza " + db.get_player_name(player_id))

            ttk.Label(stats_window, text="Wynik").grid(row=0, column=0)
            ttk.Label(stats_window, text="Czas").grid(row=0, column=1)
            ttk.Label(stats_window, text="Poziom").grid(row=0, column=2)

            labels = []
            for i, stats in enumerate(self.player_stats):
                label_wynik = ttk.Label(stats_window, text=str(stats[-3]))
                label_wynik.grid(row=i + 1, column=0)
                labels.append(label_wynik)

                label_czas = ttk.Label(stats_window, text=str(stats[-2]))
                label_czas.grid(row=i + 1, column=1)
                labels.append(label_czas)

                label_poziom = ttk.Label(stats_window, text=str(stats[-1]))
                label_poziom.grid(row=i + 1, column=2)
                labels.append(label_poziom)

            ttk.Button(stats_window, text="Sortuj po wyniku",
                       command=lambda: self.sort_statistics(0, labels)).grid(row=last_row + 1, column=0)
            ttk.Button(stats_window, text="Sortuj po czasie",
                       command=lambda: self.sort_statistics(1, labels)).grid(row=last_row + 1, column=1)
            ttk.Button(stats_window, text="Sortuj po poziomie",
                       command=lambda: self.sort_statistics(2, labels)).grid(row=last_row + 1, column=2)
        else:
            messagebox.showinfo("Brak statystyk", "Nie brałeś udziału w żadnym wydarzeniu!")

    def sort_statistics(self, specific, labels):
        if specific == 0:
            self.player_stats = sorted(self.player_stats, key=lambda x: x[-3], reverse=True)
        elif specific == 1:
            self.player_stats = sorted(self.player_stats, key=lambda x: x[-2])
        elif specific == 2:
            self.player_stats = sorted(self.player_stats, key=lambda x: x[-1])
        else:
            messagebox.showinfo("Błąd sortowania!")

        for i, stats in enumerate(self.player_stats):
            labels[i * 3].configure(text=str(stats[-3]))
            labels[i * 3 + 1].configure(text=str(stats[-2]))
            labels[i * 3 + 2].configure(text=str(stats[-1]))
