import pygame as pg

from .interfaces import Colliable, CollisionCallback, PlayInstance
from .utils import Rect, Vector2D, load_im


class Wall(PlayInstance):
    TEXTURE = load_im("wall.jpg", scale=48 / 60)
    WIDTH, HEIGHT = TEXTURE.get_size()

    def __init__(self, rect: pg.Rect, sticy: bool = False) -> None:
        self.pg_rect = rect
        self.surface = pg.Surface(rect.size)
        self.surface.fill((0, 0, 0))
        self.sticky = sticy

        for x in range(0, rect.width, Wall.WIDTH):
            for y in range(0, rect.height, Wall.HEIGHT):
                self.surface.blit(Wall.TEXTURE, (x, y))

    def get_rect(self) -> Rect:
        return Rect.from_pygame(self.pg_rect)

    def get_velocity(self) -> Vector2D:
        return Vector2D(0, 0)

    def collide(self, other: Colliable) -> bool:
        return other.get_rect().collide(self.get_rect())

    def get_callbacks(self) -> list[tuple[CollisionCallback, type[Colliable]]]:
        return []

    def render(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.pg_rect)
        if self.sticky:
            pg.draw.rect(
                surface,
                (0, 255, 0),
                (self.pg_rect.x, self.pg_rect.y, 2, self.pg_rect.height),
            )
            pg.draw.rect(
                surface,
                (0, 255, 0),
                (
                    self.pg_rect.x + self.pg_rect.width - 2,
                    self.pg_rect.y,
                    2,
                    self.pg_rect.height,
                ),
            )

    def update(self, dt: float) -> None:
        """Wall does not move, so no need to update it."""
