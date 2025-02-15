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
from collections.abc import Callable
from typing import TypeVar

from scottzach1.pif.providers.provider import Provider
from scottzach1.pif.providers.util import intercept_args

__all__ = ("Factory",)

T = TypeVar("T")


class Factory(Provider):
    """
    Generate a new instance every call.
    """

    __slots__ = ("_func", "_depends")

    def __init__(self, func: Callable[..., T], *args, **kwargs):
        self._func = functools.partial(intercept_args(func), *args, **kwargs)

    def _evaluate(self) -> T:
        return self._func()
