import pygame
from FriendList import FriendList, User

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 30)
        self.color = (100, 200, 255)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False


pygame.init()

DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 600
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

example_users = [User(f"User{i}") for i in range(5)]
friend_list = FriendList(100, 100, 200, 300, example_users)
toggle_button = Button(50, 50, 200, 50, "Toggle Friends")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if toggle_button.is_clicked(event):
            friend_list.toggle_visibility()

    screen.fill((255, 255, 255))   
    toggle_button.draw(screen)
    friend_list.draw(screen)    
    pygame.display.update()

pygame.quit()
