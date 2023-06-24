from enum import Enum

import pygame as pg

from .burger import Burger, BurgerLayer
from .command import RemoveInstanceCMD, issue_command
from .interfaces import (
    Colliable,
    Collision,
    CollisionCallback,
    ObservableDescriptor,
    PlayInstance,
)
from .monster import Monster
from .physics import RigidBodyRect, Vector2D, handle_collision
from .utils import Rect, load_im
from .wall import Wall


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
        WALK_RIGHT = 0
        WALK_LEFT = 1
        JUMP = 2
        DIVE = 3

    def __init__(
        self,
        speed: float = 128,
    ) -> None:
        super().__init__()
        self.speed = speed
        self.image = load_im("catwalk-1.png")

        self.rb: RigidBodyRect
        self.__update_state(Player.State.WALK_LEFT)

        self.burger = Burger()
        self.health = 100
        self.score = 0

    def update(self, dt: float):
        keys = pg.key.get_pressed()

        match self.state:
            case Player.State.WALK_LEFT | Player.State.WALK_RIGHT:
                self.__handle_move(keys)
                if self.rb.velocity.x > 0:
                    self.__update_state(Player.State.WALK_RIGHT)
                elif self.rb.velocity.x < 0:
                    self.__update_state(Player.State.WALK_LEFT)
                if keys[pg.K_SPACE] or keys[pg.K_UP]:
                    self.__update_state(Player.State.JUMP)
                    self.rb.apply_force(Vector2D(0, -self.speed * self.rb.mass * 10))
            case Player.State.JUMP:
                self.__handle_move(keys)
                if self.rb.velocity[1] > 0:
                    self.__update_state(Player.State.DIVE)
                if keys[pg.K_DOWN]:
                    self.__update_state(Player.State.DIVE)
                    self.rb.apply_force(Vector2D(0, self.speed * self.rb.mass * 10))
            case Player.State.DIVE:
                self.__handle_move(keys)

        self.rb.update(dt)
        self.burger.move_to(
            self.rb.position
            + Vector2D((self.rb.rect.width - 48) / 2, self.rb.rect.height / 2)
        )

    def __update_state(self, state: State):
        if state == getattr(self, "state", None):
            return
        if state == Player.State.WALK_LEFT:
            self.image = load_im("catwalk-1.png")
        elif state == Player.State.WALK_RIGHT:
            self.image = load_im("catwalk-2.png")
        elif state == Player.State.JUMP:
            self.image = load_im("catjump.png")
        elif state == Player.State.DIVE:
            self.image = load_im("catfall.png")

        if getattr(self, "rb", None):
            self.rb.rect = Rect.from_pygame(self.image.get_rect())
        else:
            self.rb = RigidBodyRect(
                Rect.from_pygame(self.image.get_rect()),
                mass=8,
                decaying=True,
                gravity=True,
            )

        self.state = state

    def render(self, surface: pg.Surface):
        # TODO: have different sprite for each state
        self.rb.render(surface)
        surface.blit(self.image, self.rb.rect.to_pygame())

    def wall_collide(self, collision: Collision):
        result = handle_collision(collision, self.rb)
        if result.normal == Vector2D(0, 0):
            return
        if result.normal == Vector2D(0, -1):
            self.__update_state(Player.State.WALK_LEFT)

    def layer_collide(self, collision: Collision):
        assert isinstance(collision.b, BurgerLayer)
        self.burger.add_layer(collision.b)
        self.score = len(self.burger.layers) * 20

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
