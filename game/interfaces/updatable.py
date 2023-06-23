from typing import Protocol


class Updatable(Protocol):
    def update(self, dt: float) -> None:
        ...


class UpdateHandler(Updatable):
    def __init__(self):
        self.updatables: list[Updatable] = []

    def add(self, updatable: Updatable):
        self.updatables.append(updatable)

    def remove(self, updatable: Updatable):
        self.updatables.remove(updatable)

    def update(self, dt: float):
        for updatable in self.updatables:
            updatable.update(dt)
