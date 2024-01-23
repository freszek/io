import tkinter as tk
from tkinter import ttk, messagebox
from Database.database_setup import db


class AchievementsWindow:
    def __init__(self):
        self.achieve_frame = None
        self.player_achievements = None
        self.root = tk.Tk()
        self.root.title("Osiągnięcia gracza")
        self.root.geometry("700x200")
        self.root.resizable(False, True)
        self.root.configure(background="lightblue")

        self.player_name_entry = None

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        player_name_label = tk.Label(self.root, text="Nazwa gracza:", font=("Arial", 12, "bold"), bg="lightblue")
        player_name_label.pack(pady=10)

        self.player_name_entry = tk.Entry(self.root, font=("Arial", 12), width=15, justify="center", bg="lightgreen")
        self.player_name_entry.pack(pady=10)

        search_button = tk.Button(self.root, text="Szukaj", command=self.search_achievements, width=15, height=1,
                                  font=("Arial", 12, "bold"), bg="darkgreen", fg="white")
        search_button.pack(pady=10)

        style = ttk.Style()
        style.configure("Achievements.TFrame", background="lightblue")

        self.achieve_frame = ttk.Frame(self.root, style="Achievements.TFrame")
        self.achieve_frame.pack(pady=10)

    def search_achievements(self):
        player_name = self.player_name_entry.get()
        player_id = db.get_player_id(player_name)
        if player_id != -1:
            self.show_achievements(player_id)
        elif len(player_name) == 0:
            messagebox.showwarning("Błąd!", "Wpisz nazwę gracza!")
        else:
            messagebox.showwarning("Błąd!", "Nie ma takiego gracza!")

    def show_achievements(self, player_id):
        self.player_achievements = db.get_player_achievements(player_id)
        if self.player_achievements:
            for widget in self.achieve_frame.winfo_children():
                widget.destroy()

            (ttk.Label(self.achieve_frame, text="Nazwa osiągnięcia", font=("Arial", 15, "bold"), background="lightblue")
             .grid(row=0, column=0, padx=10, pady=5, sticky="w"))
            (ttk.Label(self.achieve_frame, text="Opis", font=("Arial", 15, "bold"), background="lightblue")
             .grid(row=0, column=1, padx=10, pady=5, sticky="w"))

            labels = []
            for i, achievement in enumerate(self.player_achievements):
                label_name = ttk.Label(self.achieve_frame, text=achievement[1], font=("Arial", 12), wraplength=300,
                                       justify="left", anchor="w", width=30, padding=5, relief="groove", borderwidth=2,
                                       background="lightgreen", foreground="black")
                label_name.grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")
                labels.append(label_name)

                label_desc = ttk.Label(self.achieve_frame, text=achievement[2], font=("Arial", 12), wraplength=500,
                                       justify="left", anchor="w", width=30, padding=5, relief="groove", borderwidth=2)
                label_desc.grid(row=i + 1, column=1, padx=10, pady=5, sticky="w")
                labels.append(label_desc)
        else:
            messagebox.showinfo("Błąd!", "Gracz nie posiada żadnych osiągnięć!")
