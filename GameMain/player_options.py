import pygame
import subprocess
import sys
from GameMain.main_board import display_rules
from Player.player_avatar import PlayerAvatar
from BoardDao import BoardDao
import mglobals

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


def play_game():
    subprocess.run(["python", "GameMain/main_board.py", str(sys.argv[1]), str(sys.argv[2])])
    pygame.quit()
    sys.exit()


def character_selection():
    dao = BoardDao()
    player_selector = PlayerAvatar(mglobals.DISPLAY_W, mglobals.DISPLAY_H, 6)
    selected_player_avatar = player_selector.choose_player()
    dao.update_avatar_image(str(sys.argv[1]), selected_player_avatar)
    print(selected_player_avatar)
    pygame.display.flip()


def game_rules():
    display_rules()
    pygame.quit()


logo_image = pygame.image.load("logo.png")
logo_image = pygame.transform.scale(logo_image, (250, 250))
logo_rect = logo_image.get_rect(center=(width // 2, height // 5.5))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background_image, (0, 0))
    screen.blit(logo_image, logo_rect)

    buttons_data = [
        {"text": "Graj", "position": (width // 2, 2 * height // 3 - 120), "command": play_game},
        {"text": "Wybór postaci", "position": (width // 2, 2 * height // 3 - 20), "command": character_selection},
        {"text": "Zasady rozgrywki", "position": (width // 2, 2 * height // 3 + 80), "command": game_rules},
    ]

    for button_data in buttons_data:
        create_button(button_data["text"], button_data["position"], button_data["command"])

    pygame.display.flip()
