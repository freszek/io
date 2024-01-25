import pygame
import sys
import random

pygame.init()


class DoorGame:
    BACKGROUND_COLOR = (39, 174, 96)
    BLACK = (0, 0, 0)
    WITHE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BROWN = (165, 42, 42)
    DOOR_WIDTH = 285
    DOOR_HEIGHT = 500
    BORDER_WIDTH = 5
    FONT_SIZE = 36
    FONT_COLOR = (0, 0, 0)
    CHANGE_TIMES = (1000, 2000, 3000)

    def __init__(self, width=1000, height=600, duration=30):
        self.WIDTH = width
        self.HEIGHT = height
        self.duration = duration
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("DoorGame")

        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.score = 0
        self.elapsed_time = 0

    def show_instructions_popup(self):
        popup_width, popup_height = 600, 300
        popup_screen = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("DoorGame")

        font = pygame.font.Font(None, 30)
        text1 = font.render("Welcome to DoorGame!", True, self.FONT_COLOR)
        text2 = font.render("Instructions:", True, self.FONT_COLOR)
        text3 = font.render("1. Click on the yellow doors to score points.", True, self.FONT_COLOR)
        text4 = font.render("2. Each yellow door click earns you 5 points.", True, self.FONT_COLOR)
        text5 = font.render("3. You have 30 seconds.", True, self.FONT_COLOR)
        text6 = font.render("Press any key to start the game. Good luck!", True, self.FONT_COLOR)

        popup_screen.fill(self.BACKGROUND_COLOR)
        popup_screen.blit(text1, (20, 20))
        popup_screen.blit(text2, (20, 70))
        popup_screen.blit(text3, (20, 120))
        popup_screen.blit(text4, (20, 150))
        popup_screen.blit(text5, (20, 180))
        popup_screen.blit(text6, (20, 250))

        pygame.display.flip()

        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.elapsed_time = 0
                    self.clock = pygame.time.Clock()
                    self.start_time = pygame.time.get_ticks()
                    waiting_for_key = False

        pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.event.get()

    def end_game(self):

        if self.elapsed_time >= self.duration:
            self.screen.fill(self.BACKGROUND_COLOR)

            font = pygame.font.Font(None, 72)
            end_text = font.render(f'Game Over!', True, self.FONT_COLOR)
            end_rect = end_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - self.DOOR_HEIGHT // 2 - 20))
            self.screen.blit(end_text, end_rect)

            score_text = font.render(f'Your Score: {self.score}', True, self.FONT_COLOR)
            score_rect = score_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + self.DOOR_HEIGHT // 2 - 200))
            self.screen.blit(score_text, score_rect)

            pygame.display.flip()

            waiting_for_exit = True
            while waiting_for_exit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting_for_exit = False

            self.screen = pygame.display.set_mode((1200, 800))
            self.screen.fill(self.WITHE)

            return self.score

    def update_colors(self, doors):
        current_time = pygame.time.get_ticks()

        for door in doors:
            if door['color'] == self.YELLOW and current_time - door['change_time'] >= 500:
                door['color'] = self.BLACK
                door['change_time'] = current_time + random.choice(self.CHANGE_TIMES)
            elif door['color'] == self.BLACK and current_time >= door['change_time']:
                door['color'] = self.YELLOW
                door['change_time'] = current_time + random.choice(self.CHANGE_TIMES)

    def run_game(self):
        doors = [{'rect': pygame.Rect(20 + i, self.HEIGHT - self.DOOR_HEIGHT, self.DOOR_WIDTH, self.DOOR_HEIGHT),
                  'color': self.BLACK,
                  'change_time': self.start_time + random.choice(self.CHANGE_TIMES)} for i in
                 range(0, self.WIDTH, self.DOOR_WIDTH + 50)]

        self.show_instructions_popup()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for door in doors:
                        if door['rect'].collidepoint(event.pos):
                            if door['color'] == self.YELLOW:
                                door['color'] = self.BLACK
                                self.score += 5

            result = self.end_game()
            if result is not None:
                return result

            self.update_colors(doors)

            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            self.screen.fill(self.BACKGROUND_COLOR)

            for door in doors:
                pygame.draw.rect(self.screen, self.BROWN,
                                 (door['rect'].left - self.BORDER_WIDTH,
                                  door['rect'].top - self.BORDER_WIDTH,
                                  self.DOOR_WIDTH + 2 * self.BORDER_WIDTH,
                                  self.DOOR_HEIGHT + 2 * self.BORDER_WIDTH))
                pygame.draw.rect(self.screen, door['color'], door['rect'])

            font = pygame.font.Font(None, self.FONT_SIZE)
            time_text = font.render(f'Time: {self.elapsed_time}', True, self.FONT_COLOR)
            time_rect = time_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - self.DOOR_HEIGHT // 2 - 20))
            self.screen.blit(time_text, time_rect)

            score_text = font.render(f'Score: {self.score}', True, self.FONT_COLOR)
            score_rect = score_text.get_rect(topleft=(self.WIDTH - 150, 10))
            self.screen.blit(score_text, score_rect)

            pygame.display.flip()
            self.clock.tick(60)