import pygame

from Events.QuizWindow import QuizWindow
from Events.StatsWindow import StatsWindow
from Events.AchievementsWindow import AchievementsWindow
from mglobals import PLAYER_OBJ


def game(player_name, width=1200, height=800):
    players = [player.player_name for player in PLAYER_OBJ.values()]
    session_data = [[] for _ in range(3)]
    score = -1
    pygame.init()

    screen_w, screen_h = width, height
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
    exit_button_rect = pygame.Rect((screen_w - button_width) // 2, (screen_h - button_height) // 2 + 225,
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
                        quiz = QuizWindow(player_name)
                        try:
                            session_data = quiz.player_data
                            score = session_data[1][0][2]
                        except IndexError:
                            score = 0
                        quiz_clicked = True
                    elif stats_button_rect.collidepoint(mouse_x, mouse_y):
                        try:
                            StatsWindow(session_data[0:2], players)
                        except IndexError:
                            screen.blit(overlay_surface, stats_button_rect.topleft)
                    elif achievement_button_rect.collidepoint(mouse_x, mouse_y):
                        try:
                            AchievementsWindow([session_data[0], session_data[2]], players)
                        except IndexError:
                            screen.blit(overlay_surface, achievement_button_rect.topleft)
                    elif exit_button_rect.collidepoint(mouse_x, mouse_y):
                        running = False

        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, (144, 238, 0), quiz_button_rect)
        pygame.draw.rect(screen, (255, 0, 0), stats_button_rect)
        pygame.draw.rect(screen, (32, 128, 64), achievement_button_rect)
        pygame.draw.rect(screen, (0, 0, 255), exit_button_rect)

        font = pygame.font.Font(None, 36)

        quiz_text = font.render("Quiz", True, (0, 0, 0))
        stats_text = font.render("Statystyki", True, (0, 0, 0))
        achievements_text = font.render("Osiągnięcia", True, (0, 0, 0))
        exit_text = font.render("Wyjdź", True, (255, 255, 255))

        quiz_text_rect = quiz_text.get_rect(center=quiz_button_rect.center)
        stats_text_rect = stats_text.get_rect(center=stats_button_rect.center)
        achievements_text_rect = achievements_text.get_rect(center=achievement_button_rect.center)
        exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)

        screen.blit(quiz_text, quiz_text_rect.topleft)
        screen.blit(stats_text, stats_text_rect.topleft)
        screen.blit(achievements_text, achievements_text_rect.topleft)
        screen.blit(exit_text, exit_text_rect.topleft)

        if quiz_clicked:
            screen.blit(overlay_surface, quiz_button_rect.topleft)

        pygame.display.flip()
        clock.tick(60)

    return score
