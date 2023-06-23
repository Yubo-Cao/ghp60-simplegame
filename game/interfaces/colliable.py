from collections.abc import Callable
from typing import NamedTuple, Protocol

from . import pg
from .updatable import Updatable


class Colliable(Protocol):
    def get_rect(self) -> pg.Rect:
        ...

    def collide(self, other: "Colliable") -> bool:
        ...


class Collision(NamedTuple):
    a: Colliable
    b: Colliable


CollisionCallback = Callable[[Collision], None]


class CollisionHandler(Updatable):
    def __init__(self):
        self.callbacks: list[CollisionCallback] = []
        self.collidables: list[Colliable] = []
        self.jumptable: dict[
            type[Colliable], dict[type[Colliable], list[CollisionCallback]]
        ] = {}

    def add(self, colliable: Colliable):
        self.collidables.append(colliable)

    def remove(self, colliable: Colliable):
        self.collidables.remove(colliable)

    def register(
        self,
        callback: CollisionCallback,
        a: type[Colliable],
        b: type[Colliable],
    ):
        self.jumptable.setdefault(a, {}).setdefault(b, []).append(callback)

    def update(self, dt):
        collisions = []
        for a in self.collidables:
            for b in self.collidables:
                if a is not b and a.collide(b):
                    collisions.append(Collision(a, b))

        for collision in collisions:
            for callback in self.jumptable[type(collision.a)][type(collision.b)]:
                callback(collision)

        self.callbacks.clear()
