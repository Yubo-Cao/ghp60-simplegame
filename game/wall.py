import pygame as pg

from .interfaces import PlayInstance
from .utils import load_im


class Wall(PlayInstance):
    TEXTURE = load_im("wall.png")
    WIDTH, HEIGHT = TEXTURE.get_size()

    def __init__(self, rect: pg.Rect) -> None:
        self.rect = rect
        self.surface = pg.Surface(rect.size)
        self.surface.fill((0, 0, 0))

        for x in range(0, rect.width, Wall.WIDTH):
            for y in range(0, rect.height, Wall.HEIGHT):
                self.surface.blit(Wall.TEXTURE, (x, y))

    def get_rect(self) -> pg.Rect:
        return self.rect

    def collide(self, other: "Colliable") -> bool:
        return other.get_rect().colliderect(self.get_rect())

    def render(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.get_rect().topleft)

    def update(self, dt: float) -> None:
        """Wall does not move, so no need to update it."""
