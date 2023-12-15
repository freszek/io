import pygame

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
        
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont("Yu Gothic UI", 30, bold=True)
        self.color = (144, 238, 144)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 100, 0))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color(157, 193, 131)
        self.color_inactive = pygame.Color(64, 224, 208)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_inactive
        self.txt_surface = self.font.render(self.text, True, self.color)
        #self.rect.w = max(self.rect.width, self.txt_surface.get_width()+10)
        
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.text

class FriendList:
    def __init__(self, x, y, width, height, user_list):
        self.rect = pygame.Rect(x, y, width, height)
        self.user_list = user_list
        self.font = pygame.font.Font(None, 20)
        self.visible = False
        self.input_box = InputBox(x + 10, y, width, 40)

    def draw(self, screen):
        if self.visible:
            self.input_box.draw(screen)

            filtered_users = [user for user in self.user_list if self.input_box.get_text().lower() in user.name.lower()]
            for i, user in enumerate(filtered_users):
                user_y = self.rect.y + 40 + i * 30
                text_surface = self.font.render(user.name, True, (106, 168, 79))
                user_block_width = self.rect.width
                pygame.draw.rect(screen, (200, 200, 200), (self.rect.x + 10, user_y, user_block_width, 25), 1)  # Obramówka
                screen.blit(text_surface, (self.rect.x + 15, user_y + 5))


    def handle_event(self, event):
        if self.visible:
            self.input_box.handle_event(event)

    def toggle_visibility(self):
        self.visible = not self.visible
        print(self.visible)

