import sys

import pygame


class MainMenu:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the window
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Main Menu")

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # Load background image
        self.background_image = pygame.image.load("AnotherWing111621.png")
        self.background_image = pygame.transform.scale(
            self.background_image, (self.screen_width, self.screen_height)
        )

        # Load font
        self.font = pygame.font.Font(None, 50)

    def main_menu(self):
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_p:  # 'p' key to play
                        # Call the game screen
                        self.play_game()  # Start the game
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 300 <= event.pos[0] <= 500 and 250 <= event.pos[1] <= 300:
                        # Call the game screen
                        self.play_game()  # Start the game
                    elif 300 <= event.pos[0] <= 500 and 350 <= event.pos[1] <= 400:
                        pygame.quit()
                        sys.exit()

            # Draw the background image
            self.screen.blit(self.background_image, (0, 0))

            # Draw the menu options
            play_text = self.font.render("Play", True, self.WHITE)
            quit_text = self.font.render("Quit", True, self.WHITE)

            play_rect = pygame.Rect(300, 250, 200, 50)
            quit_rect = pygame.Rect(300, 350, 200, 50)

            pygame.draw.rect(self.screen, self.BLACK, play_rect)
            pygame.draw.rect(self.screen, self.BLACK, quit_rect)

            self.screen.blit(play_text, (355, 260))
            self.screen.blit(quit_text, (355, 360))

            # Update the display
            pygame.display.update()

    def play_game(self):
        # This method represents the game screen
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # THIS LINE SHOULD SWITCH SCREEN TO THE GAME - SORT OF LIKE AN ACTIVATION
            self.screen.fill(self.BLACK)

            # Update the display
            pygame.display.update()


if __name__ == "__main__":
    menu = MainMenu()
    menu.main_menu()
