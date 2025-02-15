import functools

from pif.providers.provider import Provider


def intercept_args(func):
    """
    Intercepts the args and kwargs at runtime evaluating any Provider values.

    Kept separate to wiring.py to avoid circular imports.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(
            *(a() if isinstance(a, Provider) else a for a in args),
            **{k: v() if isinstance(v, Provider) else v for k, v in kwargs.items()},
        )

    return wrapper
