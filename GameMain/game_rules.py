import pygame
import sys

class GameRules:
    def __init__(self, text, window_width=800, window_height=600):
        self.text = text
        self.window_width = window_width
        self.window_height = window_height

        self.font = pygame.font.Font(None, 28)
        self.text_lines = self.text.split('\n')
        self.text_height = len(self.text_lines) * 30  # assuming each line height is 30 pixels

        self.scrollbar_width = 20
        self.scroll_position = 0

        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Text Scrollable Scene")

    def draw(self):
        self.window.fill((0, 255, 0))  # Green background

        # Draw text with padding
        for i, line in enumerate(self.text_lines):
            text_surface = self.font.render(line, True, (0, 0, 0))
            self.window.blit(text_surface, (20, 20 + i * 30 - self.scroll_position))

        # Draw scrollbar
        pygame.draw.rect(self.window, (200, 200, 200),
                         (self.window_width - self.scrollbar_width, 0, self.scrollbar_width, self.window_height))
        scrollbar_height = self.window_height * self.window_height / self.text_height
        pygame.draw.rect(self.window, (100, 100, 100),
                         (self.window_width - self.scrollbar_width, self.scroll_position * self.window_height / self.text_height,
                          self.scrollbar_width, scrollbar_height))

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.scroll_position += 10
            elif keys[pygame.K_UP]:
                self.scroll_position -= 10

            self.scroll_position = max(0, min(self.scroll_position, self.text_height - self.window_height))

            self.draw()
            clock.tick(30)

text = """Game Rules:
1. Poruszasz się po planszy głównej i rzucasz kostką.
2. Wyzwania w minigrach pomogą ci zdobywać punkty.
3. Na oznaczonych polach możesz wziąć udział w Specjalnych Eventach.
4. Rywalizujesz z innymi graczami.
5. Codziennie masz jeden rzut i jedną minigrę.
6. Wybierasz jednego spośród sześciu pionków jako avatara.
7. Uczysz się dbać o środowisko.
8. Uczysz się ekologii.
9. Pamiętaj aby codziennie zagrać, to ważne do punktacji końcowej.
10. Zaproś znajomych.
11. Miłej zabawy !!

Authors:
Adam Kloc
Artur Gluba
Hubert Kłosowski
Kacper Janowicz
Kamil Małecki
Krzysztof Kolanek
Jakub Garus
Jakub Tomaszewski
Martyna Brzezowska
Michał Bukowski
Oskar Baranowski
Stanisław Kowalczyk
                    """
def display_rules():
    # showing game rules
    scene = GameRules(text)
    scene.run()
