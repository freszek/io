import tkinter as tk
from tkinter import ttk, messagebox
from Database.database_setup import db


class StatsWindow:
    def __init__(self):
        self.stats_frame = None
        self.player_stats = None
        self.root = tk.Tk()
        self.root.title("Statystyki gracza")
        self.root.geometry("500x400")
        self.root.resizable(False, True)
        self.root.configure(background="lightblue")
        self.player_name_entry = None

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        player_name_label = tk.Label(self.root, text="Nazwa gracza:", font=("Arial", 15, "bold"), bg="lightblue")
        player_name_label.pack(pady=10)

        self.player_name_entry = tk.Entry(self.root, font=("Arial", 15), width=15, justify="center", bg="lightgreen")
        self.player_name_entry.pack(pady=10)

        search_button = tk.Button(self.root, text="Szukaj", command=self.search_statistics, width=15, height=1,
                                  font=("Arial", 15, "bold"), bg="darkgreen", fg="white")
        search_button.pack(pady=10)

        style = ttk.Style()
        style.configure("Stats.TFrame", background="lightblue")
        style.configure("Stats.TButton", font=("Arial", 12, "bold"))

        self.stats_frame = ttk.Frame(self.root, style="Stats.TFrame")
        self.stats_frame.pack(pady=10)

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
            for widget in self.stats_frame.winfo_children():
                widget.destroy()

            (ttk.Label(self.stats_frame, text="Wynik", font=("Arial", 15, "bold"), background="lightblue")
             .grid(row=0, column=0, padx=10, pady=5, sticky="w"))
            (ttk.Label(self.stats_frame, text="Czas", font=("Arial", 15, "bold"), background="lightblue")
             .grid(row=0, column=1, padx=10, pady=5, sticky="w"))
            (ttk.Label(self.stats_frame, text="Poziom", font=("Arial", 15, "bold"), background="lightblue")
             .grid(row=0, column=2, padx=10, pady=5, sticky="w"))

            labels = []
            for i, stats in enumerate(self.player_stats):
                label_wynik = ttk.Label(self.stats_frame, text=str(stats[-3]), font=("Arial", 12),
                                        background="lightblue")
                label_wynik.grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")
                labels.append(label_wynik)

                label_czas = ttk.Label(self.stats_frame, text=str(stats[-2]), font=("Arial", 12),
                                       background="lightblue")
                label_czas.grid(row=i + 1, column=1, padx=10, pady=5, sticky="w")
                labels.append(label_czas)

                label_poziom = ttk.Label(self.stats_frame, text=str(stats[-1]), font=("Arial", 12),
                                         background="lightblue")
                label_poziom.grid(row=i + 1, column=2, padx=10, pady=5, sticky="w")
                labels.append(label_poziom)

            last_row = len(self.player_stats)
            ttk.Button(self.stats_frame, text="Sortuj po wyniku", style="Stats.TButton",
                       command=lambda: self.sort_statistics(0, labels)).grid(row=last_row + 1, column=0, pady=5)
            ttk.Button(self.stats_frame, text="Sortuj po czasie", style="Stats.TButton",
                       command=lambda: self.sort_statistics(1, labels)).grid(row=last_row + 1, column=1, pady=5)
            ttk.Button(self.stats_frame, text="Sortuj po poziomie", style="Stats.TButton",
                       command=lambda: self.sort_statistics(2, labels)).grid(row=last_row + 1, column=2, pady=5)
        else:
            messagebox.showinfo("Brak statystyk", "Nie brałeś udziału w żadnym wydarzeniu!")

    def sort_statistics(self, specific, labels):
        level_order = {"EASY": 0, "MEDIUM": 1, "HARD": 2}
        if specific == 0:
            self.player_stats = sorted(self.player_stats, key=lambda x: x[-3], reverse=True)
        elif specific == 1:
            self.player_stats = sorted(self.player_stats, key=lambda x: x[-2])
        elif specific == 2:
            self.player_stats = sorted(self.player_stats, key=lambda x: level_order.get(x[-1], float('inf')))
        else:
            messagebox.showinfo("Błąd sortowania!")

        for i, stats in enumerate(self.player_stats):
            labels[i * 3].configure(text=str(stats[-3]))
            labels[i * 3 + 1].configure(text=str(stats[-2]))
            labels[i * 3 + 2].configure(text=str(stats[-1]))
