import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 80
TAP_SIZE = 80
WATER_DROP_SIZE = 5
NPC_SIZE = 50
FPS = 60
WATER_COUNTER = 10

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player_icon.png")
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.selected_tap = None
        self.moving_to_tap = False
        self.moving_to_position = False
        self.target_position = None

    def update(self):
        if self.moving_to_tap and self.selected_tap:
            dx = self.selected_tap.rect.centerx - self.rect.centerx
            dy = self.selected_tap.rect.centery - self.rect.centery
            distance = pygame.math.Vector2(dx, dy).length()

            if distance > 2:
                speed = 2
                direction = pygame.math.Vector2(dx, dy).normalize() * speed
                self.rect.x += direction.x
                self.rect.y += direction.y
            else:
                self.moving_to_tap = False
                self.selected_tap.zakrecony = not self.selected_tap.zakrecony

        elif self.moving_to_position and self.target_position:
            dx = self.target_position[0] - self.rect.centerx
            dy = self.target_position[1] - self.rect.centery
            distance = pygame.math.Vector2(dx, dy).length()

            if distance > 2:
                speed = 2
                direction = pygame.math.Vector2(dx, dy).normalize() * speed
                self.rect.x += direction.x
                self.rect.y += direction.y
            else:
                self.moving_to_position = False


class Tap(pygame.sprite.Sprite):
    def __init__(self, x, y, water_flow_rate=0.1):
        super().__init__()
        self.image_zakrecony = pygame.image.load("tap_icon.png")
        self.image_odkrecany = pygame.image.load("odkrecony_tap.png")
        self.image = self.image_zakrecony
        self.image = pygame.transform.scale(self.image, (TAP_SIZE, TAP_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.zakrecony = True
        self.water_flow_rate = water_flow_rate


    def update(self):
        if not self.zakrecony:
            self.image = self.image_odkrecany
            self.image = pygame.transform.scale(self.image, (TAP_SIZE, TAP_SIZE))
        else:
            self.image = self.image_zakrecony
            self.image = pygame.transform.scale(self.image, (TAP_SIZE+20, TAP_SIZE+20))


class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("npc_icon.png")
        self.image = pygame.transform.scale(self.image, (NPC_SIZE, NPC_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 4)
        self.target_tap = None
        self.moving_to_tap = False

    def update(self):
        if not self.moving_to_tap:
            available_taps = [t for t in all_taps.sprites() if t.zakrecony]
            if available_taps:
                self.target_tap = random.choice(available_taps)
                self.moving_to_tap = True

        if self.moving_to_tap and self.target_tap:
            dx = self.target_tap.rect.centerx - self.rect.centerx
            dy = self.target_tap.rect.centery - self.rect.centery
            distance = pygame.math.Vector2(dx, dy).length()

            if distance > 2:
                speed = 1
                direction = pygame.math.Vector2(dx, dy).normalize() * speed
                self.rect.x += direction.x
                self.rect.y += direction.y
            else:
                self.moving_to_tap = False
                self.target_tap.zakrecony = False
                global WATER_COUNTER
                WATER_COUNTER -= self.target_tap.water_flow_rate


def generate_tap_positions(num_taps):
    tap_positions = []
    occupied_rects = []

    for _ in range(num_taps):
        tap_rect = pygame.Rect(0, 0, TAP_SIZE, TAP_SIZE)
        while True:
            tap_rect.topleft = (random.randint(0, WIDTH - TAP_SIZE), random.randint(0, HEIGHT - TAP_SIZE))
            if not any(tap_rect.colliderect(occupied_rect) for occupied_rect in occupied_rects):
                occupied_rects.append(tap_rect.copy())
                tap_positions.append((tap_rect.x, tap_rect.y, 0.1))
                break

    return tap_positions


def show_start_screen(instruction_text):
    screen.fill((0, 0, 0))

    font = pygame.font.Font(None, int(36 * min(WIDTH, HEIGHT) / 800))
    for i, line in enumerate(instruction_text):
        text = font.render(line, True, WHITE)
        screen.blit(text, (int(10 * min(WIDTH, HEIGHT) / 800), int((10 + i * 30) * min(WIDTH, HEIGHT) / 800)))

    pygame.display.flip()

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_start = False


flags = pygame.DOUBLEBUF | pygame.RESIZABLE
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

instruction_text = [
    "Witaj w minigrze WaterSafe!",
    "Twoim zadaniem jest oszczędzanie wody, zakręcając krany.",
    "Kliknij lewym przyciskiem myszy na kran, aby go zakręcić.",
    "Możesz również kliknąć w inne miejsce, aby się przemieszczać.",
    "Masz 30 sekund na ukończenie gry. Oszczędzaj wodę!",
    "Kliknij dowolny klawisz lub lewy przycisk myszy, aby rozpocząć."
]

show_start_screen(instruction_text)

clock = pygame.time.Clock()

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

all_taps_list = []

tap_positions = generate_tap_positions(6)

for pos in tap_positions:
    tap = Tap(*pos)
    all_sprites.add(tap)
    all_taps_list.append(tap)

all_taps = pygame.sprite.Group(all_taps_list)

npc1 = NPC()
npc2 = NPC()
all_sprites.add(npc1, npc2)

running = True
game_duration = 30
elapsed_time = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()

            clicked_sprites = [s for s in all_taps.sprites() if s.rect.collidepoint(pos)]
            if clicked_sprites and not clicked_sprites[0].zakrecony:
                player.selected_tap = clicked_sprites[0]
                player.moving_to_tap = True
                player.moving_to_position = False
            else:
                player.target_position = pos
                player.moving_to_tap = False
                player.moving_to_position = True
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            for tap in all_taps.sprites():
                tap.rect.topleft = (random.randint(0, WIDTH - TAP_SIZE), random.randint(0, HEIGHT - TAP_SIZE))
            player.rect.center = (WIDTH // 2, HEIGHT // 2)

    for tap in all_taps.sprites():
        if not tap.zakrecony:
            WATER_COUNTER -= tap.water_flow_rate / FPS
    all_sprites.update()

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    font = pygame.font.Font(None, int(36 * min(WIDTH, HEIGHT) / 800))
    text = font.render(f"Woda: {WATER_COUNTER:.1f} litrów", True, WHITE)
    screen.blit(text, (int(10 * min(WIDTH, HEIGHT) / 800), int(10 * min(WIDTH, HEIGHT) / 800)))

    timer_font = pygame.font.Font(None, int(36 * min(WIDTH, HEIGHT) / 800))
    timer_text = timer_font.render(f"Czas: {int(game_duration - elapsed_time)} s", True, WHITE)
    screen.blit(timer_text, (WIDTH - int(150 * min(WIDTH, HEIGHT) / 800), int(10 * min(WIDTH, HEIGHT) / 800)))

    pygame.display.flip()

    elapsed_time += clock.get_time() / 1000

    if elapsed_time >= game_duration:
        running = False

    if WATER_COUNTER <= 0:
        running = False

    clock.tick(FPS)


screen.fill((0, 0, 0))
font = pygame.font.Font(None, int(72 * min(WIDTH, HEIGHT) / 800))
result_text1 = font.render("Koniec gry!", True, WHITE)
result_text2 = font.render(f"Pozostała woda: {WATER_COUNTER:.1f} litrów", True, WHITE)
screen.blit(result_text1, (WIDTH // 3, HEIGHT // 3))
screen.blit(result_text2, (WIDTH // 8, HEIGHT // 2))
pygame.display.flip()

waiting_for_exit = True
while waiting_for_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting_for_exit = False

pygame.quit()
sys.exit()
