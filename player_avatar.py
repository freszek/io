import pygame
import sys

class PlayerAvatar:
    def __init__(self, screen_width, screen_height, num_players):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Player Selection Menu")

        # Load player images and resize
        self.num_players = num_players
        self.player_filenames = [f"pics/p{i}.png" for i in range(1, num_players + 1)]
        self.player_images = [pygame.transform.scale(pygame.image.load(filename).convert(), (25, 40)) for filename in
                              self.player_filenames]

        # Set up font
        self.font = pygame.font.Font(None, 36)

        # Set up colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        # Set up player selection variables
        self.selected_player = 0
        self.selected_player_rect = pygame.Rect(50 - 5, self.screen_height // 2 - 50 - 5, 35, 50)

        # Player attribute to store selected player avatar
        self.selected_player_avatar = None

    def choose_player(self):
        while True:
            self.screen.fill(self.white)

            # Display player images
            for i, player_image in enumerate(self.player_images):
                x = i * 140 + 50
                y = self.screen_height // 2 - 50
                self.screen.blit(player_image, (x, y))

            # Draw a rectangle around the selected player
            pygame.draw.rect(self.screen, (255, 0, 0), self.selected_player_rect, 3)

            # Display instructions
            instructions = self.font.render("Select a player (Use arrays, Press Enter to confirm):", True, self.black)
            self.screen.blit(instructions, (50, 30))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.selected_player = max(self.selected_player - 1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_player = min(self.selected_player + 1, self.num_players - 1)
                    elif event.key == pygame.K_RETURN:
                        self.selected_player_avatar = self.player_filenames[self.selected_player]
                        return self.selected_player_avatar

            # Update the position of the rectangle based on the selected player
            self.selected_player_rect.x = self.selected_player * 140 + 50

            pygame.display.flip()

    def getPlayerID(self):
        pass

    def addPoints(self):
        pass
