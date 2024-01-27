import pygame

from User.UserDao import UserDao


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
        self.color = pygame.Color(0, 100, 0)
        self.color_active = pygame.Color(0, 100, 0)
        self.color_inactive = pygame.Color(144, 238, 144)
        self.text = text
        self.font = pygame.font.Font(None, 36)
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

        # Renderowanie tekstu
        self.txt_surface = self.font.render(self.text, True, self.color)
        text_width, text_height = self.txt_surface.get_size()

        # Ustawienie obszaru widoczności tekstu
        text_x = self.rect.x + 5
        clip_rect = self.rect.copy()
        clip_rect.width -= 5  # Odstęp z obu stron

        # Przesunięcie tekstu, jeśli jest zbyt długi
        if text_width > clip_rect.width:
            text_x -= (text_width - clip_rect.width)

        # Rysowanie tekstu z uwzględnieniem obszaru widoczności
        screen.set_clip(clip_rect)  # Ustawienie obszaru, w którym można rysować
        screen.blit(self.txt_surface, (text_x, self.rect.y + 5))
        screen.set_clip(None)  # Usunięcie ograniczenia obszaru rysowania

        # Rysowanie ramki
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.text


class FriendList:
    def __init__(self, x, y, width, height, user_list, user_id):
        self.rect = pygame.Rect(x, y, width, height)
        self.user_list = user_list
        self.font = pygame.font.Font(None, 20)
        self.visible = False
        self.input_box = InputBox(x + 10, y, width, 40)
        self.user_id = user_id
        self.user_dao = UserDao()
        self.add_friend_rect = pygame.Rect(100, 100, 50, 50)

    def draw_plus_icon(self, screen, x, y, size=20):
        # Rysowanie plusa
        plus_rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(screen, (0, 255, 0), plus_rect)  # Zielony kwadrat
        pygame.draw.line(screen, (255, 255, 255), (plus_rect.centerx, plus_rect.top + 5),
                         (plus_rect.centerx, plus_rect.bottom - 5), 2)  # Biały pionowy plus
        pygame.draw.line(screen, (255, 255, 255), (plus_rect.left + 5, plus_rect.centery),
                         (plus_rect.right - 5, plus_rect.centery), 2)  # Biały poziomy plus
        return plus_rect  # Zwróć prostokąt plusa, aby można było użyć go w obsłudze zdarzeń

    def draw(self, screen):
        if self.visible:
            self.input_box.draw(screen)
            # Rysowanie plusa obok InputBox
            self.add_friend_rect = self.draw_plus_icon(screen, self.input_box.rect.right + 5,
                                                       self.input_box.rect.y + 10)

            filtered_users = [user for user in self.user_list if
                              self.input_box.get_text().lower() in user.login.lower()]
            for i, user in enumerate(filtered_users):
                user_y = self.rect.y + 40 + i * 30
                user_block_width = self.rect.width

                # Zmieniono kolor tła i czcionki na taki sam jak w Button
                pygame.draw.rect(screen, (144, 238, 144),
                                 (self.rect.x + 10, user_y, user_block_width, 25))  # Tło kafelka
                text_surface = self.font.render(user.login, True, (0, 100, 0))  # Kolor czcionki
                screen.blit(text_surface, (self.rect.x + 15, user_y + 5))

                # Rysowanie ikony minusa
                minus_rect = pygame.Rect(self.rect.x + user_block_width + 15, user_y, 20, 20)
                pygame.draw.rect(screen, (255, 0, 0), minus_rect)  # Czerwony kwadrat
                pygame.draw.line(screen, (255, 255, 255), (minus_rect.left + 5, minus_rect.centery),
                                 (minus_rect.right - 5, minus_rect.centery), 2)  # Biały minus

                pygame.draw.rect(screen, (0, 255, 0), self.add_friend_rect)  # Zielony kwadrat
                pygame.draw.line(screen, (255, 255, 255), (self.add_friend_rect.centerx, self.add_friend_rect.top + 5),
                                 (self.add_friend_rect.centerx, self.add_friend_rect.bottom - 5),
                                 2)  # Biały pionowy plus
                pygame.draw.line(screen, (255, 255, 255), (self.add_friend_rect.left + 5, self.add_friend_rect.centery),
                                 (self.add_friend_rect.right - 5, self.add_friend_rect.centery),
                                 2)  # Biały poziomy plus

                # Dodaj atrybut `minus_rect` do użytkownika, aby można było go zidentyfikować później
                user.minus_rect = minus_rect

    def handle_event(self, event):
        if self.visible:
            self.input_box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for user in self.user_list:
                    if hasattr(user, 'minus_rect') and user.minus_rect.collidepoint(event.pos):
                        self.user_dao.delete_friend(self.user_id,
                                                    user.id)
                        # Zakładając, że `user_id` to ID aktualnego użytkownika, a `user.id` to ID znajomego
                        self.user_list.remove(user)  # Usuwa użytkownika z listy
                        break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.add_friend_rect.collidepoint(event.pos):
                    # Tutaj logika dodawania nowego znajomego
                    new_friend_username = self.input_box.get_text()
                    if new_friend_username and not any(user.login == new_friend_username for user in self.user_list):
                        # Zakładając, że masz dostęp do user_id aktualnego użytkownika i
                        # możesz uzyskać ID nowego znajomego na podstawie jego nazwy
                        new_friend = self.user_dao.get_by_login(new_friend_username)
                        if new_friend and new_friend.id != self.user_id:
                            self.user_dao.add_friend(self.user_id, new_friend.id)
                            self.user_list.append(new_friend)

    def toggle_visibility(self):
        self.visible = not self.visible
        print(self.visible)
