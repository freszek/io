import pygame
from QuizWindow import QuizWindow
from StatsWindow import StatsWindow
from AchievementsWindow import AchievementsWindow


def game():
    pygame.init()

    screen_w, screen_h = 800, 600
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Eventy")

    clock = pygame.time.Clock()

    button_width, button_height = 260, 50

    quiz_button_rect = pygame.Rect((screen_w - button_width) // 2, (screen_h - button_height) // 2 - 75,
                                   button_width, button_height)
    stats_button_rect = pygame.Rect((screen_w - button_width) // 2, (screen_h - button_height) // 2 + 25,
                                    button_width, button_height)
    achievement_button_rect = pygame.Rect((screen_w - button_width) // 2, (screen_h - button_height) // 2 + 125,
                                          button_width, button_height)

    quiz_clicked = False

    overlay_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    overlay_surface.fill((255, 255, 255, 128))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if quiz_button_rect.collidepoint(mouse_x, mouse_y) and not quiz_clicked:
                        QuizWindow()
                        quiz_clicked = True

                    elif stats_button_rect.collidepoint(mouse_x, mouse_y):
                        StatsWindow()
                    elif achievement_button_rect.collidepoint(mouse_x, mouse_y):
                        AchievementsWindow()

        pygame.draw.rect(screen, (0, 128, 255), quiz_button_rect)
        pygame.draw.rect(screen, (255, 0, 0), stats_button_rect)
        pygame.draw.rect(screen, (32, 128, 64), achievement_button_rect)

        font = pygame.font.Font(None, 36)

        quiz_text = font.render("Quiz", True, (255, 255, 255))
        stats_text = font.render("Statystyki", True, (255, 255, 255))
        achievements_text = font.render("Osiągnięcia", True, (255, 255, 255))

        quiz_text_rect = quiz_text.get_rect(center=quiz_button_rect.center)
        stats_text_rect = stats_text.get_rect(center=stats_button_rect.center)
        achievements_text_rect = achievements_text.get_rect(center=achievement_button_rect.center)

        screen.blit(quiz_text, quiz_text_rect.topleft)
        screen.blit(stats_text, stats_text_rect.topleft)
        screen.blit(achievements_text, achievements_text_rect.topleft)

        if quiz_clicked:
            screen.blit(overlay_surface, quiz_button_rect.topleft)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    game()
