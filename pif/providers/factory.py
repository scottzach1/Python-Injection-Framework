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
from pif.wiring import intercept


class Factory[T](Provider):
    """
    Generate a new instance every call.
    """

    __slots__ = ("_func", "_depends")

    def __init__(self, func: Callable[[...], T], *args, **kwargs):
        self._func = functools.partial(intercept(func), *args, **kwargs)

    def _evaluate(self) -> T:
        return self._func()
