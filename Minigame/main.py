from Minigame.SnakeGame import SnakeGame

import pygame
import random
import sys

class Tire:
    def __init__(self, game):
        self.game = game
        self.position = [random.randrange(1, (self.game.window_x // 20)) * 20,
                         random.randrange(1, (self.game.window_y // 20)) * 20]


class Scene:
    def __init__(self, game):
        self.game = game
        self.game.green2 = (31, 173, 135)

    def show_welcome_screen(self):
        self.game.game_window.fill(self.game.green2)

        font = pygame.font.SysFont('times new roman', 36)
        title_surface = font.render("WITAJ W GRZE GREENSNAKE", True, self.game.white)
        title_rect = title_surface.get_rect(center=(self.game.window_x / 2, self.game.window_y / 4))
        self.game.game_window.blit(title_surface, title_rect)

        play_button_rect = self.draw_play_button()
        how_to_play_button_rect = self.draw_how_to_play_button()

        pygame.display.flip()

        waiting_for_choice = True
        while waiting_for_choice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_play_button_clicked(mouse_pos, play_button_rect):
                        self.game.choose_level()
                    elif self.is_how_to_play_button_clicked(mouse_pos, how_to_play_button_rect):
                        self.show_rules()

            pygame.display.update()

    def draw_how_to_play_button(self):
        button_rect = pygame.Rect(self.game.window_x // 4, self.game.window_y / 2 + 50, self.game.window_x // 2, 40)
        pygame.draw.rect(self.game.game_window, self.game.white, button_rect)
        font = pygame.font.Font(None, 28)
        button_text = font.render("JAK GRAĆ?", True, self.game.black)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.game.game_window.blit(button_text, text_rect)

        return button_rect

    def is_how_to_play_button_clicked(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def draw_play_button(self):
        button_rect = pygame.Rect(self.game.window_x // 4, self.game.window_y / 2, self.game.window_x // 2, 40)
        pygame.draw.rect(self.game.game_window, self.game.white, button_rect)
        font = pygame.font.Font(None, 28)
        button_text = font.render("GRAJ", True, self.game.black)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.game.game_window.blit(button_text, text_rect)

        return button_rect

    def is_play_button_clicked(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def draw_difficulty_button(self, text, y_position):
        button_rect = pygame.Rect(self.game.window_x // 4, y_position, self.game.window_x // 2, 40)
        pygame.draw.rect(self.game.game_window, self.game.white, button_rect)
        font = pygame.font.Font(None, 28)
        button_text = font.render(text, True, self.game.black)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.game.game_window.blit(button_text, text_rect)

        return button_rect

    def is_difficulty_button_clicked(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def show_rules(self):
        self.game.game_window.fill(self.game.green2)

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
            "- Skończenie się czasu"
        ]

        font = pygame.font.SysFont('times new roman', 20)
        y_position = 50
        for line in rules_text:
            text_surface = font.render(line, True, self.game.white)
            text_rect = text_surface.get_rect(midtop=(self.game.window_x / 2, y_position))
            self.game.game_window.blit(text_surface, text_rect)
            y_position += 30

        understand_button_rect = self.game.draw_understand_button()

        waiting_for_understand = True
        while waiting_for_understand:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.game.is_understand_button_clicked(mouse_pos, understand_button_rect):
                        waiting_for_understand = False
                        self.show_welcome_screen()

            pygame.display.update()


class Snake:
    def __init__(self, game):
        self.game = game
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.snake_position = [100, 40]
        self.snake_body = [[100, 40], [80, 40]]

    def run(self):
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

            if self.direction == 'UP':
                self.snake_position[1] -= 20
            if self.direction == 'DOWN':
                self.snake_position[1] += 20
            if self.direction == 'LEFT':
                self.snake_position[0] -= 20
            if self.direction == 'RIGHT':
                self.snake_position[0] += 20

            self.game.timer -= 1

            if self.game.timer == 0:
                self.game.game_over()

            if (
                    self.game.fruit_position[0] == self.snake_position[0] and
                    self.game.fruit_position[1] == self.snake_position[1]
            ):
                self.game.score += 1
                self.game.fruit_spawn = False
            else:
                if len(self.snake_body) > 1:
                    self.snake_body.pop()
                else:
                    self.game.game_over()

            if not self.game.fruit_spawn:
                self.game.fruit_position = [
                    random.randrange(1, (self.game.window_x // 20 - 1)) * 20,
                    random.randrange(1, (self.game.window_y // 20 - 1)) * 20
                ]

            self.game.fruit_spawn = True
            self.game.game_window.fill(self.game.green)

            for pos in self.snake_body:
                pygame.draw.rect(self.game.game_window, self.game.white, pygame.Rect(pos[0], pos[1], 20, 20))
            pygame.draw.rect(self.game.game_window, self.game.black, pygame.Rect(
                self.game.fruit_position[0], self.game.fruit_position[1], 20, 20))

            if self.snake_position[0] < -5 or self.snake_position[0] >= self.game.window_x:
                self.game.game_over()
            if self.snake_position[1] < -5 or self.snake_position[1] >= self.game.window_y:
                self.game.game_over()

            for block in self.snake_body:
                if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                    self.game.game_over()

            self.snake_body.insert(0, list(self.snake_position))

            self.game.show_timer('times new roman', 20)

            self.game.show_score(1, self.game.white, 'times new roman', 20)

            pygame.display.update()

            self.game.fps.tick(self.game.snake_speed)


class Board:
    def __init__(self, game):
        self.game = game
        self.timer_rect = pygame.Rect(self.game.window_x - 150, 0, 140, 0)
        self.timer = 120
        self.score = 0
        self.points = 0
        self.fruit_spawn = True
        self.fruit_position = [random.randrange(1, (self.game.window_x // 20)) * 20,
                               random.randrange(1, (self.game.window_y // 20)) * 20]
        self.fps = pygame.time.Clock()

    def choose_level(self):
        self.game.game_window.fill(self.game.green2)
        font = pygame.font.SysFont('times new roman', 36)
        title_surface = font.render("WYBIERZ POZIOM TRUDNOŚCI", True, self.game.white)
        title_rect = title_surface.get_rect(center=(self.game.window_x / 2, 100))
        self.game.game_window.blit(title_surface, title_rect)

        easy_button_rect = self.game.draw_difficulty_button("ŁATWY", self.game.window_y / 3)
        medium_button_rect = self.game.draw_difficulty_button("ŚREDNI", self.game.window_y / 2)
        hard_button_rect = self.game.draw_difficulty_button("TRUDNY", self.game.window_y / 3 * 2)

        pygame.display.flip()

        waiting_for_difficulty = True
        while waiting_for_difficulty:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.game.is_difficulty_button_clicked(mouse_pos, easy_button_rect):
                        self.game.snake_speed = 10
                        waiting_for_difficulty = False
                        self.game.points_multiplier = 10
                        self.timer = 500
                        self.game.run()
                    elif self.game.is_difficulty_button_clicked(mouse_pos, medium_button_rect):
                        self.game.snake_speed = 20
                        waiting_for_difficulty = False
                        self.game.points_multiplier = 15
                        self.timer = 1000
                        self.game.run()
                    elif self.game.is_difficulty_button_clicked(mouse_pos, hard_button_rect):
                        self.game.snake_speed = 30
                        waiting_for_difficulty = False
                        self.game.points_multiplier = 20
                        self.timer = 1500
                        self.game.run()

            pygame.display.update()

    def show_tire_disposal_concept(self):
        self.game.game_window.fill(self.game.green2)

        font = pygame.font.SysFont('times new roman', 25)
        text_lines = [
            'Edukacyjny koncept dotyczący utylizacji opon:',
            'Odpowiednia utylizacja opon jest kluczowa dla ochrony środowiska.',
            'Zużyte opony powinny być przekazywane',
            'do punktów utylizacji, gdzie',
            'mogą być poddane recyklingowi ',
            'lub zagospodarowane w sposób bezpieczny.'
        ]

        y_position = 40
        for line in text_lines:
            text_surface = font.render(line, True, self.game.white)
            text_rect = text_surface.get_rect(midtop=(self.game.window_x / 2, y_position))
            self.game.game_window.blit(text_surface, text_rect)
            y_position += text_surface.get_height() + 10

        understand_button_rect = self.game.draw_understand_button()

        pygame.display.flip()

        waiting_for_understand = True
        while waiting_for_understand:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.game.is_understand_button_clicked(mouse_pos, understand_button_rect):
                        waiting_for_understand = False

            pygame.display.update()

        self.game.show_welcome_screen()

    def draw_super_button(self):
        button_rect = pygame.Rect(self.game.window_x // 4, self.game.window_y - 50, self.game.window_x // 2, 40)
        pygame.draw.rect(self.game.game_window, self.game.white, button_rect)
        font = pygame.font.Font(None, 28)
        button_text = font.render("SUPER!", True, self.game.black)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.game.game_window.blit(button_text, text_rect)

        return button_rect

    def is_super_button_clicked(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def game_over(self):
        self.game.game_window.fill(self.game.green2)
        my_font = pygame.font.SysFont('times new roman', 50)

        self.points = self.score * self.game.points_multiplier

        line1_text = f'ZEBRANE OPONY: {self.score}'
        line2_text = f'ZDOBYTE PUNKTY: {self.points}'

        line1_surface = my_font.render(line1_text, True, self.game.grey)
        line2_surface = my_font.render(line2_text, True, self.game.grey)

        line1_rect = line1_surface.get_rect(center=(self.game.window_x / 2, self.game.window_y / 4))
        line2_rect = line2_surface.get_rect(center=(self.game.window_x / 2, self.game.window_y / 4 + line1_rect.height + 10))

        self.game.game_window.blit(line1_surface, line1_rect)
        self.game.game_window.blit(line2_surface, line2_rect)

        score = self.game.get_score()
        print(score)

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

    def draw_understand_button(self):
        button_rect = pygame.Rect(self.game.window_x // 4, self.game.window_y - 50, self.game.window_x // 2, 40)
        pygame.draw.rect(self.game.game_window, self.game.white, button_rect)
        font = pygame.font.Font(None, 28)
        button_text = font.render("ROZUMIEM", True, self.game.black)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.game.game_window.blit(button_text, text_rect)

        return button_rect

    def is_understand_button_clicked(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def get_score(self):
        return self.points



if __name__ == "__main__":
    pygame.init()
    game = SnakeGame()
    game.show_welcome_screen()
