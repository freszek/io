import pygame
import sys
import random
import os

class Container(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.CONTAINER_WIDTH = 100
        self.CONTAINER_HEIGHT = 100
        self.image = self.load_container_image(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_container_image(self, color):
        image_path = os.path.join("Minigames/SortTrash/pics_game", f"container_{color[0]}_{color[1]}_{color[2]}.png")
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.scale(image, (self.CONTAINER_WIDTH, self.CONTAINER_HEIGHT))

class Trash(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.TRASH_WIDTH = 30
        self.TRASH_HEIGHT = 30
        self.image = pygame.Surface((self.TRASH_WIDTH, self.TRASH_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False

class Game:
    def __init__(self, width=1200, height=800, duration=30):
        pygame.init()
        self.WIDTH = width
        self.HEIGHT = height
        self.FPS = 60
        self.WHITE = (255, 255, 255)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sortowanie śmieci")

        self.CONTAINER_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 150, 0), (255, 0, 150)]
        self.TRASH_COLORS = [(255, 0, 0), (50, 117, 38), (89, 111, 187), (246, 139, 25), (248, 201, 25)]
        self.CONTAINER_WIDTH = 100
        self.CONTAINER_HEIGHT = 100
        self.TRASH_WIDTH = 30
        self.TRASH_HEIGHT = 30

        self.containers_group = pygame.sprite.Group()
        self.trash_group = pygame.sprite.Group()

        self.max_score = 300
        self.start_time = 0
        self.elapsed_time = 0
        self.game_running = True
        self.end_time = 0
        self.game_completed = False
        self.normalized_score = 0

    def generate_game(self):
        self.containers_group.empty()
        self.trash_group.empty()

        for i in range(5):
            container = Container(self.CONTAINER_COLORS[i], i * (self.WIDTH // 5), self.HEIGHT - self.CONTAINER_HEIGHT)
            self.containers_group.add(container)

        for i in range(3):
            for color in self.TRASH_COLORS:
                trash = Trash(color, random.randint(0, self.WIDTH - self.TRASH_WIDTH),
                              random.randint(0, self.HEIGHT - self.CONTAINER_HEIGHT - self.TRASH_HEIGHT - 5))
                self.trash_group.add(trash)

    def show_menu(self):
        WIDTH, HEIGHT = self.WIDTH, self.HEIGHT
        FPS = self.FPS
        WHITE = self.WHITE

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Menu")

        font = pygame.font.SysFont("Yu Gothic UI", 28, bold=True)

        rules_text = font.render("Zasady minigry:", True, (0, 0, 0))
        rules_text2 = font.render("Przeciągnij śmieci do odpowiadających im kontenerów", True, (0, 0, 0))
        rules_text3 = font.render("w jak najkrótszym czasie!", True, (0, 0, 0))
        start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 1 - 150, 200, 50)
        logo_image = pygame.image.load("logo.png")
        logo_image = pygame.transform.scale(logo_image, (250, 250))
        logo_rect = logo_image.get_rect(center=(WIDTH // 2, HEIGHT // 4.5))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and start_button.collidepoint(event.pos):
                        return True

            screen.fill(WHITE)

            pygame.draw.rect(screen, (144, 238, 144), start_button.inflate(-10, -10),
                             border_radius=10)

            rules_text_rect = rules_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))

            screen.blit(logo_image, logo_rect)
            screen.blit(rules_text, rules_text_rect)
            screen.blit(rules_text2, (WIDTH // 2 - 380, HEIGHT // 1.75 - 20))

            rules_text3_rect = rules_text3.get_rect(center=(WIDTH // 2, HEIGHT // 1.75 + 20))
            screen.blit(rules_text3, rules_text3_rect)
            start_text = font.render("Start", True, (0, 0, 0))

            start_text_rect = start_text.get_rect(center=start_button.center)
            screen.blit(start_text, start_text_rect)

            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

    def show_menu_and_start_game(self):
        if not self.show_menu():
            pygame.quit()
            sys.exit()

        self.generate_game()

    def run_game(self):
        self.show_menu_and_start_game()
        while self.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for trash in self.trash_group:
                        if trash.rect.collidepoint(event.pos):
                            trash.dragging = True
                            trash.offset_x = event.pos[0] - trash.rect.x
                            trash.offset_y = event.pos[1] - trash.rect.y
                elif event.type == pygame.MOUSEBUTTONUP:
                    for trash in self.trash_group:
                        if trash.dragging:
                            trash.dragging = False
                            container_hit = pygame.sprite.spritecollideany(trash, self.containers_group)
                            if container_hit is not None:
                                if self.containers_group.sprites().index(container_hit) == 0:
                                    container_color = (255, 0, 0)
                                else:
                                    container_color = container_hit.image.get_at(
                                        (container_hit.image.get_width() // 2, container_hit.image.get_height() // 2))[:-1]

                                trash_color = trash.image.get_at(
                                    (trash.image.get_width() // 2, trash.image.get_height() // 2))[:-1]

                                if trash_color == container_color:
                                    self.trash_group.remove(trash)
                                    if not self.trash_group:
                                        self.end_time = pygame.time.get_ticks() - self.start_time
                                        self.game_completed = True

            for trash in self.trash_group:
                if trash.dragging:
                    trash.rect.x = pygame.mouse.get_pos()[0] - trash.offset_x
                    trash.rect.y = pygame.mouse.get_pos()[1] - trash.offset_y

            self.screen.fill(self.WHITE)
            self.containers_group.draw(self.screen)
            self.trash_group.draw(self.screen)

            if not self.trash_group and self.game_running and self.game_completed:
                self.normalized_score = max(0, self.max_score - (self.end_time * 10 // 1000))

                congratulations_text = pygame.font.Font(None, 36).render(
                    f"Gratulacje! Twój czas to: {self.end_time // 1000} s", True, (0, 0, 0))
                congratulations_rect = congratulations_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 60))
                self.screen.blit(congratulations_text, congratulations_rect.topleft)

                score_text = pygame.font.Font(None, 36).render(f"Twój wynik: {self.normalized_score} pkt", True, (0, 0, 0))
                score_rect = score_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 20))
                self.screen.blit(score_text, score_rect.topleft)

            pygame.display.flip()
            pygame.time.Clock().tick(self.FPS)
            self.screen.fill(self.WHITE)
        return self.normalized_score