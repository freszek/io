import pygame
import random
import sys

snake_speed = 10

window_x = 800
window_y = 600

light_blue = (173, 216, 230)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)

pygame.init()

pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

snake_position = [100, 40]

snake_body = [[100, 40]]

fruit_position = [random.randrange(1, (window_x // 20)) * 20,
                  random.randrange(1, (window_y // 20)) * 20]

fruit_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

def show_score(choice, color, font, size):
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)

    score_surface = score_font.render('Zebrane opony: ' + str(score), True, color)

    score_rect = score_surface.get_rect()

    game_window.blit(score_surface, score_rect)

def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)

    game_over_surface = my_font.render(
        'Zebrane opony: ' + str(score), True, red)

    game_over_rect = game_over_surface.get_rect()

    game_over_rect.midtop = (window_x / 2, window_y / 4)

    game_window.blit(game_over_surface, game_over_rect)

    super_button_rect = draw_super_button()

    pygame.display.flip()

    waiting_for_super = True
    while waiting_for_super:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if is_super_button_clicked(mouse_pos, super_button_rect):
                    waiting_for_super = False

        pygame.display.update()

    show_tire_disposal_concept()

    pygame.quit()
    sys.exit()


def show_tire_disposal_concept():
    game_window.fill(black)

    font = pygame.font.SysFont('times new roman', 25)
    text_lines = [
        'Edukacyjny koncept dotyczący utylizacji opon:',
        'Odpowiednia utylizacja opon jest kluczowa dla ochrony środowiska.',
        'Zużyte opony powinny być przekazywane do punktów utylizacji, gdzie',
        'mogą być poddane recyklingowi lub zagospodarowane w sposób bezpieczny.'
    ]

    y_position = 40
    for line in text_lines:
        text_surface = font.render(line, True, white)
        text_rect = text_surface.get_rect(midtop=(window_x / 2, y_position))
        game_window.blit(text_surface, text_rect)
        y_position += text_surface.get_height() + 10

    understand_button_rect = draw_understand_button()

    pygame.display.flip()

    waiting_for_understand = True
    while waiting_for_understand:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if is_understand_button_clicked(mouse_pos, understand_button_rect):
                    waiting_for_understand = False

        pygame.display.update()


def draw_super_button():
    button_rect = pygame.Rect(window_x // 4, window_y - 50, window_x // 2, 40)
    pygame.draw.rect(game_window, white, button_rect)
    font = pygame.font.Font(None, 28)
    button_text = font.render("Super!", True, black)
    text_rect = button_text.get_rect(center=button_rect.center)
    game_window.blit(button_text, text_rect)

    return button_rect


def is_super_button_clicked(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)


def draw_understand_button():
    button_rect = pygame.Rect(window_x // 4, window_y - 50, window_x // 2, 40)
    pygame.draw.rect(game_window, white, button_rect)
    font = pygame.font.Font(None, 28)
    button_text = font.render("Rozumiem", True, black)
    text_rect = button_text.get_rect(center=button_rect.center)
    game_window.blit(button_text, text_rect)

    return button_rect


def is_understand_button_clicked(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)


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
    text_surface = font.render(line, True, white)
    text_rect = text_surface.get_rect(midtop=(window_x / 2, y_position))
    game_window.blit(text_surface, text_rect)
    y_position += 30

understand_button_rect = draw_understand_button()

waiting_for_understand = True
while waiting_for_understand:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if is_understand_button_clicked(mouse_pos, understand_button_rect):
                waiting_for_understand = False

    pygame.display.update()

pygame.time.wait(1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_position[1] -= 20
    if direction == 'DOWN':
        snake_position[1] += 20
    if direction == 'LEFT':
        snake_position[0] -= 20
    if direction == 'RIGHT':
        snake_position[0] += 20

    snake_body.insert(0, list(snake_position))
    if (
            fruit_position[0] <= snake_position[0] <= fruit_position[0] + 20
            and fruit_position[1] <= snake_position[1] <= fruit_position[1] + 20
    ):
        score += 1
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 20)) * 20,
                          random.randrange(1, (window_y // 20)) * 20]

    fruit_spawn = True
    game_window.fill(light_blue)

    for pos in snake_body:
        pygame.draw.rect(game_window, white,
                         pygame.Rect(pos[0], pos[1], 20, 20))
    pygame.draw.rect(game_window, black, pygame.Rect(
        fruit_position[0], fruit_position[1], 20, 20))

    if snake_position[0] < 0 or snake_position[0] >= window_x:
        game_over()
    if snake_position[1] < 0 or snake_position[1] >= window_y:
        game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score(1, white, 'times new roman', 20)

    pygame.display.update()

    fps.tick(snake_speed)