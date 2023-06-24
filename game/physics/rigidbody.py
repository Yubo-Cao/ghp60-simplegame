from typing import NamedTuple

import pygame as pg

from game.interfaces import Colliable, Renderable, Updatable

from game.utils.ds import Rect, Vector2D


class RigidBody(Updatable):
    GRAVITY_CONSTANT = 9.81
    ACCELERATION_DECAY = 0.05

    def __init__(self, mass: float, decaying: bool = True, gravity: bool = True):
        self.mass = mass
        self.acceleration: Vector2D = Vector2D(0, 0)
        self.velocity: Vector2D = Vector2D(0, 0)
        self.position: Vector2D = Vector2D(0, 0)
        self.decaying = decaying
        self.gravity = gravity

    def apply_force(self, force: Vector2D):
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
            self.apply_force(Vector2D(0, self.GRAVITY_CONSTANT * self.mass))

    def __repr__(self):
        return f"RigidBody({self.mass}, {self.decaying}, {self.gravity})"


class RigidBodyRect(RigidBody, Renderable, Colliable):
    def __init__(self, rect: Rect, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rect = rect
        self.pg_rect = self.rect.to_pygame()

    def render(self, surface: pg.Surface):
        pg.draw.rect(surface, (255, 0, 0), self.rect)

    def update(self, dt: float):
        super().update(dt)

    def collide(self, other: "Colliable") -> bool:
        return self.pg_rect.colliderect(other.get_rect())

    def get_rect(self) -> pg.Rect:
        return self.pg_rect

    def get_velocity(self) -> "Vector2D":
        return self.velocity

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.position = (value, self.position[1])
        self.pg_rect.x = round(value)

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.position = (self.position[0], value)
        self.pg_rect.y = round(value)

    def __repr__(self):
        return f"RigidBodyRect({self.rect}, {self.mass}g, {self.position}, {self.velocity}, {self.acceleration})"


class ContactResult(NamedTuple):
    point: Vector2D
    normal: Vector2D
    plane: Vector2D
    penetration_depth: float
    time_of_contact: float


def calculate_contact(
        a: Rect,
        b: Rect,
        v_a: Vector2D,
        v_b: Vector2D,
) -> ContactResult:
    try:
        t_x_enter = (b.left - a.right) / (v_a[0] - v_b[0])
        t_x_exit = (b.right - a.left) / (v_a[0] - v_b[0])
        t_y_enter = (b.top - a.bottom) / (v_a[1] - v_b[1])
        t_y_exit = (b.bottom - a.top) / (v_a[1] - v_b[1])
    except ZeroDivisionError:
        raise ValueError("No collision")

    t_contact = max(min(t_x_enter, t_x_exit), min(t_y_enter, t_y_exit))
    t_exit = min(max(t_x_enter, t_x_exit), max(t_y_enter, t_y_exit))

    if t_contact > t_exit or t_exit < 0:
        raise ValueError("No collision")

    penetration = min(
        a.right - b.left,
        b.right - a.left,
        a.bottom - b.top,
        b.bottom - a.top,
    )

    a = a.move(v_a * t_contact)
    b = b.move(v_b * t_contact)
    xs = sorted([a.left, a.right, b.left, b.right])[1:3]
    ys = sorted([a.top, a.bottom, b.top, b.bottom])[1:3]
    contact = Vector2D((xs[0] + xs[1]) / 2, (ys[0] + ys[1]) / 2)

    normal = Vector2D(
        1 if contact[0] == a.left else -1 if contact[0] == a.right else 0,
        1 if contact[1] == a.top else -1 if contact[1] == a.bottom else 0,
    )
    plane = Vector2D(
        -normal[1],
        normal[0],
    )

    return ContactResult(contact, normal, plane, penetration, t_contact)
