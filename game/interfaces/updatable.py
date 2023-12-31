from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class Updatable(Protocol):
    @abstractmethod
    def update(self, dt: float) -> None:
        ...


class UpdateHandler(Updatable):
    def __init__(self) -> None:
        self.updatables: list[Updatable] = []

    def add(self, updatable: Updatable):
        self.updatables.append(updatable)

    def remove(self, updatable: Updatable):
        self.updatables.remove(updatable)

    def update(self, dt: float):
        for updatable in self.updatables:
            updatable.update(dt)
