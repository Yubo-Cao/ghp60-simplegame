from enum import Enum

import pygame as pg

from .burger import Burger, BurgerLayer
from .interfaces import (
    Colliable,
    Collision,
    CollisionCallback,
    ObservableDescriptor,
    PlayInstance,
)
from .physics import RigidBodyRect, Vector2D, handle_collision
from .utils import Rect, load_im
from .wall import Wall
from .command import issue_command, RemoveInstanceCMD
from .monster import Monster


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    BOTTOM = 2
    TOP = 3


class Player(pg.sprite.Sprite, PlayInstance):
    score = ObservableDescriptor[int]()
    health = ObservableDescriptor[int]()

    # player state
    class State(Enum):
        WALK = 0
        JUMP = 1
        DIVE = 2

    def __init__(
        self,
        speed: float = 128,
    ) -> None:
        super().__init__()
        self.image = load_im("player.png")
        self.speed = speed
        self.state: Player.State = Player.State.WALK
        self.rb = RigidBodyRect(
            Rect.from_pygame(self.image.get_rect()),
            mass=8,
            decaying=True,
            gravity=True,
        )
        self.burger = Burger()

        self.health = 100
        self.score = 0

    def update(self, dt: float):
        keys = pg.key.get_pressed()
        match self.state:
            case Player.State.WALK:
                self.__handle_move(keys)
                if keys[pg.K_SPACE] or keys[pg.K_UP]:
                    self.state = Player.State.JUMP
                    self.rb.apply_force(Vector2D(0, -self.speed * self.rb.mass * 10))
            case Player.State.JUMP:
                self.__handle_move(keys)
                if self.rb.velocity[1] > 0:
                    self.state = Player.State.DIVE
                if keys[pg.K_DOWN]:
                    self.state = Player.State.DIVE
                    self.rb.apply_force(Vector2D(0, self.speed * self.rb.mass * 10))
            case Player.State.DIVE:
                self.__handle_move(keys)
        self.rb.update(dt)
        self.burger.move_to(
            self.rb.position
            + Vector2D((self.rb.rect.width - 48) / 2, self.rb.rect.height / 2)
        )

    def render(self, surface: pg.Surface):
        # TODO: have different sprite for each state
        self.rb.render(surface)
        surface.blit(self.image, self.rb.rect.to_pygame())

    def wall_collide(self, collision: Collision):
        result = handle_collision(collision, self.rb)
        if result.normal == Vector2D(0, 0):
            return
        if result.normal == Vector2D(0, -1):
            self.state = Player.State.WALK

    def layer_collide(self, collision: Collision):
        assert isinstance(collision.b, BurgerLayer)
        self.burger.add_layer(collision.b)
        self.score = len(self.burger.layers)

    def monster_collide(self, collision: Collision):
        assert isinstance(collision.b, Monster)
        self.health -= 10
        issue_command(RemoveInstanceCMD(collision.b))

    def get_callbacks(self) -> list[tuple[CollisionCallback, type["Colliable"]]]:
        return [
            (self.wall_collide, Wall),
            (self.layer_collide, BurgerLayer),
            (self.monster_collide, Monster),
        ]

    def collide(self, other: "Colliable") -> bool:
        return self.rb.collide(other)

    def get_rect(self) -> Rect:
        return self.rb.get_rect()

    def get_velocity(self) -> "Vector2D":
        return self.rb.velocity

    def __handle_move(self, keys):
        if keys[pg.K_LEFT]:
            self.__move(Direction.LEFT)
        if keys[pg.K_RIGHT]:
            self.__move(Direction.RIGHT)

    def __move(self, direction: Direction):
        if direction == Direction.LEFT:
            self.rb.apply_force(Vector2D(-self.speed, 0))
        elif direction == Direction.RIGHT:
            self.rb.apply_force(Vector2D(self.speed, 0))
        elif direction == Direction.TOP:
            self.rb.apply_force(Vector2D(0, -self.speed))
        elif direction == Direction.BOTTOM:
            self.rb.apply_force(Vector2D(0, self.speed))

    def __repr__(self):
        return f"Player({self.speed}, {self.state}, {self.rb})"
