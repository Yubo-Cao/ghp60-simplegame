from abc import ABC

from .colliable import Colliable
from .renderable import Renderable
from .updatable import Updatable


class PlayInstance(ABC, Colliable, Renderable, Updatable):
    pass
