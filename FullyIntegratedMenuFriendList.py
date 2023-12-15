import pygame
import sys

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
    print("Start Game")

def exit_game():
    print("Exit Game")
    pygame.quit()
    sys.exit()

def settings():
    print("Settings")

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

logo_image = pygame.image.load("logo.png")
logo_image = pygame.transform.scale(logo_image, (250, 250))
logo_rect = logo_image.get_rect(center=(width // 2, height // 5.5))

while True:
    screen.blit(background_image, (0, 0))
    toggle_button.draw(screen)
    friend_list.draw(screen)
    screen.blit(logo_image, logo_rect)

    buttons_data = [
        {"text": "Start gry", "position": (width // 2, 2 * height // 3 - 120), "command": start_game},
        {"text": "Ustawienia", "position": (width // 2, 2 * height // 3 - 20), "command": settings},
        {"text": "Wyjdź z gry", "position": (width // 2, 2 * height // 3 + 80), "command": exit_game},
    ]

    for button_data in buttons_data:
        create_button(button_data["text"], button_data["position"], button_data["command"])

    pygame.display.flip()
    screen.blit(background_image, (0, 0))
    screen.blit(logo_image, logo_rect)

    buttons_data = [
        {"text": "Start gry", "position": (width // 2, 2 * height // 3 - 120), "command": start_game},
        {"text": "Ustawienia", "position": (width // 2, 2 * height // 3 - 20), "command": settings},
        {"text": "Wyjdź z gry", "position": (width // 2, 2 * height // 3 + 80), "command": exit_game},
    ]

    for button_data in buttons_data:
        create_button(button_data["text"], button_data["position"], button_data["command"])

    pygame.display.flip()

    handle_events()

from FriendList import FriendList, User, Button

# Creating example users for the friend list
example_users = [User(i, f"User{i}") for i in range(12)]

# Positioning the friend list to the left side of the screen
FRIENDS_BUTTON_X = 10  # Adjusted position
FRIENDS_BUTTON_Y = 50
toggle_button = Button(FRIENDS_BUTTON_X, FRIENDS_BUTTON_Y, 140, 50, "Znajomi")
friend_list = FriendList(FRIENDS_BUTTON_X, FRIENDS_BUTTON_Y + 50, 140, 500, example_users)

# Modifying the main game loop to include friend list functionality
