from typing import Generic, TypeVar, overload

import pygame as pg

Number = float
E = TypeVar("E", bound=Number)


class Vector2D(Generic[E]):
    def __init__(self, x: Number, y: Number) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: "Vector2D[E]") -> "Vector2D[E]":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D[E]") -> "Vector2D[E]":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: E | "Vector2D[E]") -> "Vector2D[E]":
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        return Vector2D(self.x * other, self.y * other)

    def __matmul__(self, other: "Vector2D[E]") -> E:
        return self.x * other.x + self.y * other.y  # type: ignore

    def dot(self, other: "Vector2D[E]") -> E:
        return self @ other

    def __abs__(self) -> E:
        return (self.x**2 + self.y**2) ** 0.5

    def __neg__(self) -> "Vector2D[E]":
        return Vector2D(-self.x, -self.y)

    def __repr__(self) -> str:
        return f"<{self.x}, {self.y}>"

    def __len__(self) -> int:
        return 2

    def __getitem__(self, index: int) -> E:
        return (self.x, self.y)[index]  # type: ignore

    def __iter__(self):
        yield self.x
        yield self.y

    def reflect(self, other: "Vector2D[E]") -> "Vector2D[E]":
        x1, y1 = self
        x2, y2 = other

        if x2 == 0:
            slope = float("inf")
            y_intercept = float("inf")
        else:
            slope = y2 / x2
            y_intercept = y1 - slope * x1

        if slope == 0:
            reflected_vector = (x1, -y1)
        elif slope == float("inf"):
            reflected_vector = (-x1, y1)
        else:
            reflected_x = (x1 - slope * (y1 - y_intercept)) / (slope**2 + 1)
            reflected_y = slope * reflected_x + y_intercept
            reflected_vector = (2 * reflected_x - x1, 2 * reflected_y - y1)

        return Vector2D(*reflected_vector)

    def draw_point(self, surface: pg.Surface, color: tuple[int, int, int]) -> None:
        pg.draw.circle(surface, color, (int(self.x), int(self.y)), 5)

    def draw(
        self,
        surface: pg.Surface,
        pos: "Vector2D[E]",
        color: tuple[int, int, int],
    ) -> None:
        pg.draw.line(
            surface,
            color,
            (int(pos.x), int(pos.y)),
            (int(pos.x + self.x), int(pos.y + self.y)),
        )
        pos.draw_point(surface, color)

    def __eq__(self, other: "Vector2D[E]") -> bool:
        return self.x == other.x and self.y == other.y


class Rect:
    def __init__(self, x: Number, y: Number, w: Number, h: Number) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def width(self) -> Number:
        return self.w

    @property
    def height(self) -> Number:
        return self.h

    @property
    def center(self) -> Vector2D:
        return Vector2D(self.x + self.w / 2, self.y + self.h / 2)

    @property
    def centerx(self) -> Number:
        return self.x + self.w / 2

    @property
    def centery(self) -> Number:
        return self.y + self.h / 2

    @property
    def left(self) -> Number:
        return self.x

    @property
    def right(self) -> Number:
        return self.x + self.w

    @property
    def top(self) -> Number:
        return self.y

    @property
    def bottom(self) -> Number:
        return self.y + self.h

    def collide(self, other: "Rect") -> bool:
        return (
            self.x < other.x + other.w
            and self.x + self.w > other.x
            and self.y < other.y + other.h
            and self.y + self.h > other.y
        )

    def clip(self, other: "Rect") -> "Rect":
        x = max(self.x, other.x)
        y = max(self.y, other.y)
        w = min(self.x + self.w, other.x + other.w) - x
        h = min(self.y + self.h, other.y + other.h) - y
        return Rect(x, y, w, h)

    def draw(self, surface: pg.Surface, color: tuple[int, int, int], **kwargs) -> None:
        pg.draw.rect(surface, color, self.to_pygame(), width=1, **kwargs)

    def to_pygame(self) -> pg.Rect:
        return pg.Rect(self.x, self.y, self.w, self.h)

    @staticmethod
    def from_pygame(rect: pg.Rect) -> "Rect":
        return Rect(rect.x, rect.y, rect.w, rect.h)

    @overload
    def move(self, x: Number, y: Number) -> "Rect":
        ...

    @overload
    def move(self, x: Vector2D, y: None = None) -> "Rect":
        ...

    def move(self, x, y=None):
        if isinstance(x, Vector2D):
            x, y = x
        x = self.x + x
        y = self.y + y  # type: ignore
        return Rect(x, y, self.w, self.h)

    def __repr__(self):
        return f"<Rect {self.x}, {self.y}, {self.w}, {self.h}>"
