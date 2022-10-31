__doc__ = """
    Private module to hold the checkers
"""
from typing import Callable, Iterable, Set
from libqtile.backend import base


class PredicateChecker:
    """ Aggregator for a list of predicates to be checked together """

    _predicates: Set[Callable[[base.WindowType, base.WindowType], bool]]

    def __init__(
        self,
        *predicates: Iterable[Callable[[base.WindowType, base.WindowType],
                                       bool]]):
        self._predicates = set()
        self._predicates.update(predicates)

    def check(self, window: base.WindowType, parent: base.WindowType) -> bool:
        """ Checks the window against the list of available predicates"""
        return any(p(window, parent) for p in self._predicates)

    def add_predicates(
        self,
        *predicates: Iterable[Callable[[base.WindowType, base.WindowType],
                                       bool]]
    ) -> None:
        """ Updates the list of predicates adding all the elements passed as inputs"""
        self._predicates.update(predicates)

    def remove_predicates(
        self,
        *predicates: Iterable[Callable[[base.WindowType, base.WindowType],
                                       bool]]
    ) -> None:
        """ Updates the list of predicates removing all the elements passed as inputs"""
        for p in predicates:
            self._predicates.discard(p)
