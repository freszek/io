import tkinter as tk
from tkinter import ttk, messagebox
from database_setup import db


class AchievementsWindow:
    def __init__(self):
        self.player_achievements = None
        self.root = tk.Tk()
        self.root.title("Osiągnięcia gracza")
        self.root.geometry("800x200")
        self.player_name_entry = None

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        self.root.geometry("800x200")
        for widget in self.root.winfo_children():
            widget.destroy()
        player_name_label = tk.Label(self.root, text="Nazwa gracza:")
        player_name_label.pack(pady=10)

        self.player_name_entry = tk.Entry(self.root)
        self.player_name_entry.pack(pady=10)

        search_button = tk.Button(self.root, text="Szukaj", command=self.search_achievements)
        search_button.pack(pady=10)

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
            achievements_window = tk.Toplevel(self.root)
            achievements_window.resizable(False, False)
            achievements_window.title("Osiągnięcia gracza - " + db.get_player_name(player_id))

            ttk.Label(achievements_window, text="Nazwa osiągnięcia").grid(row=0, column=0)
            ttk.Label(achievements_window, text="Opis").grid(row=0, column=1)

            labels = []
            for i, achievement in enumerate(self.player_achievements):
                label_name = ttk.Label(achievements_window, text=achievement[1])
                label_name.grid(row=i + 1, column=0)
                labels.append(label_name)

                label_description = ttk.Label(achievements_window, text=achievement[2])
                label_description.grid(row=i + 1, column=1)
                labels.append(label_description)
        else:
            messagebox.showinfo("Błąd!", "Gracz nie posiada żadnych osiągnięć!")
