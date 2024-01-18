import pygame
import sys
import random
import os
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
    for i in range(3):
        for color in TRASH_COLORS:
            trash = Trash(color, random.randint(0, WIDTH - TRASH_WIDTH),
                          random.randint(0, HEIGHT - CONTAINER_HEIGHT - TRASH_HEIGHT - 5))
            trash_group.add(trash)


# Funkcja wyświetlająca menu
def show_menu_and_start_game():
    if not show_menu():
        pygame.quit()
        sys.exit()

    generate_game()


# Inicjalizacja Pygame
pygame.init()
max_score = 300
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
TRASH_COLORS = [(255, 0, 0), (50, 117, 38), (89, 111, 187), (246, 139, 25), (248, 201, 25)]

# Rozmiary kontenerów
CONTAINER_WIDTH = 100
CONTAINER_HEIGHT = 100

# Rozmiary śmieci
TRASH_WIDTH = 30
TRASH_HEIGHT = 30
IMAGE_DIRECTORY = "images"


# Klasa reprezentująca kontener

class Container(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Zamiast generowania powierzchni o określonym kolorze, użyj wczytanego obrazu
        self.image = self.load_container_image(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_container_image(self, color):
        # Generuj ścieżkę do pliku obrazu kontenera na podstawie koloru
        image_path = os.path.join(IMAGE_DIRECTORY, f"container_{color[0]}_{color[1]}_{color[2]}.png")
        # Wczytaj obraz
        image = pygame.image.load(image_path).convert_alpha()
        # Dostosuj rozmiar obrazu do rozmiaru kontenera
        return pygame.transform.scale(image, (CONTAINER_WIDTH, CONTAINER_HEIGHT))


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
                    if container_hit is not None:
                        if containers_group.sprites().index(container_hit) == 0:  # Dla pierwszego kontenera
                            container_color = (255, 0, 0)  # Kolor czerwony
                        else:
                            container_color = container_hit.image.get_at(
                                (container_hit.image.get_width() // 2, container_hit.image.get_height() // 2))[:-1]

                        trash_color = trash.image.get_at((trash.image.get_width() // 2, trash.image.get_height() // 2))[
                                      :-1]
                        print("Trash color:", trash_color)
                        print("Container color:", container_color)

                        if trash_color == container_color:
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
        normalized_score = max(0, max_score - (end_time * 10 // 1000))
        # Dodaj komunikat "Gratulacje! Twój czas to: [czas w sekundach]"
        congratulations_text = font.render(f"Gratulacje! Twój czas to: {end_time // 1000} s", True, (0, 0, 0))
        congratulations_rect = congratulations_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        screen.blit(congratulations_text, congratulations_rect.topleft)

        # Dodaj znormalizowany wynik
        score_text = font.render(f"Twój wynik: {normalized_score} pkt", True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(score_text, score_rect.topleft)

        # Dodaj przycisk "Powrót do menu głównego"
        return_to_menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(screen, (144, 238, 144), return_to_menu_button.inflate(130, 15),
                         border_radius=10)
        return_to_menu_text = font.render("Powrót do menu głównego", True, (0, 0, 0))
        return_to_menu_rect = return_to_menu_text.get_rect(center=return_to_menu_button.center)
        screen.blit(return_to_menu_text, return_to_menu_rect.topleft)

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
