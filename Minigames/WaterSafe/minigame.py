import pygame
import sys
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.image.load("Minigames/WaterSafe/pics_game/player_icon.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
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
    TAP_SIZE = 80

    def __init__(self, x, y, water_flow_rate=0.1):
        super().__init__()
        self.image_zakrecony = pygame.image.load("Minigames/WaterSafe/pics_game/tap_icon.png")
        self.image_odkrecany = pygame.image.load("Minigames/WaterSafe/pics_game/odkrecony_tap.png")
        self.image = self.image_zakrecony
        self.image = pygame.transform.scale(self.image, (self.TAP_SIZE, self.TAP_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.zakrecony = True
        self.water_flow_rate = water_flow_rate

    def update(self):
        if not self.zakrecony:
            self.image = self.image_odkrecany
            self.image = pygame.transform.scale(self.image, (self.TAP_SIZE, self.TAP_SIZE))
        else:
            self.image = self.image_zakrecony
            self.image = pygame.transform.scale(self.image, (self.TAP_SIZE + 20, self.TAP_SIZE + 20))


class NPC(pygame.sprite.Sprite):
    NPC_SIZE = 50

    def __init__(self, all_taps, game):
        super().__init__()
        self.image = pygame.image.load("Minigames/WaterSafe/pics_game/npc_icon.png")
        self.image = pygame.transform.scale(self.image, (self.NPC_SIZE, self.NPC_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (game.WIDTH // 4, game.HEIGHT // 4)
        self.target_tap = None
        self.moving_to_tap = False
        self.all_taps = all_taps
        self.water_counter = game.WATER_COUNTER

    def update(self):
        if not self.moving_to_tap:
            available_taps = [t for t in self.all_taps.sprites() if t.zakrecony]
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
                self.water_counter -= self.target_tap.water_flow_rate


class WaterSafeGame:
    def __init__(self, width=1200, height=800, duration=30):
        self.WIDTH = width
        self.HEIGHT = height
        self.PLAYER_SIZE = int(80 * min(self.WIDTH, self.HEIGHT) / 800)
        self.TAP_SIZE = int(80 * min(self.WIDTH, self.HEIGHT) / 800)
        self.FPS = 60
        self.WATER_COUNTER = 13
        self.NPC_SIZE = int(50 * min(self.WIDTH, self.HEIGHT) / 800)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.duration = duration
        self.game_running = False
        self.start_button_rect = pygame.Rect(self.WIDTH // 3, self.HEIGHT // 2,
                                             int(200 * min(self.WIDTH, self.HEIGHT) / 800),
                                             int(50 * min(self.WIDTH, self.HEIGHT) / 800))
        self.start_button_color = (0, 255, 0)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.clock = None

        self.background = pygame.image.load("Minigames/WaterSafe/pics_game/background.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.instruction_text = [
            "Witaj w minigrze WaterSafe!",
            "Twoim zadaniem jest oszczędzanie wody, zakręcając krany.",
            "Kliknij lewym przyciskiem myszy na kran, aby go zakręcić.",
            "ESC-zatrzymanie/wznowienie gry",
            "Możesz również kliknąć w inne miejsce, aby się przemieszczać.",
            "Masz 30 sekund na ukończenie gry. ",
            "Oszczędzanie wody to klucz do zrównoważonego rozwoju i ochrony środowiska. ",
            "Właściwe gospodarowanie wodą pomaga nie tylko środowisku, ",
            "ale także zmniejsza koszty i wspiera globalne wysiłki dotyczące dostępu do czystej wody.",
            "Oszczędzaj wodę!",
            "Kliknij lewy przycisk myszy, aby rozpocząć."
        ]
        self.paused = False
        self.current_elapsed_time = 0
        self.current_elapsed_time_before = 0


    def generate_tap_positions(self, num_taps):
        tap_positions = []
        occupied_rects = []

        for _ in range(num_taps):
            tap_rect = pygame.Rect(0, 0, self.TAP_SIZE, self.TAP_SIZE)
            while True:
                tap_rect.topleft = (
                    random.randint(0, self.WIDTH - self.TAP_SIZE), random.randint(0, self.HEIGHT - self.TAP_SIZE))
                if not any(tap_rect.colliderect(occupied_rect) for occupied_rect in occupied_rects):
                    occupied_rects.append(tap_rect.copy())
                    tap_positions.append((tap_rect.x, tap_rect.y, 0.1))
                    break

        return tap_positions

    def run_game(self):
        self.screen.fill((0, 0, 0))

        font = pygame.font.Font(None, int(36 * min(self.WIDTH, self.HEIGHT) / 800))
        for i, line in enumerate(self.instruction_text):
            text = font.render(line, True, self.WHITE)
            self.screen.blit(text, (int(10 * min(self.WIDTH, self.HEIGHT) / 800),
                                    int((10 + i * 30) * min(self.WIDTH, self.HEIGHT) / 800)))

        pygame.draw.rect(self.screen, self.start_button_color, self.start_button_rect)
        font = pygame.font.Font(None, int(30 * min(self.WIDTH, self.HEIGHT) / 800))
        text = font.render("Start", True, (0, 0, 0))
        text_rect = text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(text, text_rect)

        pygame.display.flip()

        waiting_for_start = True
        while waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button_rect.collidepoint(event.pos):
                        return self.run_g()

    def end_game(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, int(72 * min(self.WIDTH, self.HEIGHT) / 800))
        result_text1 = font.render("Koniec gry!", True, self.WHITE)
        result_text2 = font.render(f"Pozostała woda: {self.WATER_COUNTER:.1f} litrów", True, self.WHITE)
        result = self.WATER_COUNTER * 10
        if result > 100:
            result = 100
        result_text3 = font.render(f"Twój wynik: {result:.0f} punkty/ów", True, self.WHITE)
        self.screen.blit(result_text1, (self.WIDTH // 3, self.HEIGHT // 4))
        self.screen.blit(result_text2, (self.WIDTH // 8, self.HEIGHT // 3))
        self.screen.blit(result_text3, (self.WIDTH // 7, self.HEIGHT // 2))
        pygame.display.flip()

        waiting_for_exit = True
        while waiting_for_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_exit = False

        return result

    def pause_game(self):
        paused_start_time = pygame.time.get_ticks()
        paused_clock_time = self.clock.get_time()
        self.paused = True

        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.paused = False

            self.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, int(72 * min(self.WIDTH, self.HEIGHT) / 800))
            paused_text = font.render("Gra wstrzymana", True, self.WHITE)
            self.screen.blit(paused_text, (self.WIDTH // 3, self.HEIGHT // 2))
            pygame.display.flip()

        self.clock.tick()
        self.current_elapsed_time_before += (pygame.time.get_ticks() - paused_start_time) / 1000
        self.clock.tick_busy_loop(paused_clock_time)



    def run_g(self):
        player = Player(self.WIDTH, self.HEIGHT)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)

        all_taps_list = []

        tap_positions = self.generate_tap_positions(6)

        for pos in tap_positions:
            tap = Tap(*pos)
            all_sprites.add(tap)
            all_taps_list.append(tap)

        all_taps = pygame.sprite.Group(all_taps_list)

        npc1 = NPC(all_taps, self)
        npc2 = NPC(all_taps, self)
        all_sprites.add(npc1, npc2)
        self.clock = pygame.time.Clock()
        self.game_running = True
        while self.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()

                    clicked_sprites = [s for s in all_taps.sprites() if s.rect.collidepoint(pos)]
                    if clicked_sprites and not clicked_sprites[0].zakrecony:
                        player.selected_tap = clicked_sprites[0]
                        player.moving_to_tap = True
                    else:
                        player.target_position = pos
                        player.moving_to_position = True
                elif event.type == pygame.VIDEORESIZE:
                    self.WIDTH, self.HEIGHT = event.w, event.h
                    self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
                    for tap in all_taps.sprites():
                        tap.rect.topleft = (random.randint(0, self.WIDTH - self.TAP_SIZE),
                                            random.randint(0, self.HEIGHT - self.TAP_SIZE))
                    self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not self.paused:
                            self.pause_game()

            if not self.paused:
                for tap in all_taps.sprites():
                    if not tap.zakrecony:
                        self.WATER_COUNTER -= tap.water_flow_rate * self.clock.get_time() / 1000
                all_sprites.update()

                self.screen.blit(self.background, (0, 0))
                all_sprites.draw(self.screen)

                font = pygame.font.Font(None, int(36 * min(self.WIDTH, self.HEIGHT) / 800))
                text = font.render(f"Woda: {self.WATER_COUNTER:.1f} litrów", True, self.WHITE)
                self.screen.blit(text, (
                    int(10 * min(self.WIDTH, self.HEIGHT) / 800), int(10 * min(self.WIDTH, self.HEIGHT) / 800)))

                timer_font = pygame.font.Font(None, int(36 * min(self.WIDTH, self.HEIGHT) / 800))
                timer_text = timer_font.render(f"Czas: {int(self.duration - self.current_elapsed_time)} s", True, self.WHITE)
                self.screen.blit(timer_text, (
                    self.WIDTH - int(150 * min(self.WIDTH, self.HEIGHT) / 800),
                    int(10 * min(self.WIDTH, self.HEIGHT) / 800)))

                pygame.display.flip()
                self.current_elapsed_time += self.clock.get_time() / 1000

                if self.current_elapsed_time >= self.duration or self.WATER_COUNTER <= 0:
                    self.game_running = False
                    result = self.end_game()
                    self.screen.fill(self.WHITE)
                    return result

                self.clock.tick(self.FPS)
            else:
                pygame.time.delay(50)
