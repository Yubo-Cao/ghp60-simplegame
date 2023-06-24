from .colliable import Colliable
from .renderable import Renderable
from .updatable import Updatable


class BurgerClass(Colliable, Renderable, Updatable):
    pass
