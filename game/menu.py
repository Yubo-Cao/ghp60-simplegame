import pygame as pg

from .utils import HAlign, VAlign, text


class MainMenu:
    def __init__(self, surface, play_fn):
        self.surface = surface
        self.screen_width, self.screen_height = self.surface.get_size()
        self.cx, self.cy = self.screen_width // 2, self.screen_height // 2

        pg.display.set_caption("Catch Game")
        self.play_fn = play_fn

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # Load background image
        # self.background_image = pygame.image.load("Burger.jpg")
        # self.background_image = pygame.transform.scale(
        #     self.background_image, (self.screen_width, self.screen_height)
        # )

        # Load font
        self.font = pg.font.Font(None, 50)

    def loop(self):
        while True:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        exit()
                    elif event.key == pg.K_p:
                        self.play_fn()  # Start the game
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.cx - 100 <= x <= self.cx + 100 and 250 <= y <= 300:
                        self.play_fn()
                    elif self.cx - 100 <= x <= self.cx + 100 and 350 <= y <= 400:
                        exit()

            self.surface.fill(self.WHITE)

            # Draw the menu options
            play_rect = pg.Rect(self.cx - 100, 250, 200, 50)
            quit_rect = pg.Rect(self.cx - 100, 350, 200, 50)
            pg.draw.rect(self.surface, self.BLACK, play_rect)
            pg.draw.rect(self.surface, self.BLACK, quit_rect)

            text(
                self.surface,
                "Play",
                (self.cx, 260),
                halign=HAlign.CENTER,
                valign=VAlign.CENTER,
            )
            text(
                self.surface,
                "Quit",
                (self.cx, 360),
                halign=HAlign.CENTER,
                valign=VAlign.CENTER,
            )

            # Update the display
            pg.display.update()
