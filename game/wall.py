import pygame as pg

from .interfaces import PlayInstance
from .utils import load_im, Vector2D, Rect


class Wall(PlayInstance):
    TEXTURE = load_im("wall.png", scale=64 / 60)
    WIDTH, HEIGHT = TEXTURE.get_size()

    def __init__(self, rect: pg.Rect) -> None:
        self.pg_rect = rect
        self.surface = pg.Surface(rect.size)
        self.surface.fill((0, 0, 0))

        for x in range(0, rect.width, Wall.WIDTH):
            for y in range(0, rect.height, Wall.HEIGHT):
                self.surface.blit(Wall.TEXTURE, (x, y))

    def get_rect(self) -> "Rect":
        return Rect.from_pygame(self.pg_rect)

    def get_velocity(self) -> "Vector2D":
        return Vector2D(0, 0)

    def collide(self, other: "Colliable") -> bool:
        return other.get_rect().collide(self.get_rect())

    def render(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.pg_rect)

    def update(self, dt: float) -> None:
        """Wall does not move, so no need to update it."""
