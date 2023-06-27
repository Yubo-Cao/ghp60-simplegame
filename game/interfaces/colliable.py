from abc import abstractmethod
from collections.abc import Callable
from typing import NamedTuple, Protocol, runtime_checkable

from game.utils import Rect, Vector2D

from .updatable import Updatable


class Collision(NamedTuple):
    a: "Colliable"
    b: "Colliable"


CollisionCallback = Callable[[Collision], None]


@runtime_checkable
class Colliable(Protocol):
    @abstractmethod
    def get_rect(self) -> Rect:
        ...

    @abstractmethod
    def get_velocity(self) -> "Vector2D":
        ...

    @abstractmethod
    def collide(self, other: "Colliable") -> bool:
        ...

    @abstractmethod
    def get_callbacks(self) -> list[tuple[CollisionCallback, type["Colliable"]]]:
        ...


class CollisionHandler(Updatable):
    def __init__(self) -> None:
        self.callbacks: list[CollisionCallback] = []
        self.collidables: list[Colliable] = []
        self.jumptable: list[tuple[Colliable, type[Colliable], CollisionCallback]] = []

    def add(self, colliable: Colliable):
        self.collidables.append(colliable)

    def remove(self, colliable: Colliable):
        self.collidables.remove(colliable)

    def register(
        self,
        callback: CollisionCallback,
        a: Colliable,
        b: type[Colliable],
    ):
        self.jumptable.append((a, b, callback))

    def unregister(
        self,
        callback: CollisionCallback,
        a: Colliable,
        b: type[Colliable],
    ):
        self.jumptable.remove((a, b, callback))

    def update(self, dt):
        collisions = []
        for a in self.collidables:
            for b in self.collidables:
                if a is not b and a.collide(b):
                    collisions.append(Collision(a, b))

        for collision in collisions:
            for a, b, callback in self.jumptable:
                if a == collision.a and isinstance(collision.b, b):
                    callback(collision)

        self.callbacks.clear()
