from abc import ABC

import pygame as pg

from .command import RemoveInstanceCMD, issue_command
from .interfaces import Renderable, Updatable
from .utils import Number, Vector2D


class Particle(Renderable, Updatable, ABC):
    """Metaclass for all particles"""


class FadingParticle(Particle):
    def __init__(
        self,
        pos: Vector2D,
        vel: Vector2D,
        acc: Vector2D,
        color: tuple[int, int, int],
        size: int,
        lifetime: int,
        auto_remove: bool = True,
    ) -> None:
        self.pos = pos
        self.color = color
        self.size = size
        self.vel = vel
        self.acc = acc

        # specified in ticks
        self.age = 0
        self.lifetime = lifetime
        self.auto_remove = auto_remove

    def render(self, surface: pg.Surface) -> None:
        alpha = 255 - (self.age / self.lifetime) * 255
        size = self.size - (self.age / self.lifetime) * self.size
        pg.draw.circle(
            surface,
            self.color + (alpha,),
            (int(self.pos.x), int(self.pos.y)),
            size,
        )

    def update(self, dt: float) -> None:
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        self.age += 1
        if self.age >= self.lifetime and self.auto_remove:
            issue_command(RemoveInstanceCMD(self))


class ExplosionEffect(Particle):
    def __init__(
        self,
        pos: Vector2D,
        color: tuple[int, int, int],
        spread: int = 100,
        n: int = 100,
        lifetime: int = 200,
    ) -> None:
        self.pos = pos
        self.particles: list[FadingParticle] = [
            FadingParticle(
                pos,
                Vector2D[Number].random(),
                Vector2D[Number].random() * spread,
                color,
                2,
                lifetime,
                False,
            )
            for _ in range(n)
        ]

    def render(self, surface: pg.Surface) -> None:
        for particle in self.particles:
            particle.render(surface)

    def update(self, dt: float) -> None:
        for particle in self.particles:
            particle.update(dt)
        if all(particle.age >= particle.lifetime for particle in self.particles):
            issue_command(RemoveInstanceCMD(self))
