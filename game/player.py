from enum import Enum

import pygame as pg

from .interfaces import Colliable, Collision, ObservableDescriptor, PlayInstance
from .physics import RigidBodyRect, Vector2D, calculate_contact
from .utils import load_im, Rect


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
        speed: float = 64,
    ) -> None:
        super().__init__()
        self.image = load_im("player.png", scale=48 / 2048)
        self.speed = speed
        self.state: Player.State = Player.State.WALK
        self.rb = RigidBodyRect(
            Rect.from_pygame(self.image.get_rect()),
            mass=16,
            decaying=True,
            gravity=True,
        )

    def update(self, dt: float):
        keys = pg.key.get_pressed()
        match self.state:
            case Player.State.WALK:
                self.__handle_move(keys)
                if keys[pg.K_SPACE] or keys[pg.K_UP]:
                    self.state = Player.State.JUMP
                    self.rb.apply_force(Vector2D(0, -self.speed * 10))
            case Player.State.JUMP:
                self.__handle_move(keys)
                if self.rb.velocity[1] > 0:
                    self.state = Player.State.DIVE
                if keys[pg.K_DOWN]:
                    self.state = Player.State.DIVE
                    self.rb.apply_force(Vector2D(0, self.speed * 10))
        self.rb.update(dt)

    def render(self, surface: pg.Surface):
        # TODO: have different sprite for each state
        surface.blit(self.image, self.rb.pg_rect)

    def wall_collide(self, collision: Collision):
        result = calculate_contact(
            self.rb.rect,
            collision.b.get_rect(),
            self.rb.velocity,
            collision.b.get_velocity(),
        )
        norm = result.plane
        self.rb.velocity = self.rb.velocity.reflect(norm) * 0.5
        self.rb.acceleration = self.rb.acceleration.reflect(norm) * 0.5
        new_pos = self.rb.position + result.normal * result.penetration_depth
        self.rb.position = new_pos

    def collide(self, other: "Colliable") -> bool:
        return self.rb.collide(other)

    def get_rect(self) -> pg.Rect:
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
