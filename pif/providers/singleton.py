#                  _   _                 _     _
#    ___  ___ ___ | |_| |_ ______ _  ___| |__ / |
#   / __|/ __/ _ \| __| __|_  / _` |/ __| '_ \| |
#   \__ \ (_| (_) | |_| |_ / / (_| | (__| | | | |
#   |___/\___\___/ \__|\__/___\__,_|\___|_| |_|_|
#
#        Zac Scott (github.com/scottzach1)
#
#  https://github.com/scottzach1/python-injector-framework

import functools
from typing import Callable

from pif.providers.provider import Provider

UNSET = object()


class Singleton[T](Provider):
    """
    Provide a singleton instance.
    """

    __slots__ = ("_func", "_func", "_result", "_depends")

    def __init__(self, func: Callable[[...], T], *args, **kwargs):
        self._func = functools.partial(func, *args, **kwargs)
        self._result = UNSET

    def _evaluate(self) -> T:
        if self._result is UNSET:
            self._result = self._func()
        return self._result
