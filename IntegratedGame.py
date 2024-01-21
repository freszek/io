from datetime import datetime, timedelta
import mglobals
from game_rules import GameRulesApp
from player_avatar import PlayerAvatar
import hashlib
import sqlite3
from typing import List
import pygame
import sys
from FriendList import FriendList, Button
import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess


# from gierka import show_menu_and_start_game

# DEFINICJE KLAS ITP
class User:
    def __init__(self, id, login, password, email, answer, question):
        self.id = id
        self.login = login
        self.password = password
        self.email = email
        self.is_logged = 0
        self.answer = answer
        self.question = question


class Points:
    def __init__(self, value, date, category):
        self.value = value
        self.date = date
        self.category = category

    def get_value(self):
        return self.value

    def get_date(self):
        return self.date

    def get_category(self):
        return self.category

    def set_value(self, value):
        self.value = value

    def set_date(self, date):
        self.date = date

    def set_category(self, category):
        self.category = category


class UserDao:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()
        self.create_points_table()

    def get_ranking_data(self, user_list, period='daily'):
        ranking = {}

        # Ustalenie zakresu dat dla okresu
        current_date = datetime.now()
        if period == 'daily':
            start_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'weekly':
            start_date = current_date - timedelta(days=current_date.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        for user in user_list:
            user_points = self.get_user_points(user.id)
            for point in user_points:
                point_date = datetime.strptime(point.date, '%Y-%m-%d')
                if start_date <= point_date < current_date:
                    if user.login not in ranking:
                        ranking[user.login] = 0
                    ranking[user.login] += point.value

        # Sortowanie wyników w celu utworzenia rankingu
        sorted_ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
        return sorted_ranking

    def get_friends_ranking_data(self, user_id: int, period='daily'):
        ranking = {}

        # Ustalenie zakresu dat dla okresu
        current_date = datetime.now()
        if period == 'daily':
            start_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'weekly':
            start_date = current_date - timedelta(days=current_date.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # Pobranie listy ID znajomych
        friend_ids = self.get_friend_list(user_id)

        # Pobranie punktów dla każdego znajomego
        for friend_id in friend_ids:
            friend_points = self.get_user_points(friend_id)
            for point in friend_points:
                point_date = datetime.strptime(point.date, '%Y-%m-%d')
                if start_date <= point_date < current_date:
                    friend = self.get_by_id(friend_id)
                    if friend.login not in ranking:
                        ranking[friend.login] = 0
                    ranking[friend.login] += point.value

        # Sortowanie wyników
        sorted_ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
        return sorted_ranking

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            answer TEXT,
            question TEXT
        )
        '''
        query1 = '''
        CREATE TABLE IF NOT EXISTS user_friends (
            user_id INTEGER,
            friend_id INTEGER,
            PRIMARY KEY (user_id, friend_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (friend_id) REFERENCES users(id)
        );
        '''
        self.conn.execute(query)
        self.conn.commit()
        self.conn.execute(query1)
        self.conn.commit()

    def get_all(self) -> List[User]:
        query = 'SELECT * FROM users'
        cursor = self.conn.execute(query)
        result = cursor.fetchall()

        users = []
        for user in result:
            users.append(User(user[0], user[1], user[2], user[3], user[4], user[5]))
        return users

    def get_by_id(self, user_id: int) -> User:
        query = 'SELECT * FROM users WHERE id = ?'
        cursor = self.conn.execute(query, (user_id,))
        result = cursor.fetchone()
        try:
            return User(result[0], result[1], result[2], result[3], result[4], result[5])
        except:
            print("User not found")

    def get_by_login(self, login) -> User:
        query = 'SELECT * FROM users WHERE login = ?'
        cursor = self.conn.execute(query, (login,))
        result = cursor.fetchone()
        try:
            return User(result[0], result[1], result[2], result[3], result[4], result[5])
        except:
            print("User not found")

    def create_user(self, user: User) -> bool:
        query = 'INSERT INTO users (login, password, email, answer, question) VALUES (?, ?, ?, ?, ?)'
        try:
            self.conn.execute(query,
                              (user.login, self.hash_password(user.password), user.email, user.answer, user.question))
            self.conn.commit()
            return True
        except:
            return False

    def update_user(self, user: User, password: str) -> bool:
        hashed_password = self.hash_password(password)
        query = 'UPDATE users SET password = ? WHERE id = ?'
        try:
            self.conn.execute(query, (hashed_password, user.id))
            self.conn.commit()
            return True
        except:
            return False

    def delete_user(self, user: User) -> bool:
        query = 'DELETE FROM users WHERE id = ?'
        try:
            self.conn.execute(query, (user.id,))
            self.conn.commit()
            return True
        except:
            return False

    def get_friend_list(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
                SELECT friend_id FROM user_friends WHERE user_id = ?
            ''', (user_id,))  # Zauważ użycie przecinka, aby utworzyć krotkę jednoelementową

        friends = cursor.fetchall()

        friend_ids = [friend[0] for friend in friends]
        return friend_ids

    def delete_friend(self, user_id, friend_id):
        cursor = self.conn.cursor()

        query = "DELETE FROM user_friends WHERE user_id = ? AND friend_id = ?"
        cursor.execute(query, (user_id, friend_id))
        self.conn.commit()

        cursor.close()

    def create_points_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_name TEXT NOT NULL,
            points INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def get_user_points(self, user_id: int):
        query = 'SELECT points, date, category_name FROM points WHERE user_id = ?'
        cursor = self.conn.execute(query, (user_id,))
        results = cursor.fetchall()

        points_list = []
        for result in results:
            points = Points(result[0], result[1], result[2])
            points_list.append(points)

        return points_list

    def add_points(self, user_id: int, points: int, date: str, category_name: str) -> bool:
        query = 'INSERT INTO points (user_id, points, date, category_name) VALUES (?, ?, ?, ?)'
        try:
            self.conn.execute(query, (user_id, points, date, category_name))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def close(self):
        self.conn.close()


class SessionController:
    def __init__(self):
        self.session_user = None
        self.user_dao = UserDao()
        self.counter = 0

    def register(self, login, password, email, answer, question):
        if self.check_login(login):
            print("Uzytkownik o tym loginie juz istnieje!")
            return

        user = User(0, login, password, email, question, answer)
        self.session_user = user
        self.user_dao.create_user(user)
        print(f"ZAREJESTROWANY {login}")

    def check_login(self, login: str) -> bool:
        users = self.user_dao.get_all()
        return any(user.login == login for user in users)

    def check_password(self, login: str, password: str) -> bool:
        user = self.user_dao.get_by_login(login)
        if user:
            hashed_password = self.user_dao.hash_password(password)
            return user.password == hashed_password
        return False

    def log_in(self, login: str, password: str, answer: str) -> bool:
        if answer != "":
            if self.check_login(login) and self.check_answer(login, answer):
                print("ZALOGOWANY")
                self.session_user = self.user_dao.get_by_login(login)
                self.session_user.is_logged = True
                return True

        else:
            if self.check_login(login) and self.check_password(login, password):
                print("ZALOGOWANY")
                self.session_user = self.user_dao.get_by_login(login)
                self.session_user.is_logged = True
                return True
        print("Niezalogowany")
        return False

    def check_if_logged(self) -> bool:
        return self.session_user.is_logged

    def check_answer(self, login: str, answer: str) -> bool:
        user = self.user_dao.get_by_login(login)
        return user.answer == answer

    def log_out(self, login: str):
        user = self.user_dao.get_by_login(login)
        if user:
            user.is_logged = False

    def delete_user(self, password: str) -> bool:
        print(self.session_user)
        if self.check_password(self.session_user.login, password):
            self.user_dao.delete_user(self.session_user)
            self.log_out(self.session_user.login)
            return True
        return False

    def change_password(self, current_password: str, new_password: str) -> bool:
        if self.check_password(self.session_user.login, current_password):
            self.user_dao.update_user(self.session_user, new_password)
            return True
        return False

    def close(self):
        self.user_dao.close()


# WSZELAKO ROZUMIANA DEFINICJA GUI
session = SessionController()

settings_opened = False
ranking_opened = False


def change_password_form():
    def confirm_change_password(frame):
        password = entry_password.get()
        new_password = entry_new_password.get()
        if len(new_password) >= 8:
            if not session.change_password(password, new_password):
                messagebox.showwarning(title="Błąd", message="Niepoprawne stare hasło.")
            else:
                messagebox.showinfo(title="Komunikat", message="Hasło zmienione.")
                frame.destroy()
        else:
            messagebox.showwarning(title="Błąd", message="Nowe hasło jest za krótkie (min. 8 znaków).")

    root = tk.Tk()
    root.title("GreenGame")
    root.resizable(False, False)
    root.geometry("800x600+560+240")

    image = Image.open("background.jpg")
    background_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    label_password = ctk.CTkLabel(root, text="Stare hasło:", fg_color=("white", "gray75"),
                                  text_color="black", width=150, corner_radius=0)
    label_password.place(x=240, y=150)
    entry_password = ctk.CTkEntry(root, corner_radius=0, width=150, show="*")
    entry_password.place(x=410, y=150)

    label_new_password = ctk.CTkLabel(root, text="Nowe hasło:", fg_color=("white", "gray75"),
                                      text_color="black", width=150, corner_radius=0)
    label_new_password.place(x=240, y=200)
    entry_new_password = ctk.CTkEntry(root, show="*", corner_radius=0, width=150)
    entry_new_password.place(x=410, y=200)

    confirm_button = ctk.CTkButton(root, text="Zmień hasło", command=lambda: confirm_change_password(root),
                                   corner_radius=0, fg_color=("#60A060"),
                                   hover_color=("#006400"), )
    confirm_button.place(x=325, y=250)

    global session
    root.mainloop()

    # session.close()


def log_out():
    global settings_opened, session
    print(session.session_user.login)
    settings_opened = False
    session.close()
    pygame.quit()
    main_login_window(None)


def delete_user_form():
    def confirm_delete_user(frame):
        password = entry_password.get()
        if session.delete_user(password):
            messagebox.showwarning(title="Błąd", message="Użytkownik usunięty.")
            frame.destroy()
            pygame.quit()
            main_login_window(None)
        else:
            messagebox.showwarning(title="Błąd", message="Złe hasło.")

    root = tk.Tk()
    root.title("GreenGame")
    root.resizable(False, False)
    root.geometry("800x600+560+240")

    image = Image.open("background.jpg")
    background_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    label_password = ctk.CTkLabel(root, text="Hasło:", corner_radius=0, width=150, fg_color=("white", "gray75"),
                                  text_color="black")
    label_password.place(x=240, y=200)
    entry_password = ctk.CTkEntry(root, show="*", corner_radius=0, width=150)
    entry_password.place(x=410, y=200)

    confirm_button = ctk.CTkButton(root, text="Usuń użytkownika", command=lambda: confirm_delete_user(root),
                                   corner_radius=0, width=150, fg_color=("#60A060"),
                                   hover_color=("#006400"))
    confirm_button.place(x=325, y=250)

    global session
    root.mainloop()

    session.close()


def register_in(email, login, password, answer, question):
    global session
    if "" in (email, login, password, question, answer):
        messagebox.showwarning(title="Bład", message="Nie wszystkie dane.")
        return

    if len(password) < 8:
        messagebox.showwarning(title="Błąd", message="Za krótkie hasło(min. 8 znaków).")
        return
    if session.check_login(login):
        messagebox.showwarning(title="Błąd", message="Taki użytkownik istnieje. Zaloguj.")
    if session.register(login, password, email, answer, question):
        messagebox.showinfo(title="Komunikat", message="Użytkownik utworzony.")


def register(frame):
    frame.destroy()
    temp = tk.Tk()
    temp.title("GreenGame")
    temp.resizable(False, False)
    temp.geometry("800x600+560+240")

    image = Image.open("background.jpg")
    background_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(temp, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    email_string = ctk.CTkLabel(temp, text="Email:", fg_color=("white", "gray75"), text_color="black",
                                width=150)
    login_string = ctk.CTkLabel(temp, text="Login:", fg_color=("white", "gray75"), text_color="black",
                                width=150)
    password_string = ctk.CTkLabel(temp, text="Hasło:", fg_color=("white", "gray75"),
                                   text_color="black", width=150)
    question_string = ctk.CTkLabel(temp, text="Pytanie:", fg_color=("white", "gray75"),
                                   text_color="black", width=150)
    answer_string = ctk.CTkLabel(temp, text="Odpowiedź:", fg_color=("white", "gray75"),
                                 text_color="black",
                                 width=150)

    email_field = ctk.CTkEntry(temp, corner_radius=0, width=150)
    login_field = ctk.CTkEntry(temp, corner_radius=0, width=150)
    password_field = ctk.CTkEntry(temp, show="*", corner_radius=0, width=150)
    questions_field = ctk.CTkComboBox(temp,
                                      values=["Ulubione zwierze?", "Gdzie się urodziłes?", "Ulubiona Książka?"],
                                      corner_radius=0, width=150)
    answer_field = ctk.CTkEntry(temp, corner_radius=0, width=150)

    register_button = ctk.CTkButton(temp, text="Zarejestruj",
                                    command=lambda: register_in(email_field.get(), login_field.get(),
                                                                password_field.get(), answer_field.get(),
                                                                questions_field.get()), fg_color=("#60A060"),
                                    hover_color=("#006400"), corner_radius=0, width=150)
    back_button = ctk.CTkButton(temp, text="Powrót",
                                command=lambda: main_login_window(temp), fg_color=("#60A060"),
                                hover_color=("#006400"), corner_radius=0, width=150)

    email_string.place(x=240, y=50)
    login_string.place(x=240, y=100)
    password_string.place(x=240, y=150)
    question_string.place(x=240, y=200)
    answer_string.place(x=240, y=250)

    email_field.place(x=410, y=50)
    login_field.place(x=410, y=100)
    password_field.place(x=410, y=150)
    questions_field.place(x=410, y=200)
    answer_field.place(x=410, y=250)

    register_button.place(x=240, y=300)

    back_button.place(x=410, y=300)

    temp.mainloop()


def log_in(login, password, answer, frame):
    global session
    if session.counter >= 5:
        messagebox.showwarning(title="Błąd", message="Za dużo prób.")
    if not session.log_in(login, password, answer):
        messagebox.showwarning(title="Błąd", message="Złe dane.")
    if session.check_if_logged():
        frame.destroy()
        main_game_loop()


def answer_log_in(login, password, answer):
    global session
    session = SessionController()
    if login == "" or answer == "":
        messagebox.showwarning(title="Błąd", message="Wprowadź dane.")
    session.log_in(login, password, answer)


def answer_login(frame):
    frame.destroy()
    temp = tk.Tk()
    temp.title("GreenGame")
    temp.resizable(False, False)
    temp.geometry("800x600+560+240")

    image = Image.open("background.jpg")
    background_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(temp, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    login_log = ctk.CTkLabel(temp, text="Login:", fg_color=("white", "gray75"),
                             text_color="black", width=150)
    answer_log = ctk.CTkLabel(temp, text="Odpowiedź:", fg_color=("white", "gray75"),
                              text_color="black", width=150)

    login_field_log = ctk.CTkEntry(temp, corner_radius=0, width=150)
    answer_field_log = ctk.CTkEntry(temp, show="*", corner_radius=0, width=150)

    login_button_log = ctk.CTkButton(temp, text="Logowanie",
                                     command=lambda: answer_log_in(login_field_log.get(), "",
                                                                   answer_field_log.get()), fg_color=("#60A060"),
                                     hover_color=("#006400"), corner_radius=0, width=150)
    back_button = ctk.CTkButton(temp, text="Powrót",
                                command=lambda: main_login_window(temp), fg_color=("#60A060"),
                                hover_color=("#006400"), corner_radius=0, width=150)

    login_log.place(x=240, y=150)
    answer_log.place(x=240, y=200)

    login_field_log.place(x=410, y=150)
    answer_field_log.place(x=410, y=200)

    login_button_log.place(x=240, y=250)
    back_button.place(x=410, y=250)

    temp.mainloop()


def main_login_window(frame):
    if frame is not None:
        frame.destroy()
    root = tk.Tk()
    root.title("GreenGame")
    root.resizable(False, False)
    root.geometry("800x600+560+240")

    image = Image.open("background.jpg")
    background_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    login_log = ctk.CTkLabel(root, text="Login:", fg_color=("white", "gray75"),
                             text_color="black", width=150, corner_radius=0)
    password_log = ctk.CTkLabel(root, text="Hasło:", fg_color=("white", "gray75"),
                                text_color="black", width=150, corner_radius=0)

    login_field_log = ctk.CTkEntry(root, corner_radius=0, width=150)
    password_field_log = ctk.CTkEntry(root, show="*", corner_radius=0, width=150)

    login_button_log = ctk.CTkButton(root, text="Login",
                                     command=lambda: log_in(login_field_log.get(), password_field_log.get(),
                                                            "", root), fg_color="#60A060", hover_color="#006400",
                                     corner_radius=0, width=150)

    login_log.place(x=240, y=150)
    password_log.place(x=240, y=200)

    login_field_log.place(x=410, y=150)
    password_field_log.place(x=410, y=200)

    login_button_log.place(x=240, y=250)

    register_button = ctk.CTkButton(root, text="Zarejestruj", command=lambda: register(root), fg_color="#60A060",
                                    hover_color="#006400", corner_radius=0, width=150)

    forgot_password_button = ctk.CTkButton(root, text="Zapomniałes hasła?", command=lambda: answer_login(root),
                                           fg_color="#60A060",
                                           hover_color="#006400", corner_radius=0, width=150)

    register_button.place(x=410, y=250)

    forgot_password_button.place(x=325, y=300)

    global session
    session = SessionController()
    root.mainloop()

    # session.close()


ids = None
sorting_criteria = None


def render_events_table(screen, users, param=True):
    from database_setup import db

    def render_headers(sc, f, h, c_width, t_x=150, t_y=160, row_h=50, t_col=(0, 0, 0)):
        for index, (header, width) in enumerate(zip(h, c_width)):
            header_rect = pygame.Rect(t_x + sum(c_width[:index]), t_y, width, row_h)
            pygame.draw.rect(sc, (100, 100, 100), header_rect)
            header_text = f.render(header, True, t_col)
            t_rect = header_text.get_rect(center=header_rect.center)
            sc.blit(header_text, t_rect)

            if header in sorting_buttons:
                button_rect = pygame.Rect(t_x + sum(c_width[:index]) + width - 20, t_y + 5, 20, 20)
                pygame.draw.rect(sc, (150, 150, 150), button_rect)
                button_text = f.render("^", True, t_col) if sorting_criteria == header else f.render("v", True, t_col)
                button_text_rect = button_text.get_rect(center=button_rect.center)
                sc.blit(button_text, button_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                check_button_click(mouse_pos)

    def render_dropdown(sc, f, u):
        global ids, sorting_criteria
        user_rect = pygame.Rect(0, 120, 150, 30)
        pygame.draw.rect(sc, (255, 255, 255), user_rect)
        pygame.draw.rect(sc, (0, 0, 0), user_rect, 2)
        user_rect.y -= user_rect.height
        for el in u:
            user_rect.y += user_rect.height
            option_text = f.render(el.get('login'), True, (0, 0, 0))
            option_text_rect = option_text.get_rect(center=user_rect.center)
            sc.blit(option_text, option_text_rect)
            if user_rect.collidepoint(pygame.mouse.get_pos()):
                sorting_criteria = None
                ids = el.get('id')

    def check_button_click(x_y_mos):
        global sorting_criteria
        for index, (header, width) in enumerate(zip(headers, col_widths)):
            button_rect = pygame.Rect(table_x + sum(col_widths[:index]) + width - 20, table_y + 5, 20, 20)
            if button_rect.collidepoint(x_y_mos):
                sorting_criteria = header
                print(f"Sorting by: {sorting_criteria}")

    font = pygame.font.SysFont(None, 20)
    table_color = (200, 200, 200)
    text_color = (0, 0, 0)

    table_x = 150
    table_y = 160
    table_width = 600
    table_height = 400
    row_height = 50

    sorting_buttons = ['Wynik', 'Czas', 'Poziom']

    pygame.draw.rect(screen, table_color, (table_x, table_y, table_width, table_height))

    render_dropdown(screen, font, [{'id': user.id, 'login': user.login} for user in users])
    global ids, sorting_criteria

    if param:
        col_widths = [150, 350, 100]

        headers = ['Nazwa osiągnięcia', 'Opis', 'Liczba graczy']

        render_headers(screen, font, headers, col_widths)

        if ids is not None:
            achievements_data = {'id': ids, 'data': db.get_player_achievements(ids)}
            if len(achievements_data['data']) > 0:
                for i, achievement in enumerate(achievements_data['data']):
                    achievement = list(achievement)
                    achievement.append(db.count_achievements(achievement[0]))
                    achievement = achievement[1:]
                    for j, data_point in enumerate(achievement):
                        col_rect = pygame.Rect(table_x + sum(col_widths[:j]), table_y + (i + 1) * row_height,
                                               col_widths[j], row_height)
                        pygame.draw.rect(screen, (255, 255, 255), col_rect)
                        text = font.render(str(data_point), True, text_color)
                        text_rect = text.get_rect(center=col_rect.center)
                        screen.blit(text, text_rect)
    else:
        col_widths = [300, 100, 100, 100]

        headers = ['Nazwa eventu', 'Wynik', 'Czas', 'Poziom']

        render_headers(screen, font, headers, col_widths)

        if ids is not None:
            statistics_data = {'id': ids, 'data': db.get_player_statistics(ids, sorting_criteria)}
            if len(statistics_data['data']) > 0:
                for i, stat_entry in enumerate(statistics_data['data']):
                    stat_entry = stat_entry[2:]
                    for j, data_point in enumerate(stat_entry):
                        col_rect = pygame.Rect(table_x + sum(col_widths[:j]), table_y + (i + 1) * row_height,
                                               col_widths[j], row_height)
                        pygame.draw.rect(screen, (255, 255, 255), col_rect)
                        if j == 0:
                            text = font.render(str(db.get_event(data_point)[1]), True, text_color)
                        else:
                            text = font.render(str(data_point), True, text_color)
                        text_rect = text.get_rect(center=col_rect.center)
                        screen.blit(text, text_rect)

# Add this function wherever it fits in your code.


def render_ranking(screen, ranking_data, font, current_user, daily_ranking):
    # Define colors
    green_color = (0, 128, 0)  # Green color for the background of the leaderboard
    light_green = (144, 238, 144)  # Light green for alternating rows
    dark_green = (0, 100, 0)  # Dark green for alternating rows
    text_color = (255, 255, 255)  # White for text
    highlight_color = (255, 215, 0)  # Gold color for highlighting the current user

    # Define leaderboard size and position
    leaderboard_x = 100  # X position of the leaderboard
    leaderboard_y = 100  # Y position of the leaderboard
    leaderboard_width = 600  # Width of the leaderboard
    leaderboard_height = 50  # Height of each row in the leaderboard

    # Draw the leaderboard background
    pygame.draw.rect(screen, green_color,
                     (leaderboard_x, leaderboard_y, leaderboard_width, len(ranking_data) * leaderboard_height))

    # Loop through the ranking data and draw each row
    for index, (username, points) in enumerate(ranking_data):
        row_y = leaderboard_y + index * leaderboard_height  # Y position of the current row
        row_color = light_green if index % 2 == 0 else dark_green  # Alternating row colors

        # Draw the background for this row
        pygame.draw.rect(screen, row_color, (leaderboard_x, row_y, leaderboard_width, leaderboard_height))

        # Determine the text color
        user_text_color = highlight_color if username == current_user.login else text_color

        # Render the rank number, username, and points
        rank_text = font.render(str(index + 1), True, user_text_color)  # Render the rank number
        name_text = font.render(username, True, user_text_color)  # Render the username
        points_text = font.render(str(points), True, user_text_color)  # Render the points

        # Calculate x positions for rank, username, and points
        rank_x = leaderboard_x + 20  # 20 pixels from the left edge of the leaderboard
        name_x = leaderboard_x + 60  # 60 pixels from the left edge of the leaderboard
        points_x = leaderboard_x + leaderboard_width - 100  # 100 pixels

        # Draw the rank number, username, and points text on the screen
        screen.blit(rank_text, (rank_x, row_y + leaderboard_height / 2 - rank_text.get_height() / 2))
        screen.blit(name_text, (name_x, row_y + leaderboard_height / 2 - name_text.get_height() / 2))
        screen.blit(points_text, (points_x, row_y + leaderboard_height / 2 - points_text.get_height() / 2))

        # Draw a border around the leaderboard if desired
        border_color = (255, 255, 255)  # White color for the border
        border_rect = pygame.Rect(leaderboard_x, leaderboard_y, leaderboard_width,
                                  len(ranking_data) * leaderboard_height)
        pygame.draw.rect(screen, border_color, border_rect, 2)  # 2 is the thickness of the border


def render_button(screen, font, text, rect, is_selected):
    button_color = (100, 200, 100) if is_selected else (200, 200, 200)
    pygame.draw.rect(screen, button_color, rect)
    text_rendered = font.render(text, True, (0, 0, 0))
    text_rect = text_rendered.get_rect(center=rect.center)
    screen.blit(text_rendered, text_rect)


def ranking(current_user):
    global ranking_opened, daily_ranking, friends_ranking, statistics_opened, achievements_opened
    daily_ranking = True  # Initially shows the daily ranking
    friends_ranking = False  # Initially shows the general ranking
    statistics_opened = False
    achievements_opened = False

    if not ranking_opened:
        print("Ranking")
        ranking_opened = True

        # Definitions of buttons
        ranking_width, ranking_height = 800, 600
        ranking_screen = pygame.display.set_mode((ranking_width, ranking_height))
        pygame.display.set_caption("Ranking")

        close_button_rect = pygame.Rect(ranking_width - 30, 10, 20, 20)
        daily_button_rect = pygame.Rect(50, 10, 150, 40)
        weekly_button_rect = pygame.Rect(210, 10, 150, 40)
        general_button_rect = pygame.Rect(370, 10, 150, 40)  # Przycisk dla rankingu ogólnego
        friends_button_rect = pygame.Rect(530, 10, 150, 40)  # Przycisk dla rankingu znajomych
        statistics_button_rect = pygame.Rect(50, 60, 150, 40)  # Przycisk do statystyk
        achievements_button_rect = pygame.Rect(210, 60, 150, 40)  # Przycisk do osiagniec
        font = pygame.font.SysFont(None, 24)

        user_dao = UserDao()
        user_list = user_dao.get_all()

        current_date = datetime.now().strftime('%Y-%m-%d')
        success = user_dao.add_points(user_id=current_user.id, points=10, date=current_date, category_name='Quiz')

        while ranking_opened:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ranking_opened = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if close_button_rect.collidepoint(event.pos):
                        ranking_opened = False
                        statistics_opened = False
                        achievements_opened = False
                    elif daily_button_rect.collidepoint(event.pos):
                        daily_ranking = True
                        statistics_opened = False
                        achievements_opened = False
                    elif weekly_button_rect.collidepoint(event.pos):
                        daily_ranking = False
                        statistics_opened = False
                        achievements_opened = False
                    elif general_button_rect.collidepoint(event.pos):
                        friends_ranking = False
                        statistics_opened = False
                        achievements_opened = False
                    elif friends_button_rect.collidepoint(event.pos):
                        friends_ranking = True
                        statistics_opened = False
                        achievements_opened = False
                    elif statistics_button_rect.collidepoint(event.pos):
                        daily_ranking = False
                        friends_ranking = False
                        achievements_opened = False
                        statistics_opened = True
                    elif achievements_button_rect.collidepoint(event.pos):
                        statistics_opened = False
                        daily_ranking = False
                        friends_ranking = False
                        achievements_opened = True

            ranking_screen.fill((255, 255, 255))

            render_button(ranking_screen, font, "Ranking dzienny", daily_button_rect, daily_ranking)
            render_button(ranking_screen, font, "Ranking tygodniowy", weekly_button_rect, not daily_ranking)
            render_button(ranking_screen, font, "Ranking ogólny", general_button_rect, not friends_ranking)
            render_button(ranking_screen, font, "Ranking znajomych", friends_button_rect, friends_ranking)
            render_button(ranking_screen, font, "Statystyki", statistics_button_rect, statistics_opened)
            render_button(ranking_screen, font, "Osiągnięcia", achievements_button_rect, achievements_opened)
            pygame.draw.rect(ranking_screen, (255, 0, 0), close_button_rect)

            if friends_ranking:
                ranking_data = user_dao.get_friends_ranking_data(current_user.id,
                                                                 'daily' if daily_ranking else 'weekly')
            else:
                ranking_data = user_dao.get_ranking_data(user_list, 'daily' if daily_ranking else 'weekly')

            if not (achievements_opened or statistics_opened):  # zeby nie bylo wyrenderowanego leadboardu
                render_ranking(ranking_screen, ranking_data, font, current_user, daily_ranking)

            if statistics_opened:
                render_events_table(ranking_screen, user_list, False)
            elif achievements_opened:
                render_events_table(ranking_screen, user_list)

            pygame.display.flip()

        ranking_opened = False


def settings():
    pygame.time.delay(200)
    font = pygame.font.SysFont("Yu Gothic UI", 30, bold=True)
    global settings_opened
    print(settings_opened)

    if not settings_opened:
        print("Settings")
        settings_opened = True

        # Create a new Pygame window for settings
        settings_width, settings_height = 800, 600
        settings_screen = pygame.display.set_mode((settings_width, settings_height))
        pygame.display.set_caption("Settings")

        button_background_color = (144, 238, 144)
        dark_green = (0, 100, 0)
        light_green = (96, 160, 96)

        # Load background image
        background_image = pygame.image.load("background.jpg")
        background_image = pygame.transform.scale(background_image, (settings_width, settings_height))

        # Load logo image
        logo_image = pygame.image.load("logo.png")
        logo_image = pygame.transform.scale(logo_image, (250, 250))
        logo_rect = logo_image.get_rect(center=(settings_width // 2, settings_height // 5.5))

        # Add a close button in the settings window
        close_button_rect = pygame.Rect(settings_width - 30, 10, 20, 20)

        def play_click_sound():
            pygame.mixer.music.load("click_sound.wav")
            pygame.mixer.music.play(0)

        def create_button(text, position, command):
            font = pygame.font.SysFont("Yu Gothic UI", 30, bold=True)
            button_width, button_height = 300, 80
            text_surface = font.render(text, True, (*dark_green, 200))  # Tekst w kolorze ciemnozielonym z alfa
            button_rect = pygame.Rect(position[0] - button_width // 2, position[1] - button_height // 2, button_width,
                                      button_height)
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]

            # Rysowanie przycisku
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(settings_screen, (*light_green, 200), button_rect,
                                 border_radius=10)  # Jasnozielony przy najechaniu
                if mouse_clicked:
                    command()
            else:
                pygame.draw.rect(settings_screen, (*button_background_color, 200), button_rect,
                                 border_radius=10)  # Normalne tło

            # Rysowanie tekstu na przycisku
            text_rect = text_surface.get_rect(center=button_rect.center)
            settings_screen.blit(text_surface, text_rect)
            if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                play_click_sound()
                command()

        # Main loop for the settings window
        while settings_opened:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    settings_opened = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if close_button_rect.collidepoint(event.pos):
                        settings_opened = False
                        return  # Exit the function and return to the main menu

            # Draw the background image
            settings_screen.blit(background_image, (0, 0))

            # Draw the logo
            settings_screen.blit(logo_image, logo_rect)

            # Draw the close button
            pygame.draw.rect(settings_screen, (255, 0, 0), close_button_rect)  # Red button color

            # Call create_button with all required arguments
            create_button("Zmień hasło", (settings_width // 2, 2 * settings_height // 3 - 120), change_password_form)
            create_button("Wyloguj", (settings_width // 2, 2 * settings_height // 3 - 20), log_out)
            create_button("Usuń konto", (settings_width // 2, 2 * settings_height // 3 + 80), delete_user_form)
            pygame.display.flip()


# GRA SAMA W SOBIE

def main_game_loop():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Green Game")

    background_image = pygame.image.load("background.jpg")
    background_image = pygame.transform.scale(background_image, (width, height))

    button_background_color = (144, 238, 144)
    dark_green = (0, 100, 0)
    light_green = (96, 160, 96)

    font = pygame.font.SysFont("Yu Gothic UI", 30, bold=True)

    def play_click_sound():
        pygame.mixer.music.load("click_sound.wav")
        pygame.mixer.music.play(0)

    def create_button(text, position, command):
        button_width, button_height = 300, 80
        button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (0, 0, 0, 200), (5, 5, button_width, button_height), border_radius=10)
        rect = button_surface.get_rect(center=position)
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(button_surface, (*light_green, 200), (0, 0, button_width, button_height), border_radius=10)
        else:
            pygame.draw.rect(button_surface, (*button_background_color, 200), (0, 0, button_width, button_height),
                             border_radius=10)
        button_text = font.render(text, True, (*dark_green, 200))
        text_rect = button_text.get_rect(center=button_surface.get_rect().center)
        button_surface.blit(button_text, text_rect)
        screen.blit(button_surface, rect)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            play_click_sound()
            command()

    def start_game():
        print("hello")
        from main_board import main
        players = []
        tmp = session.user_dao.get_by_id(session.session_user.id)
        players.append({"id": tmp.id, "login": tmp.login})
        if len(example_users) != 0:
            for ids in example_users:
                tmp = session.user_dao.get_by_id(ids)
                players.append({"id": tmp.id, "login": tmp.login})
        main(players)
        # subprocess.run(["python", "main_board.py"])
        pygame.quit()

    def exit_game():
        print("Exit Game")
        pygame.quit()
        sys.exit()

    logo_image = pygame.image.load("logo.png")
    logo_image = pygame.transform.scale(logo_image, (250, 250))
    logo_rect = logo_image.get_rect(center=(width // 2, height // 5.5))

    example_users = session.user_dao.get_friend_list(session.session_user.id)
    users_list = []
    for i in example_users:
        users_list.append(session.user_dao.get_by_id(i))

    FRIENDS_BUTTON_X = 10
    FRIENDS_BUTTON_Y = 50
    toggle_button = Button(FRIENDS_BUTTON_X, FRIENDS_BUTTON_Y, 140, 50, "Znajomi")
    friend_list = FriendList(FRIENDS_BUTTON_X - 10, FRIENDS_BUTTON_Y + 50, 140, 500, users_list,
                             session.session_user.id)

    def handle_events(toggle_button, friend_list):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif toggle_button.is_clicked(event):
                friend_list.toggle_visibility()

            friend_list.handle_event(event)

    while True:
        screen.blit(background_image, (0, 0))
        screen.blit(logo_image, logo_rect)

        buttons_data = [
            {"text": "Start gry", "position": (width // 2, 2 * height // 3 - 120), "command": start_game},
            {"text": "Ranking", "position": (width // 1.23, 2 * height // 3 - 320),
             "command": lambda: ranking(session.session_user)},
            {"text": "Ustawienia", "position": (width // 2, 2 * height // 3 - 20), "command": settings},
            {"text": "Wyjdź z gry", "position": (width // 2, 2 * height // 3 + 80), "command": exit_game},
        ]

        for button_data in buttons_data:
            create_button(button_data["text"], button_data["position"], button_data["command"])

        toggle_button.draw(screen)
        friend_list.draw(screen)

        pygame.display.flip()

        handle_events(toggle_button, friend_list)


session = SessionController()
main_login_window(None)

if session.check_if_logged():
    main_game_loop()
