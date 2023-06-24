import pygame as pg

from .interfaces import PlayInstance, Colliable, Renderable, Collision
from .physics import RigidBodyRect, handle_collision
from .utils import Rect, Vector2D, Number, DATA_DIR, load_im


class BurgerLayer(PlayInstance):
    def __init__(self, sprite: pg.Surface, name: str) -> None:
        self.sprite = sprite
        self.name = name

        self._pos = Vector2D[Number](0.0, 0.0)
        self.rect = Rect(
            self.pos.x,
            self.pos.y,
            sprite.get_width(),
            sprite.get_height(),
        )
        self.rb = RigidBodyRect(self.rect, gravity=True)

    @property
    def pos(self) -> Vector2D[Number]:
        return self._pos

    @pos.setter
    def pos(self, value: Vector2D[Number]) -> None:
        self._pos = value
        self.rect = Rect(
            value.x,
            value.y,
            self.sprite.get_width(),
            self.sprite.get_height(),
        )

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


LAYERS = [
    BurgerLayer(load_im(path), path.stem)
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
        self.layers.insert(0, layer)
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
            layer.pos = Vector2D[Number](x, y + h)
            h += layer.sprite.get_height()
