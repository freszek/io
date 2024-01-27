import pygame
import random
import sys


class EkologicznySnake:
    def __init__(self, width=1200, height=800, duration=30):
        pygame.init()
        self.szerokosc = width
        self.wysokosc = height

        self.ekran = pygame.display.set_mode((self.szerokosc, self.wysokosc))
        pygame.display.set_caption('Ekologiczny Snake')

        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)

        self.rozmiar_segmentu = 40
        self.gracz_obrazek = pygame.image.load('Minigames/BioFoodGame/pics_game/gracz.png')
        self.gracz_obrazek = pygame.transform.scale(self.gracz_obrazek, (self.rozmiar_segmentu, self.rozmiar_segmentu))

        self.gracz_pos = [self.szerokosc // 2 // self.rozmiar_segmentu * self.rozmiar_segmentu,
                          self.wysokosc // 2 // self.rozmiar_segmentu * self.rozmiar_segmentu]

        self.frytki_obrazek = pygame.image.load('Minigames/BioFoodGame/pics_game/fryty.png')
        self.frytki_obrazek = pygame.transform.scale(self.frytki_obrazek,
                                                     (self.rozmiar_segmentu, self.rozmiar_segmentu))

        self.jablko_obrazek = pygame.image.load('Minigames/BioFoodGame/pics_game/japko.png')
        self.jablko_obrazek = pygame.transform.scale(self.jablko_obrazek,
                                                     (self.rozmiar_segmentu, self.rozmiar_segmentu))

        self.ekologiczne_pos = self.losowa_pozycja([self.gracz_pos])
        self.ilosc_nieekologicznych = 50
        self.nieekologiczne_pozycje = [self.losowa_pozycja([self.gracz_pos, self.ekologiczne_pos])
                                       for _ in range(self.ilosc_nieekologicznych)]

        self.zdrowie = 1000
        self.wynik = 0

        self.zegar = pygame.time.Clock()
        self.FPS = 15

    def losowa_pozycja(self, zabronione_pozycje):
        pozycja = None
        while pozycja is None or pozycja in zabronione_pozycje:
            pozycja = [random.randint(0, (self.szerokosc - self.rozmiar_segmentu) // self.rozmiar_segmentu) *
                       self.rozmiar_segmentu,
                       random.randint(0, (self.wysokosc - self.rozmiar_segmentu) // self.rozmiar_segmentu) *
                       self.rozmiar_segmentu]
        return pozycja

    def rysuj_ekran(self):
        self.ekran.fill(self.BLACK)

        for pozycja in self.nieekologiczne_pozycje:
            self.ekran.blit(self.frytki_obrazek, (*pozycja, self.rozmiar_segmentu, self.rozmiar_segmentu))

        self.ekran.blit(self.jablko_obrazek, (*self.ekologiczne_pos, self.rozmiar_segmentu, self.rozmiar_segmentu))

        self.ekran.blit(self.gracz_obrazek, self.gracz_pos)

        self.zdrowie = max(0, self.zdrowie - 2)
        zdrowie_tekst = pygame.font.SysFont("comicsansms", 20).render(f"Zdrowie: {self.zdrowie}", True, self.WHITE)
        self.ekran.blit(zdrowie_tekst, (10, 10))

        wynik_tekst = pygame.font.SysFont("comicsansms", 20).render(f"Wynik: {self.wynik}", True, self.WHITE)
        self.ekran.blit(wynik_tekst, (self.szerokosc - 110, 10))

        pygame.display.flip()

    def ekran_startowy(self):
        self.ekran.fill(self.WHITE)
        font = pygame.font.SysFont("comicsansms", 30)
        naglowek = font.render("Zdrowe odżywianie", True, self.BLACK)
        naglowek_rect = naglowek.get_rect(center=(self.szerokosc // 2, self.wysokosc // 4))

        zasady_gry = [
            "Zasady gry:",
            "1. Sterowanie za pomocą strzałek.",
            "2. Jedz ekologiczne jedzenie (zielone) aby zdobywać punkty i regenerować zdrowie.",
            "3. Unikaj nieekologicznego jedzenia (czerwone), które obniża zdrowie.",
            "4. Gra kończy się, gdy zdrowie spadnie do zera lub gracz uzyska 100 punktów.",
            "5. Możesz przechodzić przez ściany"
            "",
            "Naciśnij dowolny klawisz, aby rozpocząć grę."
        ]

        linie_tekstu = []
        for linia in zasady_gry:
            linie_tekstu.append(font.render(linia, True, self.BLACK))

        self.ekran.blit(naglowek, naglowek_rect)

        y = self.wysokosc // 2
        for linia in linie_tekstu:
            linia_rect = linia.get_rect(center=(self.szerokosc // 2, y))
            self.ekran.blit(linia, linia_rect)
            y += 40

        pygame.display.flip()

        czekaj_na_start = True
        while czekaj_na_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    czekaj_na_start = False

    def run_game(self):
        self.ekran_startowy()

        dziala = True
        while dziala:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    dziala = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.gracz_pos[0] -= self.rozmiar_segmentu
                    elif event.key == pygame.K_RIGHT:
                        self.gracz_pos[0] += self.rozmiar_segmentu
                    elif event.key == pygame.K_UP:
                        self.gracz_pos[1] -= self.rozmiar_segmentu
                    elif event.key == pygame.K_DOWN:
                        self.gracz_pos[1] += self.rozmiar_segmentu

            self.gracz_pos[0] %= self.szerokosc
            self.gracz_pos[1] %= self.wysokosc

            if self.gracz_pos == self.ekologiczne_pos:
                self.wynik += 5
                self.zdrowie += 30
                self.ekologiczne_pos = self.losowa_pozycja([self.gracz_pos] + self.nieekologiczne_pozycje)

            for i in range(self.ilosc_nieekologicznych):
                if self.gracz_pos == self.nieekologiczne_pozycje[i]:
                    self.zdrowie -= 200
                    self.nieekologiczne_pozycje[i] = self.losowa_pozycja([self.gracz_pos, self.ekologiczne_pos] +
                                                                         self.nieekologiczne_pozycje)

            self.rysuj_ekran()

            if self.zdrowie <= 0 or self.wynik == 100:
                self.koniec_gry()

            self.zegar.tick(self.FPS)

        pygame.quit()

    def koniec_gry(self):
        self.ekran.fill(self.WHITE)
        font = pygame.font.SysFont("comicsansms", 50)
        tekst = font.render(f"Koniec gry! Twój wynik to: {self.wynik}", True, self.BLACK)
        tekst_rect = tekst.get_rect(center=(self.szerokosc // 2, self.wysokosc // 2))
        self.ekran.blit(tekst, tekst_rect)
        pygame.display.flip()

        czekaj = True
        while czekaj:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    czekaj = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    czekaj = False
        pygame.quit()
        sys.exit()
