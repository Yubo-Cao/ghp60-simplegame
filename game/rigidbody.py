import pygame as pg
from .interfaces import Updatable, Renderable, Colliable

Vec = tuple[float, float]


class RigidBody(Updatable):
    GRAVITY_CONSTANT = 9.81
    ACCELERATION_DECAY = 0.05

    def __init__(self, mass: float, decaying: bool = True, gravity: bool = True):
        self.mass = mass
        self.acceleration: Vec = (0, 0)
        self.velocity: Vec = (0, 0)
        self.position: Vec = (0, 0)
        self.decaying = decaying
        self.gravity = gravity

    def apply_force(self, force: Vec):
        self.acceleration = (
            self.acceleration[0] + force[0] / self.mass,
            self.acceleration[1] + force[1] / self.mass,
        )

    def update(self, dt: float):
        self.position = (
            self.position[0] + self.velocity[0] * dt,
            self.position[1] + self.velocity[1] * dt,
        )
        self.velocity = (
            self.velocity[0] + self.acceleration[0] * dt,
            self.velocity[1] + self.acceleration[1] * dt,
        )
        if self.decaying:
            self.acceleration = (
                self.acceleration[0] * (1 - self.ACCELERATION_DECAY),
                self.acceleration[1] * (1 - self.ACCELERATION_DECAY),
            )
        if self.gravity:
            self.apply_force((0, self.GRAVITY_CONSTANT * self.mass))


class RigidBodyRect(RigidBody, Renderable, Colliable):
    def __init__(self, rect: pg.Rect, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rect = rect

    def render(self, surface: pg.Surface):
        pg.draw.rect(surface, (255, 0, 0), self.rect)

    def update(self, dt: float):
        super().update(dt)
        # sync rect
        self.x = self.position[0]
        self.y = self.position[1]

    def collide(self, other: "Colliable") -> bool:
        return self.rect.colliderect(other.get_rect())

    def get_rect(self) -> pg.Rect:
        return self.rect

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = round(value)

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = round(value)
