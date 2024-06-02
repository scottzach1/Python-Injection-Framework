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
import importlib
import inspect
import types
from typing import Callable

from pif import providers


def patch_args_decorator[T: Callable](func: T, patched_kwargs: dict[str, providers.Provider]) -> T:
    """
    Get a decorated copy of `func` with patched arguments.

    TODO(scottzach1) - add support for positional kwargs.

    :param func: to decorate.
    :param patched_kwargs: the kwargs to patch.
    :return: the decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for keyword in patched_kwargs:
            if keyword not in kwargs:
                kwargs[keyword] = patched_kwargs[keyword]()

        return func(*args, **kwargs)

    wrapper._patched_func = func
    return wrapper


def is_patched(func: Callable | types.FunctionType) -> bool:
    """
    Checks if a function has been "patched" by the `patch_args_decorator`

    :param func: the function to check.
    :return: True if patched, False otherwise.
    """
    return hasattr(func, "_patched_func")


def patch_method[T: Callable | types.FunctionType](func: T) -> T:
    """
    Return a "patched" version of the method provided.

    If no values required patching, the provided function will be returned unchanged..

    :param func: to patch default values.
    :return: a "patched" version of the method provided.
    """
    patched_args = {}

    for name, value in inspect.signature(func).parameters.items():
        if value.kind == inspect.Parameter.POSITIONAL_ONLY:
            continue  # TODO(scottzach1) Add support for non keyword arguments.

        if isinstance(value.default, providers.Provider):
            patched_args[name] = value.default

    if patched_args:
        return patch_args_decorator(func, patched_args)

    return func


def unpatch_method[T: Callable | types.FunctionType](func: T) -> T:
    """
    Get an "unpatched" copy of a method.

    If the value was not patched, the provided function will be returned unchanged.

    :param func: the function to unpatch.
    :return: the unpatched provided function.
    """
    return getattr(func, "_patched_func", func)


def wire(modules: list[types.ModuleType | str]) -> None:
    """
    Patch all methods in the module containing `Provide` default arguments.

    :param modules: list of modules to wire.
    """
    for module in modules:
        if isinstance(module, str):
            module = importlib.import_module(module)

        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj):
                if obj is not (patched := patch_method(obj)):
                    setattr(module, name, patched)
            elif inspect.isclass(obj):
                for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                    if method is not (patched := patch_method(method)):
                        setattr(obj, method_name, patched)


def unwire(modules: list[types.ModuleType]) -> None:
    """
    Unpatch all methods in the module containing `Provide` default arguments.

    :param modules: list of modules to wire.
    """
    for module in modules:
        if isinstance(module, str):
            module = importlib.import_module(module)

        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj):
                if obj is not (unpatched := unpatch_method(obj)):
                    setattr(module, name, unpatched)
            elif inspect.isclass(obj):
                for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                    if method is not (unpatched := unpatch_method(method)):
                        setattr(obj, method_name, unpatched)
