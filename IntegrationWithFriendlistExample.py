import pygame
from FriendList import FriendList, User, Button

pygame.init()

DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 600
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

example_users = [User(f"User{i}") for i in range(12)]

FRIENDS_BUTTON_X = 250
FRIENDS_BUTTON_Y = 50

toggle_button = Button(FRIENDS_BUTTON_X, FRIENDS_BUTTON_Y, 140, 50, "Znajomi")

friend_list = FriendList(FRIENDS_BUTTON_X - 10, FRIENDS_BUTTON_Y + 50, 140, 500, example_users)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif toggle_button.is_clicked(event):
            friend_list.toggle_visibility()
        
        friend_list.handle_event(event)

    screen.fill((255, 255, 255))
    
    toggle_button.draw(screen)

    friend_list.draw(screen)
    
    pygame.display.update()

pygame.quit()
