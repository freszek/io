import tkinter as tk
from tkinter import ttk
from Database.database_setup import db


class AchievementsWindow:
    def __init__(self, data, player_names):
        self.player_names = player_names
        self.achieve_frame = None
        self.player_achievements = data[1]
        self.player_id = data[0]
        self.root = tk.Tk()
        self.root.title("Osiągnięcia graczy")
        self.root.geometry("900x400")
        self.root.resizable(False, True)
        self.root.configure(background="#c1ffc1")

        self.player_name_combobox = None

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        player_name_label = tk.Label(self.root, text="Osiągnięcia", font=("Arial", 15, "bold"), bg="#c1ffc1",
                                     fg="black")
        player_name_label.pack(pady=10)

        self.player_name_combobox = ttk.Combobox(self.root, values=self.player_names, font=("Arial", 15), width=15,
                                                 justify="center", state="readonly", background="lightgreen",
                                                 foreground="black")
        self.player_name_combobox.set("Wybierz gracza")
        self.player_name_combobox.pack(pady=10)

        search_button = tk.Button(self.root, text="Szukaj", command=self.search_achievements, width=15, height=1,
                                  font=("Arial", 12, "bold"), bg="darkgreen", fg="white")
        search_button.pack(pady=10)

        style = ttk.Style()
        style.configure("Achievements.TFrame", background="#c1ffc1")

        self.achieve_frame = ttk.Frame(self.root, style="Achievements.TFrame")
        self.achieve_frame.pack(pady=10)

    def search_achievements(self):
        self.clear_labels()
        player_name = self.player_name_combobox.get()
        if player_name and player_name != "Wybierz gracza":
            player_id = db.get_player_id(player_name)
            if player_id != -1 and self.player_id is not None and player_id == self.player_id:
                self.show_achievements()
            elif player_id != -1 and self.player_id is None:
                self.show_achievements()
            elif player_id != -1 and self.player_id is not None:
                ttk.Label(self.achieve_frame, text="Brak osiągnięć!", font=("Arial", 15, "bold"), background="#c1ffc1",
                          foreground="black").grid(row=0, column=1, padx=10, pady=5, sticky="w")
            else:
                ttk.Label(self.achieve_frame, text="Nie ma takiego gracza!", font=("Arial", 15, "bold"),
                          background="#c1ffc1", foreground="black").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        else:
            ttk.Label(self.achieve_frame, text="Wybierz gracza!", font=("Arial", 15, "bold"),
                      background="#c1ffc1", foreground="black").grid(row=0, column=1, padx=10, pady=5, sticky="w")

    def clear_labels(self):
        for widget in self.achieve_frame.winfo_children():
            widget.destroy()

    def show_achievements(self):
        if len(self.player_achievements) != 0:
            ttk.Label(self.achieve_frame, text="Nazwa osiągnięcia", font=("Arial", 15, "bold"), background="#c1ffc1",
                      foreground="black").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(self.achieve_frame, text="Opis", font=("Arial", 15, "bold"), background="#c1ffc1",
                      foreground="black").grid(row=0, column=1, padx=10, pady=5, sticky="w")
            ttk.Label(self.achieve_frame, text="Liczba graczy", font=("Arial", 15, "bold"), background="#c1ffc1",
                      foreground="black").grid(row=0, column=2, padx=10, pady=5, sticky="w")

            labels = []
            for i, achievement in enumerate(self.player_achievements):
                label_name = ttk.Label(self.achieve_frame, text=achievement[1], font=("Arial", 12), wraplength=300,
                                       justify="left", anchor="w", width=30, padding=5, relief="groove", borderwidth=2,
                                       background="lightgreen", foreground="black")
                label_name.grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")
                labels.append(label_name)

                label_desc = ttk.Label(self.achieve_frame, text=achievement[2], font=("Arial", 12), wraplength=500,
                                       justify="left", anchor="w", width=30, padding=5, relief="groove", borderwidth=2,
                                       background="#c1ffc1", foreground="black")
                label_desc.grid(row=i + 1, column=1, padx=10, pady=5, sticky="w")
                labels.append(label_desc)

                num_players = db.count_achievements(achievement[0])
                ttk.Label(self.achieve_frame, text=num_players, font=("Arial", 12), wraplength=100,
                          justify="left", anchor="w", width=10, padding=5, relief="groove", borderwidth=2,
                          background="lightgreen", foreground="black").grid(row=i + 1, column=2, padx=10,
                                                                            pady=5, sticky="w")
        else:
            ttk.Label(self.achieve_frame, text="Brak osiągnięć!", font=("Arial", 15, "bold"), background="#c1ffc1",
                      foreground="black").grid(row=0, column=1, padx=10, pady=5, sticky="w")
