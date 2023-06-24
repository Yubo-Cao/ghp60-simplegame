from abc import abstractmethod
from collections.abc import Callable
from typing import NamedTuple, Protocol

import pygame as pg

from game.utils.ds import Vector2D

from .updatable import Updatable


class Colliable(Protocol):
    @abstractmethod
    def get_rect(self) -> pg.Rect:
        ...

    @abstractmethod
    def get_velocity(self) -> "Vector2D":
        ...

    @abstractmethod
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
        a: Colliable,
        b: Colliable,
    ):
        self.jumptable.setdefault(type(a), {}).setdefault(type(b), []).append(callback)

    def update(self, dt):
        collisions = []
        for a in self.collidables:
            for b in self.collidables:
                if a is not b and a.collide(b):
                    collisions.append(Collision(a, b))

        for collision in collisions:
            for callback in self.jumptable.get(type(collision.a), {}).get(
                type(collision.b), []
            ):
                callback(collision)

        self.callbacks.clear()
