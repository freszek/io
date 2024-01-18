import pygame
import sys

def show_menu():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    FPS = 60
    WHITE = (255, 255, 255)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu")

    font = pygame.font.SysFont("Yu Gothic UI", 28, bold=True)

    rules_text = font.render("Zasady minigry:", True, (0, 0, 0))
    rules_text2 = font.render("Przeciągnij śmieci do odpowiadających im kontenerów", True, (0, 0, 0))
    rules_text3 = font.render("w jak najkrótszym czasie!", True, (0, 0, 0))
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 1 - 150, 200, 50)
    logo_image = pygame.image.load("../menu/logo.png")
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

        # Wyśrodkowanie tekstu "Zasady minigry:"
        rules_text_rect = rules_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))

        # Wyświetlenie logo
        screen.blit(logo_image, logo_rect)

        screen.blit(rules_text, rules_text_rect)
        screen.blit(rules_text2, (WIDTH // 2 - 380, HEIGHT // 1.75 - 20))

        # Wyśrodkowanie tekstu rules_text3
        rules_text3_rect = rules_text3.get_rect(center=(WIDTH // 2, HEIGHT // 1.75 + 20))
        screen.blit(rules_text3, rules_text3_rect)
        start_text = font.render("Start", True, (0, 0, 0))

        # Wyśrodkowanie tekstu "Start" na przycisku
        start_text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_text_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


show_menu()
