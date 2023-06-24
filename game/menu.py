import pygame
from collections.abc import Callable


class MainMenu:
    def __init__(self, width: int, height: int, play_fn: Callable) -> None:
        self.screen_width, self.screen_height = width, height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.cx, self.cy = self.screen_width // 2, self.screen_height // 2
        pygame.display.set_caption("Main Menu")

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # # Load background image
        # self.background_image = pygame.image.load("AnotherWing111621.png")
        # self.background_image = pygame.transform.scale(
        #     self.background_image, (self.screen_width, self.screen_height)
        # )

        # Load font
        self.font = pygame.font.Font(None, 48)
        self.play_fn = play_fn

    def main_menu(self):
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_p:  # 'p' key to play
                        self.play_fn()  # Start the game
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (
                        self.cx - 100 <= event.pos[0] <= self.cx + 100
                        and 250 <= event.pos[1] <= 300
                    ):
                        self.play_fn()  # Start the game
                    elif (
                        self.cx - 100 <= event.pos[0] <= self.cx + 100
                        and 350 <= event.pos[1] <= 400
                    ):
                        pygame.quit()
                        exit()

            # Draw the background image
            self.screen.fill(self.WHITE)

            # Draw the menu options
            play_text = self.font.render("Play", True, self.WHITE)
            quit_text = self.font.render("Quit", True, self.WHITE)

            play_rect = pygame.Rect(self.cx - 100, 250, 200, 50)
            quit_rect = pygame.Rect(self.cx - 100, 350, 200, 50)

            pygame.draw.rect(self.screen, self.BLACK, play_rect)
            pygame.draw.rect(self.screen, self.BLACK, quit_rect)

            self.screen.blit(play_text, (self.cx - 45, 260))
            self.screen.blit(quit_text, (self.cx - 45, 360))

            # Update the display
            pygame.display.update()
