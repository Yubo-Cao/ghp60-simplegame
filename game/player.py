from enum import Enum

from . import pg
from .interfaces import Collision, ObservableDescriptor, PlayInstance
from .utils import invert_vector, load_im, move_vector


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    BOTTOM = 2
    TOP = 3


class Player(pg.sprite.Sprite, PlayInstance):
    score = ObservableDescriptor[int]()
    health = ObservableDescriptor[int]()

    def __init__(
        self,
        keymap=None,
        speed: float = 16,
        gravity: float = 1,
    ) -> None:
        super().__init__()
        if keymap is None:
            keymap = {
                pg.K_LEFT: Direction.LEFT,
                pg.K_RIGHT: Direction.RIGHT,
                pg.K_UP: Direction.TOP,
                pg.K_DOWN: Direction.BOTTOM,
            }
        self.image = load_im("player.png", scale=48 / 2048)
        self.rect: pg.Rect = self.image.get_rect()
        self.keymap = keymap
        self.speed = speed
        self.gravity = gravity
        self.x: float = 0
        self.y: float = 0
        self.velocity: tuple[float, float] = [0, 0]

    def update(self, dt: float):
        self.velocity = [0, 0]
        keys = pg.key.get_pressed()
        for key, direction in self.keymap.items():
            if keys[key]:
                self.move(direction)
        self.velocity = [self.velocity[0], self.velocity[1] + self.gravity]
        self.apply_velocity(dt)

    def apply_velocity(self, dt: float):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.__sync_rect()

    def move(self, direction: Direction):
        if direction == Direction.LEFT:
            self.velocity = (self.velocity[0] - self.speed, self.velocity[1])
        elif direction == Direction.RIGHT:
            self.velocity = (self.velocity[0] + self.speed, self.velocity[1])
        elif direction == Direction.TOP:
            self.velocity = (self.velocity[0], self.velocity[1] - self.speed)
        elif direction == Direction.BOTTOM:
            self.velocity = (self.velocity[0], self.velocity[1] + self.speed)

    def render(self, surface: pg.Surface):
        surface.blit(self.image, self.rect)

    def wall_collide(self, collison: Collision):
        vec = invert_vector(self.velocity)
        vec = move_vector(collison.a.get_rect(), collison.b.get_rect(), vec)
        self.x += vec[0]
        self.y += vec[1]
        self.__sync_rect()

    def __sync_rect(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
