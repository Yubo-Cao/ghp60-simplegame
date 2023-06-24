from enum import Enum

import pygame as pg


class HAlign(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class VAlign(Enum):
    TOP = 0
    CENTER = 1
    BOTTOM = 2


def text(
    surface: pg.Surface,
    text: str,
    pos: tuple[float, float],
    size: int = 24,
    color: tuple[int, int, int] = (255, 255, 255),
    halign: HAlign = HAlign.LEFT,
    valign: VAlign = VAlign.TOP,
    bold: bool = False,
):
    font = pg.font.SysFont("FiraCode NF", size, bold=bold)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    x, y = pos
    if halign == HAlign.CENTER:
        x -= rect.width // 2
    elif halign == HAlign.RIGHT:
        x -= rect.width
    if valign == VAlign.CENTER:
        y += rect.height // 2
    elif valign == VAlign.BOTTOM:
        y += rect.height
    surface.blit(rendered, (x, y))


def rect(
    surface: pg.Surface,
    x: float,
    y: float,
    w: float,
    h: float,
    color: tuple[int, int, int] = (255, 255, 255),
    thickness: int = 1,
):
    pg.draw.rect(
        surface,
        color,
        (int(x), int(y), int(w), int(h)),
        thickness,
    )
