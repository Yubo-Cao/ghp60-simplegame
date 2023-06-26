import pygame as pg

from .constants import ICON
from .utils import HAlign, VAlign, text


class EndScreen:
    def __init__(self, surface: pg.Surface, title: str, score: int, message: str):
        self.surface = surface
        self.screen_width, self.screen_height = self.surface.get_size()
        self.cx, self.cy = self.screen_width // 2, self.screen_height // 2
        self.title = title
        self.score = score
        self.message = message

    def loop(self):
        while True:
            self.surface.fill((0, 0, 0))
            w, h = ICON.get_size()
            self.surface.blit(ICON, (self.cx - w // 2, self.cy - h))
            text(
                self.surface,
                self.title,
                (self.cx, self.cy),
                100,
                halign=HAlign.CENTER,
                valign=VAlign.CENTER,
            )
            text(
                self.surface,
                f"Score: {self.score}",
                (self.cx, self.cy + 100),
                50,
                halign=HAlign.CENTER,
                valign=VAlign.CENTER,
            )
            text(
                self.surface,
                self.message,
                (self.cx, self.cy + 200),
                24,
                halign=HAlign.CENTER,
                valign=VAlign.CENTER,
            )
            self.__handle_exit()
            pg.display.update()

    def __handle_exit(self):
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                pg.quit()
                exit()
            elif evt.type == pg.KEYDOWN:
                if evt.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()
