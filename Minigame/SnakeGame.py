import pygame
import random
import sys


class SnakeGame:
    def __init__(self):
        self.snake_speed = 7
        self.window_x = 800
        self.window_y = 600
        self.light_blue = (173, 216, 230)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.score = 0
        self.snake_position = [100, 40]
        self.snake_body = [[100, 40]
                           , [80, 40]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
        self.fps = pygame.time.Clock()
        self.fruit_spawn = True
        self.fruit_position = [random.randrange(1, (self.window_x // 20)) * 20,
                               random.randrange(1, (self.window_y // 20)) * 20]

# pygame.init()

    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)

        score_surface = score_font.render('Zebrane opony: ' + str(self.score), True, color)

        score_rect = score_surface.get_rect()

        self.game_window.blit(score_surface, score_rect)

    def game_over(self):
        my_font = pygame.font.SysFont('times new roman', 50)

        game_over_surface = my_font.render(
            'Zebrane opony: ' + str(self.score), True, self.red)

        game_over_rect = game_over_surface.get_rect()

        game_over_rect.midtop = (self.window_x / 2, self.window_y / 4)

        self.game_window.blit(game_over_surface, game_over_rect)

        super_button_rect = self.draw_super_button()

        pygame.display.flip()

        waiting_for_super = True
        while waiting_for_super:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_super_button_clicked(mouse_pos, super_button_rect):
                        waiting_for_super = False

            pygame.display.update()

        self.show_tire_disposal_concept()

        pygame.quit()
        sys.exit()


    def show_tire_disposal_concept(self):
        self.game_window.fill(self.black)

        font = pygame.font.SysFont('times new roman', 25)
        text_lines = [
            'Edukacyjny koncept dotyczący utylizacji opon:',
            'Odpowiednia utylizacja opon jest kluczowa dla ochrony środowiska.',
            'Zużyte opony powinny być przekazywane do punktów utylizacji, gdzie',
            'mogą być poddane recyklingowi lub zagospodarowane w sposób bezpieczny.'
        ]

        y_position = 40
        for line in text_lines:
            text_surface = font.render(line, True, self.white)
            text_rect = text_surface.get_rect(midtop=(self.window_x / 2, y_position))
            self.game_window.blit(text_surface, text_rect)
            y_position += text_surface.get_height() + 10

        understand_button_rect = self.draw_understand_button()

        pygame.display.flip()

        waiting_for_understand = True
        while waiting_for_understand:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_understand_button_clicked(mouse_pos, understand_button_rect):
                        waiting_for_understand = False

            pygame.display.update()

    def draw_super_button(self):
        button_rect = pygame.Rect(self.window_x // 4, self.window_y - 50, self.window_x // 2, 40)
        pygame.draw.rect(self.game_window, self.white, button_rect)
        font = pygame.font.Font(None, 28)
        button_text = font.render("Super!", True, self.black)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.game_window.blit(button_text, text_rect)

        return button_rect

    def is_super_button_clicked(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def draw_understand_button(self):
        button_rect = pygame.Rect(self.window_x // 4, self.window_y - 50, self.window_x // 2, 40)
        pygame.draw.rect(self.game_window, self.white, button_rect)
        font = pygame.font.Font(None, 28)
        button_text = font.render("Rozumiem", True, self.black)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.game_window.blit(button_text, text_rect)

        return button_rect

    def is_understand_button_clicked(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def run(self):
        rules_text = [
            "Zasady poruszania się węża:",
            "Ruch w górę: W lub strzałka w górę",
            "Ruch w dół: S lub strzałka w dół",
            "Ruch w lewo: A lub strzałka w lewo",
            "Ruch w prawo: D lub strzałka w prawo",
            "",
            "Warunki zakończenia gry:",
            "- Zderzenie się węża z samym sobą",
            "- Zderzenie się z krawędzią planszy",
            "- Wypełnienie całej planszy zebranie wszystkich opon"
        ]

        font = pygame.font.SysFont('times new roman', 20)
        y_position = 50
        for line in rules_text:
            text_surface = font.render(line, True, self.white)
            text_rect = text_surface.get_rect(midtop=(self.window_x / 2, y_position))
            self.game_window.blit(text_surface, text_rect)
            y_position += 30

        understand_button_rect = self.draw_understand_button()

        waiting_for_understand = True
        while waiting_for_understand:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_understand_button_clicked(mouse_pos, understand_button_rect):
                        waiting_for_understand = False

            pygame.display.update()

        pygame.time.wait(1000)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.change_to = 'UP'
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.change_to = 'RIGHT'

            if self.change_to == 'UP' and not self.direction == 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and not self.direction == 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and not self.direction == 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and not self.direction == 'LEFT':
                self.direction = 'RIGHT'

            # Update the position of the head based on the direction
            if self.direction == 'UP':
                self.snake_position[1] -= 20
            if self.direction == 'DOWN':
                self.snake_position[1] += 20
            if self.direction == 'LEFT':
                self.snake_position[0] -= 20
            if self.direction == 'RIGHT':
                self.snake_position[0] += 20

            # Check if the head collides with the fruit
            if (
                    self.fruit_position[0] == self.snake_position[0] and
                    self.fruit_position[1] == self.snake_position[1]
            ):
                self.score += 1
                self.fruit_spawn = False
            else:
                if len(self.snake_body) > 1:
                    self.snake_body.pop()
                else:
                    self.game_over()

            # Spawn a new fruit if the previous one was eaten
            if not self.fruit_spawn:
                self.fruit_position = [
                    random.randrange(1, (self.window_x // 20)) * 20,
                    random.randrange(1, (self.window_y // 20)) * 20
                ]

            self.fruit_spawn = True
            self.game_window.fill(self.light_blue)

            # Draw the snake body
            for pos in self.snake_body:
                pygame.draw.rect(self.game_window, self.white, pygame.Rect(pos[0], pos[1], 20, 20))
            pygame.draw.rect(self.game_window, self.black, pygame.Rect(
                self.fruit_position[0], self.fruit_position[1], 20, 20))

            # Check for collisions with the window borders
            if self.snake_position[0] < 0 or self.snake_position[0] >= self.window_x:
                self.game_over()
            if self.snake_position[1] < 0 or self.snake_position[1] >= self.window_y:
                self.game_over()

            # Check for collisions with the snake body
            for block in self.snake_body:
                if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                    self.game_over()

            # Update the snake body with the new head position
            self.snake_body.insert(0, list(self.snake_position))

            self.show_score(1, self.white, 'times new roman', 20)

            pygame.display.update()

            self.fps.tick(self.snake_speed)