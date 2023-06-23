import math

import pygame as pg


def invert_vector(vec: tuple[float, float]) -> tuple[float, float]:
    return -vec[0], -vec[1]


def move_vector(
    a: pg.Rect,
    b: pg.Rect,
    vec: tuple[float, float],
) -> tuple[float, float]:
    intersect: pg.Rect = a.clip(b)
    if intersect.width == 0 or intersect.height == 0:
        return vec
    angle = math.atan2(vec[1], vec[0])
    x = math.cos(angle) * intersect.width
    y = math.sin(angle) * intersect.height
    return x, y
