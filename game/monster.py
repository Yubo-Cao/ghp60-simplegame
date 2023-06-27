from .interfaces import *
from .physics import *
from .utils import *
from .wall import Wall


class Monster(PlayInstance):
    def __init__(self):
        self.sprite = load_im("monster.png")
        self.rb = RigidBodyRect(Rect.from_pygame(self.sprite.get_rect()), mass=1)
        self.rb.velocity = Vector2D(random.randint(-100, 100), random.randint(-10, 10))
        self.dt = 0

    def get_rect(self) -> Rect:
        return self.rb.get_rect()

    def get_velocity(self) -> "Vector2D":
        return self.rb.get_velocity()

    def collide(self, other: "Colliable") -> bool:
        return self.rb.collide(other)

    def get_callbacks(self) -> list[tuple[CollisionCallback, type["Colliable"]]]:
        return [(self.wall_collide, Wall)]

    def render(self, surface: pg.Surface) -> None:
        surface.blit(self.sprite, self.get_rect().to_pygame())
        self.rb.render(surface)

    def update(self, dt: float) -> None:
        self.rb.update(dt)
        self.dt = dt

    def wall_collide(self, collision: Collision) -> None:
        handle_collision(collision, self.rb, self.dt)
