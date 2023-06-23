from enum import Enum

import pygame as pg

from .interfaces import Collision, ObservableDescriptor, PlayInstance
from .utils import invert_vector, load_im, move_vector


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
            speed: float = 16,
            gravity: float = 1,
    ) -> None:
        super().__init__()
        self.image = load_im("player.png", scale=48 / 2048)
        self.rect: pg.Rect = self.image.get_rect()
        self.speed = speed
        self.gravity = gravity
        self.x: float = 0
        self.y: float = 0
        self.velocity: tuple[float, float] = [0, 0]
        self.state: Player.State = Player.State.WALK

    def update(self, dt: float):
        self.velocity = [0, 0]
        keys = pg.key.get_pressed()
        match self.state:
            case Player.State.WALK:
                self.__handle_move(keys)
                if keys[pg.K_SPACE]:
                    self.state = Player.State.JUMP
                    self.velocity = (self.velocity[0], self.velocity[1] - 32)
            case Player.State.JUMP:
                self.__handle_move(keys)

        # apply gravity
        self.velocity = [self.velocity[0], self.velocity[1] + self.gravity]
        self.__apply_velocity(dt)

    def __handle_move(self, keys):
        if keys[pg.K_LEFT]:
            self.__move(Direction.LEFT)
        if keys[pg.K_RIGHT]:
            self.__move(Direction.RIGHT)

    def __apply_velocity(self, dt: float):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.__sync_rect()

    def __move(self, direction: Direction):
        if direction == Direction.LEFT:
            self.velocity = (self.velocity[0] - self.speed, self.velocity[1])
        elif direction == Direction.RIGHT:
            self.velocity = (self.velocity[0] + self.speed, self.velocity[1])
        elif direction == Direction.TOP:
            self.velocity = (self.velocity[0], self.velocity[1] - self.speed)
        elif direction == Direction.BOTTOM:
            self.velocity = (self.velocity[0], self.velocity[1] + self.speed)

    def render(self, surface: pg.Surface):
        # TODO: have different sprite for each state
        surface.blit(self.image, self.rect)

    def wall_collide(self, collison: Collision):
        vec = invert_vector(self.velocity)
        vec = move_vector(collison.a.get_rect(), collison.b.get_rect(), vec)
        self.x += vec[0]
        self.y += vec[1]
        self.__sync_rect()

    def __sync_rect(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
