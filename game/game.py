import random
from logging import getLogger
from typing import TypeVar

import pygame as pg

from .burger import LAYERS
from .command import RemoveInstanceCMD, commands, RemoveCallbackCMD
from .interfaces import CollisionHandler, PlayInstance, RenderHandler, UpdateHandler
from .monster import Monster
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
    MONSTER_TICKS = 300
    GAME_TIME = 60 * 60
    GRID_SIZE = 48

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
        self.__update_state(dt)
        self.tick += 1
        self.__spawn_burger()
        self.__spawn_monter()
        self.__handle_cmd()

        self.__put_text(f"Score: {self.player.score}", Vector2D(Game.GRID_SIZE + 16, 0))
        self.__put_text(f"Health: {self.player.health}", Vector2D(Game.GRID_SIZE + 16, 32))
        self.__put_text(f"Time: {self.GAME_TIME - self.tick}", Vector2D(Game.GRID_SIZE + 16, 64))

        pg.display.flip()

    def __put_text(self, text: str, pos: Vector2D, size: int = 32) -> None:
        font = pg.font.SysFont("Cascadia Code", size)
        self.surface.blit(font.render(text, True, (0, 0, 0)), (pos.x, pos.y))

    def __update_state(self, dt):
        self.updates.update(dt)
        self.collisions.update(dt)
        self.renders.render(self.surface)

    def __handle_cmd(self):
        for cmd in commands:
            match cmd:
                case RemoveInstanceCMD():
                    self.__remove_instance(cmd.instance)
                case RemoveCallbackCMD():
                    self.collisions.unregister(cmd.callback, cmd.instance, cmd.type)
                case _:
                    raise ValueError(f"Unknown command {cmd}")
        commands.clear()

    def __spawn_burger(self):
        if self.tick % self.BURGER_LAYER_TICKS == 0:
            layer = random.choice(LAYERS)()
            layer.pos = Vector2D(random.randint(0, Game.WIDTH), 0)
            self.__add_instance(layer)

    def __spawn_monter(self):
        if self.tick % self.MONSTER_TICKS == 0:
            monster = self.__add_instance(Monster())
            while True:
                x = random.randint(Game.GRID_SIZE, Game.WIDTH - Game.GRID_SIZE - monster.rb.rect.width)
                y = random.randint(0, Game.HEIGHT)
                if any(
                        wall.get_rect().collide(
                            make_rect(
                                x,
                                y,
                                monster.rb.rect.width,
                                monster.rb.rect.height,
                            )
                        )
                        for wall in self.walls
                ):
                    continue
                break
            monster.rb.position = Vector2D(x, y)
            self.__add_instance(monster)

    def __enter__(self):
        self.surface = pg.display.set_mode(self.SIZE)
        pg.display.set_caption(self.TITLE)
        pg.display.set_icon(load_im("icon.png"))
        self.clock = pg.time.Clock()
        self.walls = []
        self.__init_scene()
        self.tick = 0
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pg.quit()

    def __init_scene(self):
        self.player = self.__add_instance(Player())
        self.player.rb.position = Vector2D(Game.WIDTH / 2, 0)
        self.bottom_wall = self.__wall(0, Game.HEIGHT - Game.GRID_SIZE, Game.WIDTH, 1024)
        self.left_wall = self.__wall(Game.GRID_SIZE - 1024, -1024, 1024, Game.HEIGHT + 1024)
        self.right_wall = self.__wall(Game.WIDTH - Game.GRID_SIZE, -1024, 1024, Game.HEIGHT + 1024)
        self.top_wall = self.__wall(-256, -1024, Game.WIDTH, 1024)
        self.__wall(Game.GRID_SIZE * 2, Game.GRID_SIZE * 5, Game.GRID_SIZE * 2, Game.GRID_SIZE),
        self.__wall(Game.GRID_SIZE * 7, Game.GRID_SIZE * 2, Game.GRID_SIZE * 2, Game.GRID_SIZE),
        self.__wall(Game.GRID_SIZE * 8, Game.GRID_SIZE * 8, Game.GRID_SIZE * 4, Game.GRID_SIZE),
        self.__wall(Game.GRID_SIZE * 5, Game.GRID_SIZE * 10, Game.GRID_SIZE * 3, Game.GRID_SIZE),

    def __wall(self, x, y, w, h):
        result = self.__add_instance(Wall(make_rect(x, y, w, h)))
        self.walls.append(result)
        return result

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
