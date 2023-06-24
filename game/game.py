from typing import TypeVar

import pygame as pg

from .interfaces import CollisionHandler, PlayInstance, RenderHandler, UpdateHandler
from .player import Player
from .utils import load_im, make_rect
from .wall import Wall

T = TypeVar("T", bound=PlayInstance)


class Game:
    SIZE = WIDTH, HEIGHT = 1200, 800
    TITLE = "Catch the ball"
    FPS = 60
    BACKGROUND_COLOR = (255, 255, 255)

    def __init__(self):
        self.collisions = CollisionHandler()
        self.renders = RenderHandler()
        self.updates = UpdateHandler()

        self.dt: int
        self.surface: pg.Surface
        self.clock: pg.time.Clock

    def loop(self):
        dt = self.clock.tick(self.FPS) / 1000  # deciseconds
        self.surface.fill(self.BACKGROUND_COLOR)
        self.updates.update(dt)
        self.collisions.update(dt)
        self.renders.render(self.surface)
        pg.display.flip()

    def __enter__(self):
        self.surface = pg.display.set_mode(self.SIZE)
        pg.display.set_caption(self.TITLE)
        pg.display.set_icon(load_im("icon.png"))
        self.clock = pg.time.Clock()
        self.__init_scene()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pg.quit()

    def __init_scene(self):
        self.player = self.__add_instance(Player())
        self.wall = self.__add_instance(
            Wall(make_rect(0, Game.HEIGHT - 64, Game.WIDTH, 64))
        )
        self.collisions.register(self.player.wall_collide, self.player, self.wall)

    def __add_instance(self, instance: T) -> T:
        self.collisions.add(instance)
        self.renders.add(instance)
        self.updates.add(instance)
        return instance

    def __remove_instance(self, instance: T) -> T:
        self.collisions.remove(instance)
        self.renders.remove(instance)
        self.updates.remove(instance)
        return instance
