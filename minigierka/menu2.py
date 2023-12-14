import pygame
import sys

def show_menu():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    FPS = 60
    WHITE = (255, 255, 255)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu")

    font = pygame.font.Font(None, 36)
    title_text = font.render("Green game", True, (0, 0, 0))
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and start_button.collidepoint(event.pos):
                    return True

        screen.fill(WHITE)
        pygame.draw.rect(screen, (0, 255, 0), start_button)
        screen.blit(title_text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
        start_text = font.render("Start", True, (0, 0, 0))
        screen.blit(start_text, (WIDTH // 2 - 60, HEIGHT // 2 - 40))

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)