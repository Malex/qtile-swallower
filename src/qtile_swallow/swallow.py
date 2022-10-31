import psutil
from typing import Iterable, Callable

from libqtile import hook
from libqtile.utils import logger
from libqtile.backend import base

from ._conf import PredicateChecker as _PredicateChecker

_checker_instance = _PredicateChecker()


def add_swallow_rule(
        *func: Iterable[Callable[[base.WindowType, base.WindowType], bool]]):
    _checker_instance.add_predicates(*func)


def remove_swallow_rule(
        *func: Iterable[Callable[[base.WindowType, base.WindowType], bool]]):
    _checker_instance.remove_predicates(*func)


@hook.subscribe.client_new
def _swallow(window: base.WindowType):
    pid = window.get_net_wm_pid()
    ppid = psutil.Process(pid).ppid()
    cpids = {
        c.window.get_net_wm_pid(): wid
        for wid, c in window.qtile.windows_map.items()
    }
    for _ in range(5):
        if not ppid:
            return
        if ppid in cpids:
            parent = window.qtile.windows_map.get(cpids[ppid])
            if _checker_instance.check(window, parent):
                parent.minimized = True
                window.parent = parent
            return
        ppid = psutil.Process(ppid).ppid()


@hook.subscribe.client_killed
def _unswallow(window: base.WindowType):
    if hasattr(window, 'parent') and hasattr(window.parent, 'minimized'):
        window.parent.minimized = False
