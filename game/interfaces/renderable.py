from typing import Protocol

import pygame as pg


class Renderable(Protocol):
    def render(self, surface: pg.Surface) -> None:
        ...


class RenderHandler(Renderable):
    def __init__(self):
        self.renderables: list[Renderable] = []

    def add(self, renderable: Renderable):
        self.renderables.append(renderable)

    def remove(self, renderable: Renderable):
        self.renderables.remove(renderable)

    def render(self, surface: pg.Surface):
        for renderable in self.renderables:
            renderable.render(surface)
