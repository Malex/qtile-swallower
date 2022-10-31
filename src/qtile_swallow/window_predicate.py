from typing import Callable, Any

from libqtile.backend.base import WindowType


class WindowPredicate:
    """
    A Callable with id identification provided for simplicity.
    Its focus is to provide an easy way to remove a predicate from swallow rules,
    while also allowing for type annotations to be added to the __call__ signature.
    Any id can be provided, but it must be of hash-able type and with defined __eq__ method.
    Equality will be delegate to the identifier type
    """

    __slots__ = ("_func", "id")

    def __init__(self, identifier: Any,
                 func: Callable[[WindowType, WindowType], bool]):
        self._func = func
        self.id = identifier

    def __call__(self, window: WindowType, parent: WindowType) -> bool:
        """ Delegates call to provided base callable"""
        return self._func(window, parent)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other: 'WindowPredicate'):
        return self.id == other.id
