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
from typing import Generic, TypeVar

__all__ = ("Provider", "Override")

T = TypeVar("T")
U = TypeVar("U")


class Provider(abc.ABC, Generic[T]):
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

    def override(self, provider: Provider[U] | None) -> Override[Provider[U] | None]:
        """
        Override the current providers value with another provider.
        """
        return Override(self, provider)

    def override_existing(self, value: U) -> Override[Provider[U]]:
        """
        Override the current provider with an existing singleton.
        """
        from pif.providers.existing_singleton import ExistingSingleton

        return self.override(ExistingSingleton(value))


class Override(Generic[T]):
    """
    A context manager to implement overrides for providers.
    """

    __slots__ = ("_base", "_override", "_before")

    def __init__(self, base: Provider, override: Provider[T] | None = None):
        # noinspection PyProtectedMember
        self._before = base._override
        self._base = base
        self._override = override
        base._override = override

    def __enter__(self) -> Override[T]:
        yield self

    def disable(self) -> None:
        """
        Disable the currently active override.
        """
        self._base._override = self._before

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disable()
