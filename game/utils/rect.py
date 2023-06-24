import math

import pygame as pg


def make_rect(x: float, y: float, w: float, h: float) -> pg.Rect:
    return pg.Rect(round(x), round(y), round(w), round(h))
