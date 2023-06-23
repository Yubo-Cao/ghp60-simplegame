from abc import abstractmethod
from typing import Any, Generic, Protocol, TypeVar


class Observer(Protocol):
    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None:
        pass


class Observable(Protocol):
    def add_observer(self, observer: Observer) -> None:
        pass

    def remove_observer(self, observer: Observer) -> None:
        pass

    def notify_observers(self, *args: Any, **kwargs: Any) -> None:
        pass


T = TypeVar("T")


class ObservableDescriptor(Observable, Generic[T]):
    def __set_name__(self, owner, name: str) -> None:
        self.name = f"_observable_{name}"
        self.owner = owner
        self.observers: set[Observer] = set()

    def __get__(self, instance, owner) -> T:
        return getattr(instance, self.name)

    def __set__(self, instance, value: T) -> None:
        old_value = getattr(instance, self.name)
        setattr(instance, self.name, value)
        self.notify_observers(instance, old_value, value)

    def add_observer(self, observer: Observer) -> None:
        self.observers.add(observer)

    def remove_observer(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify_observers(self, *args: Any, **kwargs: Any) -> None:
        for observer in self.observers:
            observer.update(*args, **kwargs)
