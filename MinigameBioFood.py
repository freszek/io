import pygame
import random

pygame.init()

szerokosc, wysokosc = 640, 480
ekran = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption('Ekologiczny Snake')

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

gracz_obrazek = pygame.image.load('gracz.png')

rozmiar_segmentu = 40
gracz_obrazek = pygame.transform.scale(gracz_obrazek, (rozmiar_segmentu, rozmiar_segmentu))

gracz_pos = [szerokosc // 2 // rozmiar_segmentu * rozmiar_segmentu, wysokosc // 2 // rozmiar_segmentu * rozmiar_segmentu]

def losowa_pozycja(zabronione_pozycje):
    pozycja = None
    while pozycja is None or pozycja in zabronione_pozycje:
        pozycja = [random.randint(0, (szerokosc - rozmiar_segmentu) // rozmiar_segmentu) * rozmiar_segmentu,
                   random.randint(0, (wysokosc - rozmiar_segmentu) // rozmiar_segmentu) * rozmiar_segmentu]
    return pozycja


ekologiczne_pos = losowa_pozycja([gracz_pos])
ilosc_nieekologicznych = 5 
nieekologiczne_pozycje = [losowa_pozycja([gracz_pos, ekologiczne_pos]) for _ in range(ilosc_nieekologicznych)]

zdrowie = 1000
wynik = 0

zegar = pygame.time.Clock()
FPS = 15

dziala = True
while dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dziala = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                gracz_pos[0] -= rozmiar_segmentu
            elif event.key == pygame.K_RIGHT:
                gracz_pos[0] += rozmiar_segmentu
            elif event.key == pygame.K_UP:
                gracz_pos[1] -= rozmiar_segmentu
            elif event.key == pygame.K_DOWN:
                gracz_pos[1] += rozmiar_segmentu

    gracz_pos[0] %= szerokosc
    gracz_pos[1] %= wysokosc

    if gracz_pos == ekologiczne_pos:
        wynik += 1
        zdrowie += 30
        ekologiczne_pos = losowa_pozycja([gracz_pos] + nieekologiczne_pozycje)

    for i in range(ilosc_nieekologicznych):
        if gracz_pos == nieekologiczne_pozycje[i]:
            zdrowie -= 200
            nieekologiczne_pozycje[i] = losowa_pozycja([gracz_pos, ekologiczne_pos] + nieekologiczne_pozycje)

    ekran.fill(BLACK)
    pygame.draw.rect(ekran, GREEN, (*ekologiczne_pos, rozmiar_segmentu, rozmiar_segmentu))
    for pozycja in nieekologiczne_pozycje:
        pygame.draw.rect(ekran, RED, (*pozycja, rozmiar_segmentu, rozmiar_segmentu))
    #pygame.draw.rect(ekran, WHITE, (*gracz_pos, rozmiar_segmentu, rozmiar_segmentu))
    ekran.blit(gracz_obrazek, gracz_pos)

    zdrowie = max(0, zdrowie - 2)
    if zdrowie <= 0:
        print(f"Koniec gry! Twój wynik to: {wynik}")
        dziala = False

    zdrowie_tekst = pygame.font.SysFont("comicsansms", 20).render(f"Zdrowie: {zdrowie}", True, WHITE)
    ekran.blit(zdrowie_tekst, (10, 10))

    wynik_tekst = pygame.font.SysFont("comicsansms", 20).render(f"Wynik: {wynik}", True, WHITE)
    ekran.blit(wynik_tekst, (szerokosc - 110, 10))

    pygame.display.flip()

    zegar.tick(FPS)

pygame.quit()
