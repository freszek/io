import pygame
import sys
import random
from menu2 import show_menu

# Funkcja generująca planszę gry
def generate_game():
    containers_group.empty()
    trash_group.empty()

    # Tworzenie kontenerów
    for i in range(5):
        container = Container(CONTAINER_COLORS[i], i * (WIDTH // 5), HEIGHT - CONTAINER_HEIGHT)
        containers_group.add(container)

    # Tworzenie śmieci
    for i in range(4):  # Utwórz po trzy śmieci dla każdego koloru
        for color in TRASH_COLORS:
            trash = Trash(color, random.randint(0, WIDTH - TRASH_WIDTH), random.randint(0, HEIGHT - CONTAINER_HEIGHT - TRASH_HEIGHT - 5 ))
            trash_group.add(trash)
    
# Funkcja wyświetlająca menu
def show_menu_and_start_game():
    if not show_menu():
        pygame.quit()
        sys.exit()

    generate_game()

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)

# Inicjalizacja ekranu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sortowanie śmieci")

# Kolory kontenerów
CONTAINER_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 150, 0), (255, 0, 150)]

# Kolory śmieci
TRASH_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 150, 0), (255, 0, 150)]

# Rozmiary kontenerów
CONTAINER_WIDTH = 100
CONTAINER_HEIGHT = 100

# Rozmiary śmieci
TRASH_WIDTH = 30
TRASH_HEIGHT = 30

# Klasa reprezentująca kontener
class Container(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((CONTAINER_WIDTH, CONTAINER_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Klasa reprezentująca śmieci
class Trash(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TRASH_WIDTH, TRASH_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False  # Flaga określająca, czy śmieć jest przeciągany

# Grupa sprite'ów
containers_group = pygame.sprite.Group()
trash_group = pygame.sprite.Group()

show_menu_and_start_game()  # Wyświetl menu i rozpocznij grę

# Ustawienia licznika czasu
start_time = 0
elapsed_time = 0
game_running = True
end_time = 0  # Dodana zmienna end_time przed pętlą główną
game_completed = False  # Dodaj zmienną game_completed, aby śledzić, czy gra została ukończona

# Przygotowanie obiektu font przed pętlą gry
font = pygame.font.Font(None, 36)

# Pętla gry
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Sprawdzanie, czy kliknięto na któryś z elementów w grupie śmieci
            for trash in trash_group:
                if trash.rect.collidepoint(event.pos):
                    trash.dragging = True
                    trash.offset_x = event.pos[0] - trash.rect.x
                    trash.offset_y = event.pos[1] - trash.rect.y
        elif event.type == pygame.MOUSEBUTTONUP:
            # Zakończenie przeciągania śmieci
            for trash in trash_group:
                if trash.dragging:
                    trash.dragging = False
                    # Sprawdzenie, czy śmieć trafił do odpowiedniego kontenera
                    container_hit = pygame.sprite.spritecollideany(trash, containers_group)
                    if container_hit and trash.image.get_at((0, 0)) == container_hit.image.get_at((0, 0)):
                        trash_group.remove(trash)
                        if not trash_group:
                            end_time = pygame.time.get_ticks() - start_time
                            game_completed = True

    # Aktualizacja położenia przeciąganych śmieci
    for trash in trash_group:
        if trash.dragging:
            trash.rect.x = pygame.mouse.get_pos()[0] - trash.offset_x
            trash.rect.y = pygame.mouse.get_pos()[1] - trash.offset_y

    # Rysowanie
    screen.fill(WHITE)
    containers_group.draw(screen)
    trash_group.draw(screen)

    # Sprawdzenie, czy wszystkie śmieci zostały wyrzucone do odpowiednich kontenerów
    if not trash_group and game_running and game_completed:
        trash_group.remove(trash)
        containers_group.remove(containers_group)

        # Dodaj komunikat "Gratulacje! Twój czas to: [czas w sekundach]"
        congratulations_text = font.render(f"Gratulacje! Twój czas to: {end_time // 1000} s", True, (0, 0, 0))
        screen.blit(congratulations_text, (WIDTH // 2 - 200, HEIGHT // 2 - 30))

        # Dodaj przycisk "Powrót do menu głównego"
        return_to_menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(screen, (0, 255, 0), return_to_menu_button)
        return_to_menu_text = font.render("Powrót do menu głównego", True, (0, 0, 0))
        screen.blit(return_to_menu_text, (WIDTH // 2 - 150, HEIGHT // 2 + 65))

        # Sprawdź, czy kliknięto na przycisk "Powrót do menu głównego"
        if pygame.mouse.get_pressed()[0] and return_to_menu_button.collidepoint(pygame.mouse.get_pos()):
            # W przypadku kliknięcia przycisku, zresetuj zmienne gry i wyświetl menu
            game_completed = False
            show_menu_and_start_game()  # Wyświetl menu i zacznij grę od nowa
            start_time = pygame.time.get_ticks()  # Zresetuj licznik czasu

    # Aktualizacja ekranu
    pygame.display.flip()

    # Ustawienie liczby klatek na sekundę
    pygame.time.Clock().tick(FPS)
