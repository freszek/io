import random
import tkinter as tk
from tkinter import ttk, messagebox
from DifficultyLevel import DifficultyLevel
from Event import Event
from database_setup import db


class QuizForm:
    def __init__(self):
        db_event = db.get_event(random.randint(1, 10))
        event = Event(db_event[0], db_event[1])
        if not event.can_player_join():
            messagebox.showinfo("Nie można dołączyć", "Nie możesz dołączyć do tego wydarzenia!")
            return
        self.level_var = None
        root = tk.Tk()
        self.next_button = None
        self.var = None
        self.question_label = None
        self.current_question = None
        self.questions = None
        self.event = event
        self.master = root
        self.master.title(event.get_name() + " Quiz")
        self.master.geometry("600x300")
        self.master.configure(background="#90EE90")

        self.player_id = 0  # TODO: wziąć id gracza zamiast 0, ale to scenariusz ma dac metode
        self.player_stats = []

        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, background="#90EE90", foreground="black", font=("Arial", 15),
                             width=30, height=30)
        self.style.configure("TLabel", padding=10, foreground="black", font=("Arial", 15))
        self.style.configure("TRadiobutton", padding=10, foreground="black", font=("Arial", 15))

        self.show_rules()

        self.master.mainloop()

    def choose_level(self):
        self.destroy_window()
        level_label = ttk.Label(self.master, text="Wybierz poziom")
        level_label.pack()

        self.level_var = tk.StringVar()
        levels = ["EASY", "MEDIUM", "HARD"]
        for level in levels:
            ttk.Radiobutton(self.master, text=level, variable=self.level_var, value=level).pack()
        level_button = ttk.Button(self.master, text="Rozpocznij quiz", command=self.start_quiz)
        level_button.pack()

    def show_rules(self):
        s = ("Zasady wydarzenia\n"
             "1. Nie oszukujemy!\n"
             "2. Nie można wracać do poprzednich pytań!\n"
             "3. Jest tylko jedna odpowiedź poprawna!\n"
             "4. Nie ma ujemnych punktów!\n"
             "5. Za poprawną odpowiedź dostajesz 1, 2 lub 3\n"
             "punkty w zależności od poziomu (łatwy, średni, trudny)")

        rules_label = ttk.Label(self.master, text=s)
        rules_label.pack()

        rules_button = ttk.Button(self.master, text="Zacznijmy!", command=self.choose_level)
        rules_button.pack()

    def start_quiz(self):
        selected_level = self.level_var.get()
        try:
            self.event.set_level(DifficultyLevel.from_string(selected_level))
        except ValueError:
            self.event.set_level(DifficultyLevel.EASY)
        self.event.start_event()

        self.destroy_window()

        self.questions = self.event.get_questions()
        self.current_question = 0

        self.question_label = ttk.Label(self.master, text=self.questions[0][2])
        self.question_label.pack()

        self.var = tk.IntVar()
        answers = self.questions[0][3:7]
        for i, answer in enumerate(answers):
            ttk.Radiobutton(self.master, text=answer, variable=self.var, value=i).pack()

        self.next_button = ttk.Button(self.master, text="Dalej", command=self.next_question)
        self.next_button.pack()

    def destroy_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def next_question(self):
        selected_answer = self.var.get()
        correct_answer = self.questions[self.current_question][7]
        self.check_answer(selected_answer, correct_answer)

        self.current_question += 1

        if self.current_question < len(self.questions):
            self.update_question()
        else:
            messagebox.showinfo("Koniec wydarzenia", "Odpowiedziałeś na pytania!\nTwój wynik: "
                                + str(self.event.get_score()))
            self.destroy_window()
            self.event.end_event()
            show_stats = ttk.Button(self.master, text="Zobacz statystyki", command=self.show_statistics)
            show_stats.pack()
            show_achievements = ttk.Button(self.master, text="Zobacz osiągnięcia", command=self.show_achievements)
            show_achievements.pack()
            end = ttk.Button(self.master, text="Zakończ podgląd", command=self.end_window)
            end.pack()

    def end_window(self):
        # db.close_connection()
        self.master.destroy()

    def update_question(self):
        self.destroy_window()
        self.question_label = ttk.Label(self.master, text=self.questions[self.current_question][2])
        self.question_label.pack()
        self.var.set(0)

        answers = self.questions[self.current_question][3:7]
        for i, answer in enumerate(answers):
            ttk.Radiobutton(self.master, text=answer, variable=self.var, value=i).pack()

        self.next_button = ttk.Button(self.master, text="Dalej", command=self.next_question)
        self.next_button.pack()

    def check_answer(self, selected, correct):
        if selected == correct:
            self.event.calculate_score()

    def show_statistics(self):
        self.player_stats = db.get_statistics(self.player_id)
        if self.player_stats:
            last_row = len(self.player_stats)
            stats_window = tk.Toplevel(self.master)
            stats_window.resizable(False, False)
            stats_window.title("Statystyki gracza " + db.get_player_name(self.player_id))

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

    def show_achievements(self):
        achievements = db.get_player_achievements(self.player_id)
        if achievements:
            achievements_window = tk.Toplevel(self.master)
            achievements_window.resizable(False, False)
            achievements_window.title("Osiągnięcia gracza " + db.get_player_name(self.player_id))

            ttk.Label(achievements_window, text="Nazwa").grid(row=0, column=0)
            ttk.Label(achievements_window, text="Opis").grid(row=0, column=1)

            labels = []
            for i, achievement in enumerate(achievements):
                label_name = ttk.Label(achievements_window, text=achievement[1])
                label_name.grid(row=i + 1, column=0)
                labels.append(label_name)

                label_description = ttk.Label(achievements_window, text=achievement[2])
                label_description.grid(row=i + 1, column=1)
                labels.append(label_description)
        else:
            messagebox.showinfo("Brak osiągnięć", "Nie masz żadnych osiągnięć!")
