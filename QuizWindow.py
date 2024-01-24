import random
import tkinter as tk
from tkinter import ttk, messagebox
from DifficultyLevel import DifficultyLevel, to_string
from Event import Event
from database_setup import db
import time


class QuizWindow:
    def __init__(self, player_name):
        db_event = db.get_event(random.randint(1, 10))
        event = Event(db_event[0], db_event[1])

        self.event = event
        self.player_id = db.get_player_id(player_name)
        self.player_data = []

        self.start_time = 0
        self.time_limit = 0

        check = event.can_player_join(self.player_id)

        if check == -1:
            messagebox.showinfo("Błąd", "Za dużo punktów uzyskałeś w eventach!")
            db.save_statistics(event.event_id, self.player_id, 0, 0, to_string(event.level))
            return
        elif check == -2:
            messagebox.showinfo("Błąd", "Zdobyłeś wszystkie osiągnięcia w eventach!")
            return

        self.level_var = None
        self.next_button = None
        self.var = None
        self.question_label = None
        self.current_question = None
        self.questions = None
        self.root = tk.Tk()
        self.root.title(f"{event.get_name()} Quiz")
        self.root.geometry("900x400")
        self.root.configure(background="#B0E57C")

        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, foreground="black", font=("Arial", 15), width=30, height=30,
                             background="#60A060")
        self.style.configure("TLabel", padding=10, foreground="black", font=("Arial", 15), background="#B0E57C")
        self.style.configure("TRadiobutton", padding=10, foreground="black", font=("Arial", 15),
                             background="#B0E57C")

        self.show_rules()

        self.root.mainloop()

    def choose_level(self):
        self.destroy_window()
        level_label = ttk.Label(self.root, text="Wybierz poziom", style="TLabel")
        level_label.pack()

        self.level_var = tk.StringVar()
        levels = ("EASY", "MEDIUM", "HARD")
        poziomy = ("Łatwy", "Średni", "Trudny")
        for i, level in enumerate(levels):
            ttk.Radiobutton(self.root, text=poziomy[i], variable=self.level_var, value=level,
                            style="TRadiobutton").pack()

        level_button = ttk.Button(self.root, text="Rozpocznij quiz", command=self.start_quiz, style="TButton")
        level_button.pack()

    def show_rules(self):
        s = (
            "Zasady wydarzenia\n"
            "1. Nie oszukujemy!\n"
            "2. Nie można wracać do poprzednich pytań!\n"
            "3. Jest tylko jedna odpowiedź poprawna!\n"
            "4. Nie ma ujemnych punktów!\n"
            "5. Za poprawną odpowiedź dostajesz 1, 2 lub 3\n"
            "   punkty w zależności od poziomu (łatwy, średni, trudny)\n"
            "6. Jeśli posiadasz osiągnięcie Legenda albo przekraczasz 90% możliwych\n   punktów w obecnym evencie to"
            "nie możesz rozpocząć eventu."
        )

        rules_label = ttk.Label(self.root, text=s, style="TLabel")
        rules_label.pack()

        rules_button = ttk.Button(self.root, text="Zacznij!", command=self.choose_level, style="TButton")
        rules_button.pack()

    def start_quiz(self):
        selected_level = self.level_var.get()
        try:
            self.event.set_level(DifficultyLevel.from_string(selected_level))
        except ValueError:
            self.event.set_level(DifficultyLevel.EASY)
        self.event.start_event()

        if self.event.get_level() == DifficultyLevel.EASY:
            self.time_limit = 13
        elif self.event.get_level() == DifficultyLevel.MEDIUM:
            self.time_limit = 8
        else:
            self.time_limit = 5

        self.destroy_window()

        self.questions = self.event.get_questions()
        self.current_question = 0

        self.question_label = ttk.Label(self.root, text=self.questions[0][2], style="TLabel")
        self.question_label.pack()

        self.var = tk.IntVar()
        answers = self.questions[0][3:7]
        for i, answer in enumerate(answers):
            ttk.Radiobutton(self.root, text=answer, variable=self.var, value=i, style="TRadiobutton").pack()

        self.next_button = ttk.Button(self.root, text="Dalej", command=self.next_question, style="TButton")
        self.next_button.pack()

        self.start_time = time.perf_counter()

        self.event.start_time = self.start_time

        self.root.after(10, self.check_time_limit)

    def check_time_limit(self):
        time_elapsed = time.perf_counter() - self.start_time
        if time_elapsed >= self.time_limit and self.current_question != len(self.questions):
            messagebox.showinfo("Czas minął", "Przekroczyłeś limit czasu!")
            self.destroy_window()
            self.player_data = self.event.end_event(self.player_id, time_elapsed=round(time_elapsed, 3))
            self.end_window()
        else:
            self.root.after(10, self.check_time_limit)

    def destroy_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def next_question(self):
        selected_answer = self.var.get()
        correct_answer = self.questions[self.current_question][7]
        self.check_answer(selected_answer, correct_answer)

        self.current_question += 1

        if self.current_question < len(self.questions):
            self.update_question()
        else:
            messagebox.showinfo(
                "Koniec wydarzenia", f"Odpowiedziałeś na pytania!\nTwój wynik: {self.event.get_score()}"
            )
            self.destroy_window()
            self.player_data = self.event.end_event(self.player_id)
            self.end_window()

    def end_window(self):
        self.root.destroy()

    def update_question(self):
        self.destroy_window()
        self.question_label = ttk.Label(self.root, text=self.questions[self.current_question][2], style="TLabel")
        self.question_label.pack()
        self.var.set(0)

        answers = self.questions[self.current_question][3:7]
        for i, answer in enumerate(answers):
            ttk.Radiobutton(self.root, text=answer, variable=self.var, value=i, style="TRadiobutton").pack()

        self.next_button = ttk.Button(self.root, text="Dalej", command=self.next_question, style="TButton")
        self.next_button.pack()

    def check_answer(self, selected, correct):
        if selected == correct:
            self.event.calculate_score()
