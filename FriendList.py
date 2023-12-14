import pygame

class User:
    def __init__(self, name):
        self.name = name

class FriendList:
    def __init__(self, x, y, width, height, user_list):
        self.rect = pygame.Rect(x, y, width, height)
        self.user_list = user_list
        self.surface = pygame.Surface(self.rect.size)
        self.font = pygame.font.Font(None, 20)
        self.visible = False
    
    def draw(self, screen):
        if self.visible:
            self.surface.fill((255, 255, 255))
            for i, user in enumerate(self.user_list):
                text_surface = self.font.render(user.name, True, (0, 0, 0))
                self.surface.blit(text_surface, (10, i * 30))
            screen.blit(self.surface, self.rect.topleft)
    
    def toggle_visibility(self):
        self.visible = not self.visible
