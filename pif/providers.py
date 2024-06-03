#                  _   _                 _     _
#    ___  ___ ___ | |_| |_ ______ _  ___| |__ / |
#   / __|/ __/ _ \| __| __|_  / _` |/ __| '_ \| |
#   \__ \ (_| (_) | |_| |_ / / (_| | (__| | | | |
#   |___/\___\___/ \__|\__/___\__,_|\___|_| |_|_|
#
#        Zac Scott (github.com/scottzach1)
#
#  https://github.com/scottzach1/python-injector-framework

import abc
import functools
from typing import Callable


class Provider[T](abc.ABC):
    """
    Signposts something that can be injected.
    """

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> T:
        """
        Evaluate the value to provide.
        """


class ExistingSingleton[T](Provider):
    """
    Provide an existing object instance.
    """

    __slots__ = ("t",)

    def __init__(self, t: T):
        self.t = t

    def __call__(self) -> T:
        return self.t


UNSET = object()


class Singleton[T](Provider):
    """
    Provide a singleton instance.
    """

    __slots__ = ("_func", "_func", "_result", "_depends")

    def __init__(self, func: Callable[[...], T], *args, **kwargs):
        self._func = functools.partial(func, *args, **kwargs)
        self._result = UNSET

    def __call__(self) -> T:
        if self._result is UNSET:
            self._result = self._func()
        return self._result


class Factory[T](Provider):
    """
    Generate a new instance every call.
    """

    __slots__ = ("_func", "_depends")

    def __init__(self, func: Callable[[...], T], *args, **kwargs):
        self._func = functools.partial(func, *args, **kwargs)

    def __call__(self) -> T:
        return self._func()
