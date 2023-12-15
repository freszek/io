
import pygame
import sys

# Initialization and screen setup
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Green Game")

# Loading background image and other assets
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (width, height))

# Defining colors and font
button_background_color = (144, 238, 144)
dark_green = (0, 100, 0)
light_green = (96, 160, 96)
font = pygame.font.SysFont("Yu Gothic UI", 30, bold=True)

# Sound function
def play_click_sound():
    pygame.mixer.music.load("click_sound.mp3")
    pygame.mixer.music.play()

from FriendList import FriendList, User, Button

# Creating example users for the friend list
example_users = [User(i, f"User{i}") for i in range(12)]

# Creating a button to toggle the friend list visibility
FRIENDS_BUTTON_X = 250
FRIENDS_BUTTON_Y = 50
toggle_button = Button(FRIENDS_BUTTON_X, FRIENDS_BUTTON_Y, 140, 50, "Znajomi")

# Creating the friend list
friend_list = FriendList(FRIENDS_BUTTON_X - 10, FRIENDS_BUTTON_Y + 50, 140, 500, example_users)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif toggle_button.is_clicked(event):
            friend_list.toggle_visibility()
        friend_list.handle_event(event)

    screen.blit(background_image, (0, 0))
    toggle_button.draw(screen)
    friend_list.draw(screen)

    pygame.display.update()

pygame.quit()
