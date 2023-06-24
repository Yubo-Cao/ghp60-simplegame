import random
from logging import getLogger
from typing import TypeVar

import pygame as pg

from .burger import LAYERS, Burger, BurgerLayer
from .command import RemoveInstanceCMD, commands, RemoveCallbackCMD
from .interfaces import CollisionHandler, PlayInstance, RenderHandler, UpdateHandler
from .player import Player
from .utils import Vector2D, load_im, make_rect
from .wall import Wall

T = TypeVar("T", bound=PlayInstance)
log = getLogger(__name__)


class Game:
    SIZE = WIDTH, HEIGHT = 1200, 800
    TITLE = "Catch the ball"
    FPS = 60
    BACKGROUND_COLOR = (255, 255, 255)
    BURGER_LAYER_TICKS = 128

    def __init__(self) -> None:
        self.collisions = CollisionHandler()
        self.renders = RenderHandler()
        self.updates = UpdateHandler()

        self.dt: int
        self.surface: pg.Surface
        self.clock: pg.time.Clock
        self.tick: int

    def loop(self):
        dt = self.clock.tick(self.FPS) / 1000  # deciseconds
        self.surface.fill(self.BACKGROUND_COLOR)
        self.updates.update(dt)
        self.collisions.update(dt)
        self.renders.render(self.surface)

        self.tick += 1
        if self.tick % self.BURGER_LAYER_TICKS == 0:
            layer = random.choice(LAYERS)()
            layer.pos = Vector2D(random.randint(0, Game.WIDTH), 0)
            self.__add_instance(layer)

        for cmd in commands:
            match cmd:
                case RemoveInstanceCMD():
                    self.__remove_instance(cmd.instance)
                case RemoveCallbackCMD():
                    self.collisions.unregister(cmd.callback, cmd.instance, cmd.type)
                case _:
                    raise ValueError(f"Unknown command {cmd}")
        commands.clear()

        pg.display.flip()

    def __enter__(self):
        self.surface = pg.display.set_mode(self.SIZE)
        pg.display.set_caption(self.TITLE)
        pg.display.set_icon(load_im("icon.png"))
        self.clock = pg.time.Clock()
        self.__init_scene()
        self.tick = 0
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pg.quit()

    def __init_scene(self):
        self.player = self.__add_instance(Player())
        self.player.rb.position = Vector2D(Game.WIDTH / 2, 0)
        self.bottom_wall = self.__wall(0, Game.HEIGHT - 64, Game.WIDTH, 1024)
        self.left_wall = self.__wall(64 - 1024, 0, 1024, Game.HEIGHT)
        self.right_wall = self.__wall(Game.WIDTH - 64, 0, 1024, Game.HEIGHT)
        self.platforms = [
            self.__wall(64 * 2, 64 * 5, 128, 64),
            self.__wall(64 * 7, 64 * 2, 128, 64),
            self.__wall(64 * 8, 64 * 8, 256, 64),
            self.__wall(64 * 5, 64 * 10, 128, 64),
        ]

    def __wall(self, x, y, w, h):
        return self.__add_instance(Wall(make_rect(x, y, w, h)))

    def __add_instance(self, instance: T) -> T:
        self.collisions.add(instance)
        self.renders.add(instance)
        self.updates.add(instance)
        for cb, type in instance.get_callbacks():
            self.collisions.register(cb, instance, type)
        return instance

    def __remove_instance(self, instance: T) -> T:
        self.collisions.remove(instance)
        self.renders.remove(instance)
        self.updates.remove(instance)
        for cb, type in instance.get_callbacks():
            self.collisions.unregister(cb, instance, type)
        return instance
