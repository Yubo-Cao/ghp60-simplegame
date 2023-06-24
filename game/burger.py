import pygame as pg

from .interfaces import PlayInstance, Colliable, Renderable, Collision
from .physics import RigidBodyRect, handle_collision
from .utils import Rect, Vector2D, Number


class BurgerLayer(PlayInstance):
    def __init__(self, sprite: pg.Surface, name: str) -> None:
        self.sprite = sprite
        self.name = name

        self.pos = Vector2D[Number](0.0, 0.0)
        self.rect = Rect(self.pos.x, self.pos.y, sprite.get_width(), sprite.get_height())
        self.rb = RigidBodyRect(self.rect, gravity=True)

    def get_rect(self) -> Rect:
        return self.rect

    def get_velocity(self) -> "Vector2D":
        return self.rb.velocity

    def collide(self, other: Colliable) -> bool:
        return self.rect.collide(other.get_rect())

    def render(self, surface: pg.Surface) -> None:
        surface.blit(self.sprite, tuple(self.pos))

    def update(self, dt: float) -> None:
        self.rb.update(dt)

    def wall_collide(self, collision: Collision):
        handle_collision(collision, self.rb)

    def __repr__(self) -> str:
        return f"BurgerLayer({self.name})"


class BurgerClass(Renderable, Colliable):
    def __init__(self) -> None:
        self.rect = Rect(0, 0, 0, 0)
        # TODO: Connect with player
        self.velocity = Vector2D[Number](0.0, 0.0)
        self.layers: list[BurgerLayer] = []

    def move(self, pos: Vector2D[Number]) -> None:
        self.rect.x = pos.x
        self.rect.y = pos.y

    def get_rect(self) -> Rect:
        return self.rect

    def get_velocity(self) -> "Vector2D":
        return self.velocity

    def collide(self, other: "Colliable") -> bool:
        return self.rect.collide(other.get_rect())

    def render(self, surface: pg.Surface) -> None:
        for layer in self.layers:
            layer.render(surface)
