from datetime import datetime
from GameMain import game_rules
from GameMain.BoardDao import BoardDao
from Userr import Userr as User
from UserDao import UserDao
import pygame
import sys
from FriendList import FriendList, Button
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess


# DEFINICJE KLAS ITP
class SessionController:
    def __init__(self):
        self.session_user = None
        self.user_dao = UserDao()
        self.board_dao = BoardDao()
        self.counter = 0

    def register(self, login, password, email, answer, question):
        if self.check_login(login):
            print("Uzytkownik o tym loginie juz istnieje!")
            return

        user = User(0, login, password, email, question, answer)
        self.session_user = user
        self.user_dao.create_user(user)
        self.create_board_table_in_DB()
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
                print(self.session_user.id)
                return True
        print("Niezalogowany")
        return False

    def create_board_table_in_DB(self) -> bool:
        self.board_dao.add_board_entry(
                user_login=self.session_user.login,
                board_position=0,
                avatar_img=None
            )

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


def display_rules():
    # showing game rules
    app = game_rules.GameRulesApp()
    app.run()

    round.round_loop()
    pygame.quit()
    quit()

# def start_game_on_board():
#     mglobals.init()
#     display_rules()
#     player_selector = player.PlayerAvatar(mglobals.DISPLAY_W, mglobals.DISPLAY_H, 6)
#     selected_player_avatar = player_selector.choose_player()
#     mglobals.P1_IMG = pygame.image.load(selected_player_avatar)
#     mglobals.P2_IMG = pygame.image.load('GameMain/pics/p2.png')
#
#     round.round_loop()

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
                                 text_color="black", width=150,corner_radius=0)
    label_password.place(x=240,y=150)
    entry_password = ctk.CTkEntry(root,corner_radius=0,width=150,show="*")
    entry_password.place(x=410,y=150)
    
    label_new_password = ctk.CTkLabel(root, text="Nowe hasło:", fg_color=("white", "gray75"),
                                 text_color="black", width=150,corner_radius=0)
    label_new_password.place(x=240,y=200)
    entry_new_password = ctk.CTkEntry(root, show="*", corner_radius=0,width=150)
    entry_new_password.place(x=410,y=200)
    
    confirm_button = ctk.CTkButton(root, text="Zmień hasło", command=lambda:confirm_change_password(root), corner_radius=0,fg_color=("#60A060"),
                                     hover_color=("#006400"),)
    confirm_button.place(x=325,y=250)
    
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
    
    label_password = ctk.CTkLabel(root, text="Hasło:", corner_radius=0, width=150,fg_color=("white", "gray75"), text_color="black")
    label_password.place(x=240,y=200)
    entry_password = ctk.CTkEntry(root, show="*", corner_radius=0, width=150)
    entry_password.place(x=410,y=200)
    
    confirm_button = ctk.CTkButton(root, text="Usuń użytkownika", command=lambda: confirm_delete_user(root), corner_radius=0, width=150,fg_color=("#60A060"),
                                     hover_color=("#006400"))
    confirm_button.place(x=325,y=250)
    
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

    email_field = ctk.CTkEntry(temp,corner_radius=0,width=150)
    login_field = ctk.CTkEntry(temp,corner_radius=0,width=150)
    password_field = ctk.CTkEntry(temp, show="*",corner_radius=0,width=150)
    questions_field = ctk.CTkComboBox(temp,
                                      values=["Ulubione zwierze?", "Gdzie się urodziłes?", "Ulubiona Książka?"],corner_radius=0,width=150)
    answer_field = ctk.CTkEntry(temp,corner_radius=0,width=150)

    register_button = ctk.CTkButton(temp, text="Zarejestruj", command=lambda: register_in(email_field.get(), login_field.get(),
                                                        password_field.get(), answer_field.get(), questions_field.get()), fg_color=("#60A060"),
                                    hover_color=("#006400"),corner_radius=0,width=150)
    back_button = ctk.CTkButton(temp, text="Powrót",
                                    command=lambda: main_login_window(temp), fg_color=("#60A060"),
                                    hover_color=("#006400"), corner_radius=0,width=150)

    email_string.place(x=240,y=50)
    login_string.place(x=240,y=100)
    password_string.place(x=240,y=150)
    question_string.place(x=240,y=200)
    answer_string.place(x=240,y=250)

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

    login_field_log = ctk.CTkEntry(temp,corner_radius=0, width=150)
    answer_field_log = ctk.CTkEntry(temp, show="*",corner_radius=0, width=150)

    login_button_log = ctk.CTkButton(temp, text="Logowanie",
                                     command=lambda: answer_log_in(login_field_log.get(), "",
                                                            answer_field_log.get()), fg_color=("#60A060"), hover_color=("#006400"),corner_radius=0, width=150)
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
                             text_color="black", width=150,corner_radius=0)
    password_log = ctk.CTkLabel(root, text="Hasło:", fg_color=("white", "gray75"),
                                text_color="black", width=150,corner_radius=0)

    login_field_log = ctk.CTkEntry(root,corner_radius=0,width=150)
    password_field_log = ctk.CTkEntry(root, show="*",corner_radius=0,width=150)

    login_button_log = ctk.CTkButton(root, text="Login",
                                     command=lambda: log_in(login_field_log.get(), password_field_log.get(),
                                                            "", root),fg_color=("#60A060"), hover_color=("#006400"),corner_radius=0,width=150)

    login_log.place(x=240, y=150)
    password_log.place(x=240, y=200)

    login_field_log.place(x=410, y=150)
    password_field_log.place(x=410, y=200)

    login_button_log.place(x=240, y=250)

    register_button = ctk.CTkButton(root, text="Zarejestruj", command=lambda: register(root), fg_color=("#60A060"),
                                 hover_color=("#006400"),corner_radius=0,width=150)

    forgot_password_button = ctk.CTkButton(root, text="Zapomniałes hasła?", command=lambda: answer_login(root), fg_color=("#60A060"),
                                 hover_color=("#006400"),corner_radius=0,width=150)

    register_button.place(x=410, y=250)

    forgot_password_button.place(x=325, y=300)

    global session
    session = SessionController()
    root.mainloop()

    #session.close()

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
    pygame.draw.rect(screen, green_color, (leaderboard_x, leaderboard_y, leaderboard_width, len(ranking_data) * leaderboard_height))

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
        border_rect = pygame.Rect(leaderboard_x, leaderboard_y, leaderboard_width, len(ranking_data) * leaderboard_height)
        pygame.draw.rect(screen, border_color, border_rect, 2)  # 2 is the thickness of the border



def render_button(screen, font, text, rect, is_selected):
    button_color = (100, 200, 100) if is_selected else (200, 200, 200)
    pygame.draw.rect(screen, button_color, rect)
    text_rendered = font.render(text, True, (0, 0, 0))
    text_rect = text_rendered.get_rect(center=rect.center)
    screen.blit(text_rendered, text_rect)


def ranking(current_user):
    global ranking_opened, daily_ranking, friends_ranking
    daily_ranking = True  # Początkowo pokazuje ranking dzienny
    friends_ranking = False  # Początkowo pokazuje ranking ogólny

    if not ranking_opened:
        print("Ranking")
        ranking_opened = True

        # Definicje przycisków
        ranking_width, ranking_height = 800, 600
        ranking_screen = pygame.display.set_mode((ranking_width, ranking_height))
        pygame.display.set_caption("Ranking")

        close_button_rect = pygame.Rect(ranking_width - 30, 10, 20, 20)
        daily_button_rect = pygame.Rect(50, 10, 150, 40)
        weekly_button_rect = pygame.Rect(210, 10, 150, 40)
        general_button_rect = pygame.Rect(370, 10, 150, 40)  # Przycisk dla rankingu ogólnego
        friends_button_rect = pygame.Rect(530, 10, 150, 40)  # Przycisk dla rankingu znajomych
        font = pygame.font.SysFont(None, 24)

        user_dao = UserDao()
        user_list = user_dao.get_all()
        #
        # current_date = datetime.now().strftime('%Y-%m-%d')
        # # Wywołanie metody add_points z aktualną datą
        # success = user_dao.add_points(user_id=current_user.id, points=0, date=current_date, category_name='Quiz')


        while ranking_opened:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ranking_opened = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if close_button_rect.collidepoint(event.pos):
                        ranking_opened = False
                    elif daily_button_rect.collidepoint(event.pos):
                        daily_ranking = True
                    elif weekly_button_rect.collidepoint(event.pos):
                        daily_ranking = False
                    elif general_button_rect.collidepoint(event.pos):
                        friends_ranking = False
                    elif friends_button_rect.collidepoint(event.pos):
                        friends_ranking = True

            ranking_screen.fill((255, 255, 255))  # Biały tło

            # Rysowanie przycisków
            render_button(ranking_screen, font, "Ranking dzienny", daily_button_rect, daily_ranking)
            render_button(ranking_screen, font, "Ranking tygodniowy", weekly_button_rect, not daily_ranking)
            render_button(ranking_screen, font, "Ranking ogólny", general_button_rect, not friends_ranking)
            render_button(ranking_screen, font, "Ranking znajomych", friends_button_rect, friends_ranking)
            pygame.draw.rect(ranking_screen, (255, 0, 0), close_button_rect)  # Red button color

            # Pobieranie i renderowanie danych rankingu
            if friends_ranking:
                ranking_data = user_dao.get_friends_ranking_data(current_user.id, 'daily' if daily_ranking else 'weekly')
            else:
                ranking_data = user_dao.get_ranking_data(user_list, 'daily' if daily_ranking else 'weekly')
            render_ranking(ranking_screen, ranking_data, font, current_user, daily_ranking)

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
            button_rect = pygame.Rect(position[0] - button_width // 2, position[1] - button_height // 2, button_width, button_height)
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]

            # Rysowanie przycisku
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(settings_screen, (*light_green, 200), button_rect, border_radius=10)  # Jasnozielony przy najechaniu
                if mouse_clicked:
                    command()
            else:
                pygame.draw.rect(settings_screen, (*button_background_color, 200), button_rect, border_radius=10)  # Normalne tło

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
            pygame.draw.rect(button_surface, (*button_background_color, 200), (0, 0, button_width, button_height), border_radius=10)
        button_text = font.render(text, True, (*dark_green, 200))
        text_rect = button_text.get_rect(center=button_surface.get_rect().center)
        button_surface.blit(button_text, text_rect)
        screen.blit(button_surface, rect)
        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            play_click_sound()
            command()


    def start_game():
        subprocess.run(["python", "GameMain/main_board.py", str(session.session_user.login), str(session.session_user.id)])
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
    friend_list = FriendList(FRIENDS_BUTTON_X - 10, FRIENDS_BUTTON_Y + 50, 140, 500, users_list, session.session_user.id)

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
            {"text": "Ranking", "position": (width // 1.23, 2 * height // 3 - 320), "command": lambda: ranking(session.session_user)},
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