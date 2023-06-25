import random
from collections.abc import Callable
from logging import getLogger
from typing import TypeVar

import pygame as pg

from .burger import LAYERS
from .command import RemoveCallbackCMD, RemoveInstanceCMD, commands, AddInstanceCMD
from .constants import FPS, HEIGHT, WIDTH
from .interfaces import CollisionHandler, PlayInstance, RenderHandler, UpdateHandler, Updatable, Renderable, Colliable
from .monster import Monster
from .player import Player
from .utils import Vector2D, make_rect
from .wall import Wall

T = TypeVar("T", bound=PlayInstance)
log = getLogger(__name__)


class Game:
    BACKGROUND_COLOR = (255, 255, 255)
    BURGER_LAYER_TICKS = 128
    MONSTER_TICKS = 300
    GAME_TIME = 60 * 60
    GRID_SIZE = 48

    def __init__(self, surface: pg.Surface, end_game: Callable[[str, int, str], None]):
        self.surface = surface
        self.collisions = CollisionHandler()
        self.renders = RenderHandler()
        self.updates = UpdateHandler()
        self.end_game = end_game

        self.clock = pg.time.Clock()
        self.walls: list[Wall] = []
        self.__init_scene()
        self.tick = 0

    def loop(self):
        while True:
            dt = self.clock.tick(FPS) / 1000
            self.tick += 1
            self.surface.fill(self.BACKGROUND_COLOR)
            self.__update_state(dt)
            self.__spawn_burger()
            self.__spawn_monster()
            self.__handle_cmd()
            self.__render_player_status()
            self.__handle_end_game()
            pg.display.flip()

    def __enter__(self):
        self.clock = pg.time.Clock()
        self.walls = []
        self.__init_scene()
        self.tick = 0
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        ...

    def __handle_end_game(self):
        if self.tick >= self.GAME_TIME:
            if self.player.score >= 100:
                self.end_game("You win!", self.player.score, "You got 100 points!")
            elif self.player.score == 0:
                self.end_game("You lose!", self.player.score, "You scored nothing!")
            else:
                self.end_game("You lose!", self.player.score, "Be better next time!")
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                pg.quit()
        if self.player.health <= 0:
            self.end_game("You lose!", self.player.score, "You died!")

    def __render_player_status(self):
        self.__put_text(f"Score: {self.player.score}", Vector2D(Game.GRID_SIZE + 16, 0))
        self.__put_text(
            f"Health: {self.player.health}", Vector2D(Game.GRID_SIZE + 16, 32)
        )
        self.__put_text(
            f"Time: {self.GAME_TIME - self.tick}", Vector2D(Game.GRID_SIZE + 16, 64)
        )

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
                case AddInstanceCMD():
                    self.__add_instance(cmd.instance)
                case _:
                    raise ValueError(f"Unknown command {cmd}")
        commands.clear()

    def __spawn_burger(self):
        if self.tick % self.BURGER_LAYER_TICKS == 0:
            layer = random.choice(LAYERS)()
            layer.pos = Vector2D(random.randint(0, WIDTH), 0)
            self.__add_instance(layer)

    def __spawn_monster(self):
        if self.tick % self.MONSTER_TICKS == 0:
            monster = self.__add_instance(Monster())
            while True:
                x = random.randint(
                    Game.GRID_SIZE, WIDTH - Game.GRID_SIZE - monster.rb.rect.width
                )
                y = random.randint(0, HEIGHT)
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

    def __init_scene(self):
        self.player = self.__add_instance(Player())
        self.player.rb.position = Vector2D(WIDTH / 2, 0)
        self.bottom_wall = self.__wall(0, HEIGHT - Game.GRID_SIZE, WIDTH, 1024)
        self.left_wall = self.__wall(Game.GRID_SIZE - 1024, -1024, 1024, HEIGHT + 1024)
        self.right_wall = self.__wall(
            WIDTH - Game.GRID_SIZE, -1024, 1024, HEIGHT + 1024
        )
        self.top_wall = self.__wall(-256, -1024, WIDTH, 1024)
        self.__wall(
            Game.GRID_SIZE * 2, Game.GRID_SIZE * 5, Game.GRID_SIZE * 2, Game.GRID_SIZE
        ),
        self.__wall(
            Game.GRID_SIZE * 7, Game.GRID_SIZE * 2, Game.GRID_SIZE * 2, Game.GRID_SIZE
        ),
        self.__wall(
            Game.GRID_SIZE * 8, Game.GRID_SIZE * 8, Game.GRID_SIZE * 4, Game.GRID_SIZE
        ),
        self.__wall(
            Game.GRID_SIZE * 5, Game.GRID_SIZE * 10, Game.GRID_SIZE * 3, Game.GRID_SIZE
        ),

    def __wall(self, x, y, w, h):
        result = self.__add_instance(Wall(make_rect(x, y, w, h)))
        self.walls.append(result)
        return result

    def __add_instance(self, instance: T) -> T:
        if isinstance(instance, Colliable):
            self.collisions.add(instance)
            for cb, type in instance.get_callbacks():
                self.collisions.register(cb, instance, type)
        if isinstance(instance, Renderable):
            self.renders.add(instance)
        if isinstance(instance, Updatable):
            self.updates.add(instance)
        return instance

    def __remove_instance(self, instance: T) -> T:
        if isinstance(instance, Colliable):
            self.collisions.remove(instance)
            for cb, type in instance.get_callbacks():
                self.collisions.unregister(cb, instance, type)
        if isinstance(instance, Renderable):
            self.renders.remove(instance)
        if isinstance(instance, Updatable):
            self.updates.remove(instance)
        return instance