from enum import Enum
from typing import Any, Callable, Iterable
from uuid import uuid4 as uuid

from libqtile.backend.base import WindowType
from libqtile.log_utils import logger


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
        if identifier is None:
            logger.error(
                f"No identifier was provided to Predicate object for function {func}"
            )

    def __call__(self, window: WindowType, parent: WindowType) -> bool:
        """ Delegates call to provided base callable"""
        return self._func(window, parent)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: 'WindowPredicate') -> bool:
        return self.id == other.id

    def __and__(self, other: 'WindowPredicate') -> 'WindowPredicate':
        return WindowPredicate(
            {self.id, other.id, 'AND'}, lambda child, parent: self.__call__(
                child, parent) and other.__call__(child, parent))

    def __or__(self, other: 'WindowPredicate') -> 'WindowPredicate':
        return WindowPredicate(
            {self.id, other.id, 'OR'}, lambda child, parent: self.__call__(
                child, parent) or other.__call__(child, parent))


_terminals = {
    "roxterm",
    "sakura",
    "hyper",
    "alacritty",
    "terminator",
    "termite",
    "gnome-terminal",
    "konsole",
    "xfce4-terminal",
    "lxterminal",
    "mate-terminal",
    "kitty",
    "yakuake",
    "tilda",
    "guake",
    "eterm",
    "st",
    "urxvt",
    "wezterm",
    "xterm",
    "qterminal",
}

_browsers = {
    "Falkon",
    "qutebrowser",
}


class Predicates(Enum):
    """
    Enumeration of standard predicates provided.
    TERMINAL_CHILD triggers when the window has a terminal emulator as a parent
    BROWSER triggers when the window is a browser
    ALL triggers always
    NONE never triggers and it's the default
    """
    TERMINAL_CHILD = WindowPredicate(
        uuid(), lambda child, parent: any(a in _terminals
                                          for a in parent.get_wm_class()))
    BROWSER = WindowPredicate(
        uuid(), lambda child, parent: any(a in _browsers
                                          for a in child.get_wm_class()))
    ALL = WindowPredicate(uuid(), lambda a, b: True)
    NONE = WindowPredicate(uuid(), lambda a, b: False)

    @classmethod
    def add_terminal(cls, *terms: Iterable[str]) -> None:
        """Extends the terminal list with inputs"""
        _terminals.update(terms)

    @classmethod
    def add_browser(cls, *browsers: Iterable[str]) -> None:
        """Extends the browsers list with inputs"""
        _browsers.update(browsers)
