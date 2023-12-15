
import pygame
import sys
from FriendList import FriendList, User, Button

# Initialization and screen setup from Menu.py
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Green Game")

# Loading background image and other assets from Menu.py
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (width, height))

# Defining colors, font, and other elements from Menu.py
# ...

# Sound function from Menu.py
def play_click_sound():
    pygame.mixer.music.load("click_sound.mp3")
    pygame.mixer.music.play()

# Creating example users for the friend list
example_users = [User(i, f"User{i}") for i in range(12)]

# Creating a button to toggle the friend list visibility
FRIENDS_BUTTON_X = 10  # Adjusted position
FRIENDS_BUTTON_Y = 50
toggle_button = Button(FRIENDS_BUTTON_X, FRIENDS_BUTTON_Y, 140, 50, "Znajomi")

# Creating the friend list
friend_list = FriendList(FRIENDS_BUTTON_X, FRIENDS_BUTTON_Y + 50, 140, 500, example_users)

# Modifying the main game loop from Menu.py to include friend list functionality
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif toggle_button.is_clicked(event):
            friend_list.toggle_visibility()
        friend_list.handle_event(event)

    screen.blit(background_image, (0, 0))
    
    # Drawing existing menu elements from Menu.py
    # ...

    toggle_button.draw(screen)
    friend_list.draw(screen)

    pygame.display.flip()

pygame.quit()
