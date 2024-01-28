import pygame
import sys

class RoundEndedInfo:
    def __init__(self, round_number, leader):
        self.round_number = round_number
        self.info_displayed = False
        self.closed = False
        self.leader = leader

    def display_info(self):
        if not self.info_displayed:
            print(f"Round {self.round_number} ended!")
            self.info_displayed = True
            self.show_pygame_scene()

    def show_pygame_scene(self):
        pygame.init()
        screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption(f"Round {self.round_number} Ended!")

        # Load the background image
        background_image = pygame.image.load("background.jpg")
        background_image = pygame.transform.scale(background_image, (1200, 800))
        screen.blit(background_image, (0, 0))

        font = pygame.font.Font(None, 96)
        text = font.render(f"Round {self.round_number} Ended!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(600, 200))
        text2 = font.render(f"Current leader: {self.leader}", True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(600, 300))

        button_stats = pygame.Rect(200, 600, 400, 100)
        button_next_round = pygame.Rect(600, 600, 400, 100)

        white = (255, 255, 255)
        green = (0, 128, 0)

        pygame.draw.rect(screen, white, (150, 550, 500, 200))
        pygame.draw.rect(screen, white, (550, 550, 500, 200))

        pygame.draw.rect(screen, green, button_stats)
        pygame.draw.rect(screen, green, button_next_round)

        font_button = pygame.font.Font(None, 48)
        text_next_round = font_button.render("Start Next Round", True, (255, 255, 255))

        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text_next_round, (button_next_round.x + 50, button_next_round.y + 30))

        pygame.display.flip()

        while not self.closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button_stats.collidepoint(mouse_pos):
                        print("Show Round Statistics clicked!")
                        # Add logic to show round statistics
                    elif button_next_round.collidepoint(mouse_pos):
                        print("Start Next Round clicked!")
                        # Add logic to start the next round
                        self.closed = True