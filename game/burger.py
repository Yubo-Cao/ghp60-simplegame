from contextlib import suppress
from functools import partial

import pygame as pg

from game.interfaces.colliable import Colliable, CollisionCallback

from .command import RemoveInstanceCMD, issue_command, RemoveCallbackCMD
from .interfaces import (
    Colliable,
    Collision,
    CollisionCallback,
    PlayInstance,
    Renderable,
)
from .physics import RigidBodyRect, handle_collision
from .utils import DATA_DIR, Number, Rect, Vector2D, load_im
from .wall import Wall


class BurgerLayer(PlayInstance):
    def __init__(self, sprite: pg.Surface, name: str) -> None:
        self.sprite = sprite
        self.name = name
        self.width = sprite.get_width()
        self.height = sprite.get_height()
        self.rb = RigidBodyRect(
            Rect(0, 0, self.width, self.height),
            mass=4,
            gravity=True,
        )

    @property
    def pos(self) -> Vector2D[Number]:
        return self.rb.position

    @pos.setter
    def pos(self, value: Vector2D[Number]) -> None:
        self.rb.position = value

    def get_rect(self) -> Rect:
        return self.rb.rect

    def get_velocity(self) -> "Vector2D":
        return self.rb.velocity

    def collide(self, other: Colliable) -> bool:
        return self.rb.collide(other)

    def render(self, surface: pg.Surface) -> None:
        surface.blit(self.sprite, tuple(self.pos))
        self.rb.render(surface)

    def update(self, dt: float) -> None:
        self.rb.update(dt)

    def wall_collide(self, collision: Collision):
        with suppress(Exception):  # TODO: fix this
            handle_collision(collision, self.rb)
        issue_command(RemoveInstanceCMD(self))

    def __repr__(self) -> str:
        return f"BurgerLayer({self.name})"

    def __eq__(self, o: object) -> bool:
        return id(self) == id(o)

    def get_callbacks(self) -> list[tuple[CollisionCallback, type[Colliable]]]:
        return [(self.wall_collide, Wall)]


LAYERS = [
    partial(BurgerLayer, load_im(path), path.stem)
    for path in (DATA_DIR / "burger_layers").glob("*.png")
]


class Burger(Renderable, Colliable):
    def __init__(self) -> None:
        self.rect = Rect(0, 0, 0, 0)
        self.velocity = Vector2D[Number](0.0, 0.0)
        self.layers: list[BurgerLayer] = []

    def move_to(self, pos: Vector2D[Number]) -> None:
        self.rect = Rect(
            pos.x,
            pos.y,
            self.rect.w,
            self.rect.h,
        )
        self.__arrange_layers(pos.x, pos.y)

    def add_layer(self, layer: BurgerLayer) -> None:
        if layer in self.layers:
            return
        layer.rb.gravity = False
        self.layers.append(layer)
        issue_command(RemoveCallbackCMD(layer.wall_collide, layer, Wall))
        self.__arrange_layers(self.rect.x, self.rect.y)

    def get_rect(self) -> Rect:
        return self.rect

    def get_velocity(self) -> "Vector2D":
        return self.velocity

    def collide(self, other: "Colliable") -> bool:
        return self.rect.collide(other.get_rect())

    def render(self, surface: pg.Surface) -> None:
        for layer in self.layers:
            layer.render(surface)

    def __arrange_layers(self, x: Number, y: Number) -> None:
        h = 0
        for layer in self.layers:
            layer.pos = Vector2D[Number](x, y - h)
            h += layer.sprite.get_height()
        self.rect = Rect(x, y - h, self.rect.w, h)

    def layer_collide(self, collision: Collision) -> None:
        assert isinstance(collision.b, BurgerLayer)
        self.add_layer(collision.b)

    def get_callbacks(self) -> list[tuple[CollisionCallback, type["Colliable"]]]:
        return [
            (self.layer_collide, BurgerLayer),
        ]
