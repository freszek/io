import tkinter as tk
from tkinter import ttk, messagebox
from Database.database_setup import db


class StatsWindow:
    def __init__(self, stats, player_names):
        self.player_names = player_names
        self.player_id = stats[0]
        self.stats_frame = None
        self.player_stats = stats[1]
        self.root = tk.Tk()
        self.root.title("Statystyki gracza")
        self.root.geometry("900x400")
        self.root.resizable(False, True)
        self.root.configure(background="#c1ffc1")
        self.player_name_combobox = None

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        player_name_label = tk.Label(self.root, text="Statystyki", font=("Arial", 15, "bold"), bg="#c1ffc1")
        player_name_label.pack(pady=10)

        self.player_name_combobox = ttk.Combobox(self.root, values=self.player_names, font=("Arial", 15),
                                                 state="readonly", background="lightgreen")
        self.player_name_combobox.set("Wybierz gracza")
        self.player_name_combobox.pack(pady=10)

        search_button = tk.Button(self.root, text="Szukaj", command=self.search_statistics, width=15, height=1,
                                  font=("Arial", 15, "bold"), bg="darkgreen", fg="white")
        search_button.pack(pady=10)

        style = ttk.Style()
        style.configure("Stats.TFrame", background="#c1ffc1")
        style.configure("Stats.TButton", font=("Arial", 12, "bold"))

        self.stats_frame = ttk.Frame(self.root, style="Stats.TFrame")
        self.stats_frame.pack(pady=10)

    def search_statistics(self):
        self.clear_labels()
        player_name = self.player_name_combobox.get()
        if player_name and player_name != "Wybierz gracza":
            player_id = db.get_player_id(player_name)
            if player_id != -1 and self.player_id is not None and player_id == self.player_id:
                self.show_statistics()
            elif player_id != -1 and self.player_id is None:
                self.show_statistics()
            elif player_id != -1 and self.player_id is not None:
                ttk.Label(self.stats_frame, text="Brak statystyk!", font=("Arial", 15, "bold"), background="#c1ffc1",
                          foreground="black").grid(row=0, column=1, padx=10, pady=5, sticky="w")
            else:
                ttk.Label(self.stats_frame, text="Nie ma takiego gracza!", font=("Arial", 15, "bold"),
                          background="#c1ffc1", foreground="black").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        else:
            ttk.Label(self.stats_frame, text="Wybierz gracza!", font=("Arial", 15, "bold"), background="#c1ffc1",
                      foreground="black").grid(row=0, column=1, padx=10, pady=5, sticky="w")

    def clear_labels(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

    def show_statistics(self):
        if len(self.player_stats) != 0:
            ttk.Label(self.stats_frame, text="Wynik",
                      font=("Arial", 15, "bold"),
                      background="#c1ffc1").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(self.stats_frame, text="Czas",
                      font=("Arial", 15, "bold"),
                      background="#c1ffc1").grid(row=0, column=1, padx=10, pady=5, sticky="w")
            ttk.Label(self.stats_frame, text="Poziom",
                      font=("Arial", 15, "bold"),
                      background="#c1ffc1").grid(row=0, column=2, padx=10, pady=5, sticky="w")

            labels = []
            for i, stats in enumerate(self.player_stats):
                l_wynik = ttk.Label(self.stats_frame, text=str(stats[-3]), font=("Arial", 12), background="#c1ffc1")
                l_wynik.grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")
                labels.append(l_wynik)

                l_czas = ttk.Label(self.stats_frame, text=str(stats[-2]), font=("Arial", 12), background="#c1ffc1")
                l_czas.grid(row=i + 1, column=1, padx=10, pady=5, sticky="w")
                labels.append(l_czas)

                l_poziom = ttk.Label(self.stats_frame, text=str(stats[-1]), font=("Arial", 12), background="#c1ffc1")
                l_poziom.grid(row=i + 1, column=2, padx=10, pady=5, sticky="w")
                labels.append(l_poziom)

            if len(self.player_stats) > 1:
                last = len(self.player_stats)
                ttk.Button(self.stats_frame, text="Sortuj po wyniku", style="Stats.TButton",
                           command=lambda: self.sort_statistics(0, labels)).grid(row=last + 1, column=0, pady=5)
                ttk.Button(self.stats_frame, text="Sortuj po czasie", style="Stats.TButton",
                           command=lambda: self.sort_statistics(1, labels)).grid(row=last + 1, column=1, pady=5)
                ttk.Button(self.stats_frame, text="Sortuj po poziomie", style="Stats.TButton",
                           command=lambda: self.sort_statistics(2, labels)).grid(row=last + 1, column=2, pady=5)
        else:
            ttk.Label(self.stats_frame, text="Nie brałeś udziału w żadnym wydarzeniu!", font=("Arial", 15, "bold"),
                      background="#c1ffc1", foreground="black").grid(row=0, column=1, padx=10, pady=5, sticky="w")

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
