import pygame
import sys

class PlayerAvatar:

    def __init__(self, screen_width, screen_height, num_players, selected_players):
        pygame.init()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Player Selection Menu")

        # Load player images and resize
        self.num_players = num_players
        self.player_filenames = [f"GameMain/pics/p{i}.png" for i in range(1, num_players + 1)]
        self.selected_players = selected_players
        self.player_images = [pygame.transform.scale(pygame.image.load(filename).convert(), (30, 45)) for filename in
                              self.player_filenames]

        # Set up font
        self.font = pygame.font.Font(None, 36)

        # Set up colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        # Set up player selection variables
        self.selected_player = 0
        self.selected_player_rect = pygame.Rect(50 - 5, self.screen_height // 2 - 50 - 5, 35, 50)

        # Player attribute to store the selected player avatar
        self.selected_player_avatar = None

    def choose_player(self):
        while True:
            self.screen.fill(self.white)

            # Display all player images
            for i, player_image in enumerate(self.player_images):
                x = i * 120 + 50
                y = self.screen_height // 2 - 50
                self.screen.blit(player_image, (x, y))

                # Draw a rectangle around the selected player if available
                if i == self.selected_player and self.player_filenames[i] not in self.selected_players:
                    pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(x - 5, y - 5, 35, 50), 3)

            # Display instructions
            instructions = self.font.render("Select a player (Use arrows, Press Enter to confirm):", True, self.black)
            self.screen.blit(instructions, (50, 30))

            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.selected_player = max(self.selected_player - 1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_player = min(self.selected_player + 1, len(self.player_images) - 1)
                    elif event.key == pygame.K_RETURN and self.player_filenames[self.selected_player] not in self.selected_players:
                        self.selected_player_avatar = self.player_filenames[self.selected_player]
                        return self.selected_player_avatar