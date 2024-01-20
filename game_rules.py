import pygame

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class ScrollableText:
    def __init__(self, text, x, y, width, height, font_size, color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, self.font_size)
        self.render_text()

    def render_text(self):
        lines = [self.text[i:i + 40] for i in range(0, len(self.text), 40)]
        self.rendered_text = [self.font.render(line, True, self.color) for line in lines]

    def draw(self, screen):
        for i, line in enumerate(self.rendered_text):
            screen.blit(line, (self.x, self.y + i * self.font_size))

class ScrollButton:
    def __init__(self, x, y, width, height, color, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

class GameRules:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Green Game")
        self.clock = pygame.time.Clock()
        self.scroll_up_button = ScrollButton(1050, 50, 50, 30, WHITE, "Up", self.scroll_up)
        self.scroll_down_button = ScrollButton(1050, HEIGHT - 50, 50, 30, WHITE, "Down", self.scroll_down)
        self.rules, self.authors = self.load_rules_from_file()
        self.scroll_y_rules = 0
        self.scroll_y_authors = 0

    def load_rules_from_file(self):
        rules = []
        authors = []
        with open("game_rules.txt", "r", encoding="utf-8") as file:
            section = None
            for line in file:
                line = line.strip()
                if line == "Game Rules:":
                    section = "rules"
                elif line == "Authors:":
                    section = "authors"
                elif section == "rules":
                    rules.append(line)
                elif section == "authors":
                    authors.append(line)
        return rules, authors

    def display_rules(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Game Rules:", True, WHITE)
        self.screen.blit(text, (50, 50 + self.scroll_y_rules))

        for i, rule in enumerate(self.rules):
            rule_text = font.render(f"{rule}", True, WHITE)
            self.screen.blit(rule_text, (50, 100 + i * 30 + self.scroll_y_rules))

    def display_authors(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Authors:", True, WHITE)
        self.screen.blit(text, (50, 450 + self.scroll_y_authors))

        for i, author in enumerate(self.authors):
            author_text = font.render(f"{i + 1}. {author}", True, WHITE)
            self.screen.blit(author_text, (50, 500 + i * 30 + self.scroll_y_authors))

    def scroll_up(self):
        self.scroll_y_rules = max(self.scroll_y_rules - 30, 0)
        self.scroll_y_authors = max(self.scroll_y_authors - 30, 0)

    def scroll_down(self):
        max_scroll_rules = len(self.rules) * 30 - HEIGHT + 200
        max_scroll_authors = len(self.authors) * 30 - HEIGHT + 200
        self.scroll_y_rules = min(self.scroll_y_rules + 30, max_scroll_rules)
        self.scroll_y_authors = min(self.scroll_y_authors + 30, max_scroll_authors)


class GameRulesApp:
    def run(self):
        game_rules = GameRules()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
                game_rules.scroll_up_button.handle_event(event)
                game_rules.scroll_down_button.handle_event(event)

            game_rules.screen.fill(BLACK)
            game_rules.display_rules()
            game_rules.display_authors()
            game_rules.scroll_up_button.draw(game_rules.screen)
            game_rules.scroll_down_button.draw(game_rules.screen)

            pygame.display.flip()
            game_rules.clock.tick(FPS)


if __name__ == "__main__":
    app = GameRulesApp()
    app.run()
