import pygame
import sys


class end_screen:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.cx, self.cy = self.screen_width // 2, self.screen_height // 2

        # Set up the window
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.font = pygame.font.Font(None, 50)

    def success_end_screen(self):
        while True:
            for event in pygame.event.get():
                play_rect = pygame.Rect(self.cx - 100, 250, 200, 50)

                self.screen.blit(play_text, (self.cx - 45, 260))

                # Draw the menu options
                play_text = self.font.render("SCORE: f{score}", True, self.WHITE)

                play_rect = pygame.Rect(300, 250, 200, 50)

                pygame.draw.rect(self.screen, self.BLACK, play_rect)

                self.screen.blit(play_text, (355, 260))

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def failure_end_screen(self):
        while True:
            for event in pygame.event.get():
                play_rect = pygame.Rect(self.cx - 100, 250, 200, 50)

                self.screen.blit(play_text, (self.cx - 45, 260))

                # Draw the menu options
                play_text = self.font.render("FAILURE", True, self.WHITE)

                play_rect = pygame.Rect(300, 250, 200, 50)

                pygame.draw.rect(self.screen, self.BLACK, play_rect)

                self.screen.blit(play_text, (355, 260))

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
