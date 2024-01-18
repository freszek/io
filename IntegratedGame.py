class User:
    def __init__(self, id, login, password, email, answer, question):
        self.id = id
        self.login = login
        self.password = password
        self.email = email
        self.is_logged = 0
        self.answer = answer
        self.question = question


import hashlib
import sqlite3
from typing import List
import pygame
import sys
from FriendList import FriendList, Button
import tkinter as tk
import customtkinter as ctk
from UserDao import *
import subprocess
#from gierka import show_menu_and_start_game



class UserDao:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

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
        self.conn.execute(query)
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

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def close(self):
        self.conn.close()




class SessionController:
    def __init__(self):
        self.session_user = None
        self.user_dao = UserDao()

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

    def close(self):
        self.user_dao.close()

global login_successful, session_controller, qeustions_field  # This will be used to control the flow based on login success
login_successful = False  # Default to False until login is successful
session_controller = SessionController()

def display_rules():
    # showing game rules
    app = GameRulesApp()
    app.run()

    round.round_loop()
    pygame.quit()
    quit()

def start_game_on_board():
    mglobals.init()
    display_rules()
    player_selector = PlayerAvatar(mglobals.DISPLAY_W, mglobals.DISPLAY_H, 6)
    selected_player_avatar = player_selector.choose_player()
    mglobals.P1_IMG = pygame.image.load(selected_player_avatar)
    mglobals.P2_IMG = pygame.image.load('GameMain/pics/p2.png')

    round.round_loop()

def show_login_form():
    email_string.grid_forget()
    email_field.grid_forget()
    login_string.grid_forget()
    login_field.grid_forget()
    password_string.grid_forget()
    password_field.grid_forget()
    question_string.grid_forget()
    questions_field.grid_forget()
    answer_string.grid_forget()
    answer_field.grid_forget()
    register_button.grid_forget()
    login_button.grid_forget()

    # Pokaż elementy formularza logowania
    login_form_login_string.grid(row=0, column=0)
    login_form_login_field.grid(row=0, column=1)
    login_form_password_string.grid(row=1, column=0)
    login_form_password_field.grid(row=1, column=1)
    login_form_answer_string.grid(row=2, column=0)
    login_form_answer_field.grid(row=2, column=1)
    login_form_login_button.grid(row=3, column=0)

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
            pygame.draw.rect(button_surface, (*button_background_color, 200), (0, 0, button_width, button_height), border_radius=10)
        button_text = font.render(text, True, (*dark_green, 200))
        text_rect = button_text.get_rect(center=button_surface.get_rect().center)
        button_surface.blit(button_text, text_rect)
        screen.blit(button_surface, rect)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            play_click_sound()
            command()


    def start_game():
        print("hello")
        subprocess.run(["python", "GameMain/main_board.py"])
        pygame.quit()


    def exit_game():
        print("Exit Game")
        pygame.quit()
        sys.exit()

    def settings():
        print("Settings")

    logo_image = pygame.image.load("logo.png")
    logo_image = pygame.transform.scale(logo_image, (250, 250))
    logo_rect = logo_image.get_rect(center=(width // 2, height // 5.5))
    

    example_users = session_controller.user_dao.get_friend_list(session_controller.session_user.id)
    users_list = []
    for i in example_users:
        users_list.append(session_controller.user_dao.get_by_id(i))

    FRIENDS_BUTTON_X = 10
    FRIENDS_BUTTON_Y = 50
    toggle_button = Button(FRIENDS_BUTTON_X, FRIENDS_BUTTON_Y, 140, 50, "Znajomi")
    friend_list = FriendList(FRIENDS_BUTTON_X - 10, FRIENDS_BUTTON_Y + 50, 140, 500, users_list, session_controller.session_user.id)

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
            {"text": "Ustawienia", "position": (width // 2, 2 * height // 3 - 20), "command": settings},
            {"text": "Wyjdź z gry", "position": (width // 2, 2 * height // 3 + 80), "command": exit_game},
        ]

        for button_data in buttons_data:
            create_button(button_data["text"], button_data["position"], button_data["command"])

        toggle_button.draw(screen)
        friend_list.draw(screen)

        pygame.display.flip()

        handle_events(toggle_button, friend_list)

def log_in_callback():
    # Wywołanie metody logowania
    session_controller.log_in(login_form_login_field.get(), login_form_password_field.get(), login_form_answer_field.get())

    if session_controller.check_if_logged():
        root.destroy()  # Zamknij okno Tkintera
        main_game_loop()  # Uruchom pętlę gry w Pygame

root = tk.Tk()
root.title("GreenGame")
root.resizable(False, False)

email_string = ctk.CTkLabel(root, text="Email:", fg_color=("white", "gray75"), corner_radius=8, text_color="black",
                            width=150)
login_string = ctk.CTkLabel(root, text="Login:", fg_color=("white", "gray75"), corner_radius=8, text_color="black",
                            width=150)
password_string = ctk.CTkLabel(root, text="Password:", fg_color=("white", "gray75"), corner_radius=8,
                               text_color="black", width=150)
question_string = ctk.CTkLabel(root, text="Question:", fg_color=("white", "gray75"), corner_radius=8,
                               text_color="black", width=150)
answer_string = ctk.CTkLabel(root, text="Answer:", fg_color=("white", "gray75"), corner_radius=8, text_color="black",
                             width=150)

email_field = ctk.CTkEntry(root)
login_field = ctk.CTkEntry(root)
password_field = ctk.CTkEntry(root, show="*")
questions_field = ctk.CTkComboBox(root, values=["What is your pet's name?", "Where you were born?", "Favourite book?"])
answer_field = ctk.CTkEntry(root)

login_form_login_string = ctk.CTkLabel(root, text="Login:", fg_color=("white", "gray75"), corner_radius=8, text_color="black",
                            width=150)
login_form_password_string = ctk.CTkLabel(root, text="Password:", fg_color=("white", "gray75"), corner_radius=8,
                               text_color="black", width=150)
login_form_answer_string = ctk.CTkLabel(root, text="Answer:", fg_color=("white", "gray75"), corner_radius=8, text_color="black",
                             width=150)


login_form_login_field = ctk.CTkEntry(root)
login_form_password_field = ctk.CTkEntry(root, show="*")
login_form_answer_field = ctk.CTkEntry(root)

register_button = ctk.CTkButton(root, text="Register", command=lambda: session_controller.register(login_field.get(), password_field.get(), email_field.get(), answer_field.get(), questions_field.get()), fg_color=("#60A060"), hover_color=("#006400"))
login_button = ctk.CTkButton(root, text="Already have an account? Log in", command=show_login_form, fg_color=("#60A060"), hover_color=("#006400"))

login_form_login_button = ctk.CTkButton(root, text="Log in", command=log_in_callback,fg_color=("#60A060"), hover_color=("#006400"))

email_string.grid(row=0, column=0, padx=10, pady=5, sticky="e")
login_string.grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_string.grid(row=2, column=0, padx=10, pady=5, sticky="e")
question_string.grid(row=3, column=0, padx=10, pady=5, sticky="e")
answer_string.grid(row=4, column=0, padx=10, pady=5, sticky="e")

email_field.grid(row=0, column=1, padx=10, pady=5)
login_field.grid(row=1, column=1, padx=10, pady=5)
password_field.grid(row=2, column=1, padx=10, pady=5)
questions_field.grid(row=3, column=1, padx=10, pady=5)
answer_field.grid(row=4, column=1, padx=10, pady=5)

register_button.grid(row=5, column=0, pady=10, columnspan=3)
login_button.grid(row=6, column=0, pady=10, columnspan=3)

session = SessionController()
root.mainloop()

if session_controller.check_if_logged():
    main_game_loop()

