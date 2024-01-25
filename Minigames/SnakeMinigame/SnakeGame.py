import pygame
import random
import sys

class SnakeGame:
    def __init__(self, width=1200, height=800, duration=120):
        pygame.init()
        self.points_multiplier = 10
        self.snake_speed = 10
        self.window_x = width
        self.window_y = height
        self.tire = pygame.image.load('Minigames/SnakeMinigame/Images/tire.jpg')
        self.field = pygame.image.load('Minigames/SnakeMinigame/Images/field.jpg')
        self.head_up = pygame.image.load('Minigames/SnakeMinigame/Images/head_up.png')
        self.head_down = pygame.image.load('Minigames/SnakeMinigame/Images/head_down.png')
        self.head_left = pygame.image.load('Minigames/SnakeMinigame/Images/head_left.png')
        self.head_right = pygame.image.load('Minigames/SnakeMinigame/Images/head_right.png')
        self.blue = (100, 125, 255)
        self.green = (18, 102, 79)
        self.green2 = (31, 173, 135)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.grey = (183, 183, 183)
        self.timer = duration
        self.timer_rect = pygame.Rect(self.window_x - 150, 0, 140, 0)
        self.score = 0
        self.points = 0
        self.snake_position = [100, 40]
        self.snake_body = [[100, 40],
                           [80, 40]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
        self.fps = pygame.time.Clock()
        self.fruit_spawn = True
        self.fruit_position = [random.randrange(1, (self.window_x // 20)) * 20,
                               random.randrange(1, (self.window_y // 20)) * 20]

    def run_game(self):
        self.game_window.fill(self.green2)
        result = 0

        font = pygame.font.SysFont('times new roman', 36)
        title_surface = font.render("WITAJ W GRZE GREENSNAKE", True, self.white)
        title_rect = title_surface.get_rect(center=(self.window_x / 2, self.window_y / 4))
        self.game_window.blit(title_surface, title_rect)

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
                        result = self.choose_level()
                        return result
                    elif self.is_how_to_play_button_clicked(mouse_pos, how_to_play_button_rect):
                        self.show_rules()

            pygame.display.update()
        return result

    def draw_how_to_play_button(self):
        button_rect = pygame.Rect(self.window_x // 4, self.window_y / 2 + 50, self.window_x // 2, 40)
        pygame.draw.rect(self.game_window, self.white, button_rect)
        font = pygame.font.Font(None, 28)
        button_text = font.render("JAK GRAĆ?", True, self.black)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.game_window.blit(button_text, text_rect)

        return button_rect

    def is_how_to_play_button_clicked(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def draw_play_button(self):
        button_rect = pygame.Rect(self.window_x // 4, self.window_y / 2, self.window_x // 2, 40)
        pygame.draw.rect(self.game_window, self.white, button_rect)
        font = pygame.font.Font(None, 28)
        button_text = font.render("GRAJ", True, self.black)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.game_window.blit(button_text, text_rect)

        return button_rect

    def is_play_button_clicked(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def draw_difficulty_button(self, text, y_position):
        button_rect = pygame.Rect(self.window_x // 4, y_position, self.window_x // 2, 40)
        pygame.draw.rect(self.game_window, self.white, button_rect)
        font = pygame.font.Font(None, 28)
        button_text = font.render(text, True, self.black)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.game_window.blit(button_text, text_rect)

        return button_rect

    def is_difficulty_button_clicked(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def show_rules(self):
        self.game_window.fill(self.black)

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
                        self.run_game()

            pygame.display.update()

    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Zebrane opony: ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        self.game_window.blit(score_surface, score_rect)

    def show_timer(self, font, size):
        timer_font = pygame.font.SysFont(font, size)
        timer_surface = timer_font.render('Czas: ' + str(self.timer), True, self.white)
        self.game_window.fill(self.black, self.timer_rect)
        self.game_window.blit(timer_surface, self.timer_rect)

    def choose_level(self):
        result = 0
        self.game_window.fill(self.green2)
        font = pygame.font.SysFont('times new roman', 36)
        title_surface = font.render("WYBIERZ POZIOM TRUDNOŚCI", True, self.white)
        title_rect = title_surface.get_rect(center=(self.window_x / 2, 100))
        self.game_window.blit(title_surface, title_rect)

        easy_button_rect = self.draw_difficulty_button("ŁATWY", self.window_y / 3)
        medium_button_rect = self.draw_difficulty_button("ŚREDNI", self.window_y / 2)
        hard_button_rect = self.draw_difficulty_button("TRUDNY", self.window_y / 3 * 2)

        pygame.display.flip()

        waiting_for_difficulty = True
        while waiting_for_difficulty:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_difficulty_button_clicked(mouse_pos, easy_button_rect):
                        self.snake_speed = 10
                        waiting_for_difficulty = False
                        self.points_multiplier = 10
                        self.timer = 500
                        result = self.run()
                        return result
                    elif self.is_difficulty_button_clicked(mouse_pos, medium_button_rect):
                        self.snake_speed = 20
                        waiting_for_difficulty = False
                        self.points_multiplier = 15
                        self.timer = 1000
                        result = self.run()
                        return result
                    elif self.is_difficulty_button_clicked(mouse_pos, hard_button_rect):
                        self.snake_speed = 30
                        waiting_for_difficulty = False
                        self.points_multiplier = 20
                        self.timer = 1500
                        result = self.run()
                        return result

            pygame.display.update()


    def show_tire_disposal_concept(self):
        self.game_window.fill(self.green2)

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
        button_text = font.render("SUPER!", True, self.black)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.game_window.blit(button_text, text_rect)

        return button_rect

    def is_super_button_clicked(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def game_over(self):
        self.game_window.fill(self.green2)
        my_font = pygame.font.SysFont('times new roman', 50)

        self.points = self.score * self.points_multiplier

        line1_text = f'ZEBRANE OPONY: {self.score}'
        line2_text = f'ZDOBYTE PUNKTY: {self.points}'

        line1_surface = my_font.render(line1_text, True, self.grey)
        line2_surface = my_font.render(line2_text, True, self.grey)

        line1_rect = line1_surface.get_rect(center=(self.window_x / 2, self.window_y / 4))
        line2_rect = line2_surface.get_rect(center=(self.window_x / 2, self.window_y / 4 + line1_rect.height + 10))

        self.game_window.blit(line1_surface, line1_rect)
        self.game_window.blit(line2_surface, line2_rect)

        score = self.get_score()
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
        self.game_window.fill(self.white)
        return self.points

    def draw_understand_button(self):
        button_rect = pygame.Rect(self.window_x // 4, self.window_y - 50, self.window_x // 2, 40)
        pygame.draw.rect(self.game_window, self.white, button_rect)
        font = pygame.font.Font(None, 28)
        button_text = font.render("ROZUMIEM", True, self.black)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.game_window.blit(button_text, text_rect)

        return button_rect

    def is_understand_button_clicked(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def get_score(self):
        return self.points

    def run(self):
        pygame.time.wait(1000)
        tire_resized = pygame.transform.scale(self.tire, (20, 20))
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

            self.timer -= 1

            if self.timer == 0:
                result = self.game_over()
                return result

            if (
                    self.fruit_position[0] == self.snake_position[0] and
                    self.fruit_position[1] == self.snake_position[1]
            ):
                self.score += 1
                self.fruit_spawn = False
            else:
                if len(self.snake_body) > 0:
                    self.snake_body.pop()
                else:
                    result = self.game_over()
                    return result

            if not self.fruit_spawn:
                self.fruit_position = [
                    random.randrange(1, (self.window_x // 20 - 1)) * 20,
                    random.randrange(1, (self.window_y // 20 - 1)) * 20
                ]

            self.fruit_spawn = True
            field_resized = pygame.transform.scale(self.field, (self.window_x, self.window_y))
            self.game_window.blit(field_resized, (0, 0))
            head_up_resized = pygame.transform.scale(self.head_up, (20, 20))
            head_down_resized = pygame.transform.scale(self.head_down, (20, 20))
            head_left_resized = pygame.transform.scale(self.head_left, (20, 20))
            head_right_resized = pygame.transform.scale(self.head_right, (20, 20))

            for idx, pos in enumerate(self.snake_body):
                if idx == 0:
                    if self.direction == 'UP':
                        self.game_window.blit(head_up_resized, (pos[0], pos[1]))
                    elif self.direction == 'DOWN':
                        self.game_window.blit(head_down_resized, (pos[0], pos[1]))
                    elif self.direction == 'LEFT':
                        self.game_window.blit(head_left_resized, (pos[0], pos[1]))
                    elif self.direction == 'RIGHT':
                        self.game_window.blit(head_right_resized, (pos[0], pos[1]))
                else:
                    pygame.draw.rect(self.game_window, self.blue, pygame.Rect(pos[0], pos[1], 20, 20))

            self.game_window.blit(tire_resized, (self.fruit_position[0], self.fruit_position[1]))

            if self.snake_position[0] < -5 or self.snake_position[0] >= self.window_x:
                result = self.game_over()
                return result
            if self.snake_position[1] < -5 or self.snake_position[1] >= self.window_y:
                result = self.game_over()
                return result

            for block in self.snake_body:
                if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                    result = self.game_over()
                    return result

            self.snake_body.insert(0, list(self.snake_position))

            self.show_timer('times new roman', 20)

            self.show_score(1, self.white, 'times new roman', 20)

            pygame.display.update()

            self.fps.tick(self.snake_speed)