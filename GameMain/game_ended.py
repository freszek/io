import pygame
import sys

from BoardDao import BoardDao
from GameMain.RoundDao import RoundDao
from User.UserDao import UserDao


pygame.init()

class GameEndedChecker:
    def __init__(self):
        self.game_ended = False
        self.thank_you_menu_shown = False

    def check_game_ended(self, current_round_number):
        if current_round_number >= 14:
            self.game_ended = True

    def has_game_ended(self):
        return self.game_ended


    def thank_you_menu(self, leader):
        width, height = 800, 600
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Green Game - Thank You!")

        background_color = (144, 238, 144)
        dark_green = (0, 100, 0)
        light_green = (96, 160, 96)

        font = pygame.font.SysFont("Yu Gothic UI", 20, bold=True)

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
                pygame.draw.rect(button_surface, (*background_color, 200), (0, 0, button_width, button_height),
                                 border_radius=10)
            button_text = font.render(text, True, (*dark_green, 200))
            text_rect = button_text.get_rect(center=button_surface.get_rect().center)
            button_surface.blit(button_text, text_rect)
            screen.blit(button_surface, rect)
            if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                play_click_sound()
                command()

        def finish_game():
            dao = BoardDao()
            round_dao = RoundDao()
            user_dao = UserDao()
            dao.prepare_database()
            round_dao.prepare_database()
            user_dao.prepare_database()
            pygame.quit()
            sys.exit()

        def show_game_statistics():
            pass

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(background_color)

            font_caption = pygame.font.SysFont("Yu Gothic UI", 72, bold=True)  # Set the font size for the caption
            game_ended_caption = font_caption.render("Game Ended", True, (*dark_green, 200))
            game_ended_caption2 = font_caption.render(f"Winner: {leader}", True, (*dark_green, 200))
            game_ended_rect2 = game_ended_caption2.get_rect(center=(width // 2, height // 2))
            game_ended_rect = game_ended_caption.get_rect(center=(width // 2, height // 3))
            screen.blit(game_ended_caption, game_ended_rect)
            screen.blit(game_ended_caption2, game_ended_rect2)

            buttons_data = [
                {"text": "Finish", "position": (width // 2, 2 * height // 3 - 20), "command": finish_game},
            ]

            for button_data in buttons_data:
                create_button(button_data["text"], button_data["position"], button_data["command"])

            pygame.display.flip()