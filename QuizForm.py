import random
import tkinter as tk
from tkinter import messagebox
from DifficultyLevel import DifficultyLevel
from database_setup import db
from Event import Event


class QuizForm:
    def __init__(self):
        db_event = db.get_event(random.randint(1, 10))
        event = Event(db_event[0], db_event[1], db_event[2])
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
        self.master.geometry("600x150")

        self.player_name = "0"
        self.player_stats = []

        self.show_rules()

        self.master.mainloop()

    def choose_level(self):
        self.destroy_window()
        level_label = tk.Label(self.master, text="Wybierz poziom")
        level_label.pack()

        self.level_var = tk.StringVar()
        levels = ["EASY", "MEDIUM", "HARD"]
        for level in levels:
            tk.Radiobutton(self.master, text=level, variable=self.level_var, value=level).pack()
        level_button = tk.Button(self.master, text="Rozpocznij quiz", command=self.start_quiz)
        level_button.pack()

    def show_rules(self):
        content = ("Zasady wydarzenia\n"
                   "1. Nie oszukujemy!\n"
                   "2. Nie można wracać do poprzednich pytań!\n"
                   "3. Jest tylko jedna odpowiedź poprawna!\n"
                   "4. Nie ma ujemnych punktów!\n"
                   "5. Za poprawną odpowiedź dostajesz 1, 2 lub 3\n"
                   "punkty w zależności od poziomu (łatwy, średni, trudny)")

        rules_label = tk.Label(self.master, text=content)
        rules_label.pack()

        rules_button = tk.Button(self.master, text="Zacznijmy!", command=self.choose_level)
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

        self.question_label = tk.Label(self.master, text=self.questions[0][2])
        self.question_label.pack()

        self.var = tk.IntVar()
        answers = self.questions[0][3:7]
        for i, answer in enumerate(answers):
            tk.Radiobutton(self.master, text=answer, variable=self.var, value=i).pack()

        self.next_button = tk.Button(self.master, text="Dalej", command=self.next_question)
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
            show_stats = tk.Button(self.master, text="Zobacz statystyki", command=self.show_statistics)
            show_stats.pack()
            end = tk.Button(self.master, text="Zakończ podgląd", command=self.end_window)
            end.pack()

    def end_window(self):
        self.event.end_event()
        db.close_connection()
        self.master.destroy()

    def update_question(self):
        self.destroy_window()
        self.question_label = tk.Label(self.master, text=self.questions[self.current_question][2])
        self.question_label.pack()
        self.var.set(0)

        answers = self.questions[self.current_question][3:7]
        for i, answer in enumerate(answers):
            tk.Radiobutton(self.master, text=answer, variable=self.var, value=i).pack()

        self.next_button = tk.Button(self.master, text="Dalej", command=self.next_question)
        self.next_button.pack()

    def check_answer(self, selected, correct):
        if selected == correct:
            self.event.calculate_score()

    def show_statistics(self):
        self.player_stats = db.get_statistics(self.player_name)
        if self.player_stats:
            last_row = len(self.player_stats)
            stats_window = tk.Toplevel(self.master)
            stats_window.title("Statystyki gracza " + self.player_name)

            tk.Label(stats_window, text="Wynik").grid(row=0, column=0)
            tk.Label(stats_window, text="Czas").grid(row=0, column=1)

            labels = []
            for i, stats in enumerate(self.player_stats):
                label_wynik = tk.Label(stats_window, text=str(stats[-2]))
                label_wynik.grid(row=i + 1, column=0)
                labels.append(label_wynik)

                label_czas = tk.Label(stats_window, text=str(stats[-1]))
                label_czas.grid(row=i + 1, column=1)
                labels.append(label_czas)

            tk.Button(stats_window, text="Sortuj po wyniku",
                      command=lambda: self.sort_statistics(0, labels)).grid(row=last_row, column=0)
            tk.Button(stats_window, text="Sortuj po czasie",
                      command=lambda: self.sort_statistics(1, labels)).grid(row=last_row, column=1)
        else:
            messagebox.showinfo("Brak statystyk", "Nie brałeś udziału w żadnym wydarzeniu!")

    def sort_statistics(self, specific, labels):
        if specific == 0:
            self.player_stats = sorted(self.player_stats, key=lambda x: x[-2])
        elif specific == 1:
            self.player_stats = sorted(self.player_stats, key=lambda x: x[-1])
        else:
            messagebox.showinfo("Błąd sortowania!")

        for i, stats in enumerate(self.player_stats):
            labels[i * 2].config(text=str(stats[-2]))
            labels[i * 2 + 1].config(text=str(stats[-1]))

    def show_achievements(self):
        pass
