from .colliable import Colliable
from .renderable import Renderable
from .updatable import Updatable


class PlayInstance(Colliable, Renderable, Updatable):
    pass
