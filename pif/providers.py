#                  _   _                 _     _
#    ___  ___ ___ | |_| |_ ______ _  ___| |__ / |
#   / __|/ __/ _ \| __| __|_  / _` |/ __| '_ \| |
#   \__ \ (_| (_) | |_| |_ / / (_| | (__| | | | |
#   |___/\___\___/ \__|\__/___\__,_|\___|_| |_|_|
#
#        Zac Scott (github.com/scottzach1)
#
#  https://github.com/scottzach1/python-injector-framework

from __future__ import annotations

import abc
import functools
from typing import Callable, Self


class Provider[T](abc.ABC):
    """
    Signposts something that can be injected.
    """

    _override: Provider | None = None

    def __call__(self, *args, **kwargs) -> T:
        """
        Evaluate the provider, will select override if present.
        """
        if self._override:
            return self._override()

        return self._evaluate()

    @abc.abstractmethod
    def _evaluate(self) -> T:
        """
        Define the behavior to evaluate the provided value.
        """
        return self()

    def override[U: Provider | None](self, provider: U) -> Override[U]:
        """
        Override the current providers value with another provider.
        """
        return Override(self, provider)


class Override[ProviderT: Provider]:
    """
    A context manager to implement overrides for providers.
    """

    __slots__ = ("_base", "_override", "_before")

    def __init__(self, base: Provider, override: ProviderT | None = None):
        # noinspection PyProtectedMember
        self._before = base._override
        self._base = base
        self._override = override
        base._override = override

    def __enter__(self) -> Self:
        yield self

    def disable(self) -> None:
        """
        Disable the currently active override.
        """
        self._base._override = self._before

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disable()


class ExistingSingleton[T](Provider):
    """
    Provide an existing object instance.
    """

    __slots__ = ("t",)

    def __init__(self, t: T):
        self.t = t

    def _evaluate(self) -> T:
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

    def _evaluate(self) -> T:
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

    def _evaluate(self) -> T:
        return self._func()
