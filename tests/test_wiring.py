import inspect
from unittest.mock import MagicMock

from pif import providers, wiring

provider = providers.Singleton[str](lambda: "hello")


def my_func(a: str = provider):
    """
    Our dummy method to test wiring for the module.
    """
    return a


def test_patch_kwarg():
    """
    Test the very rudimentary wiring logic for a module.
    """
    sig_before = inspect.signature(my_func)
    doc_before = my_func.__doc__
    assert provider == my_func()
    assert not wiring.is_patched(my_func)

    wiring.wire([__name__])
    sig_wired = inspect.signature(my_func)
    doc_wired = my_func.__doc__
    assert my_func() == "hello"
    assert sig_before == sig_wired
    assert doc_before == doc_wired
    assert wiring.is_patched(my_func)

    wiring.unwire([__name__])
    sig_unwired = inspect.signature(my_func)
    doc_unwired = my_func.__doc__
    assert provider == my_func()
    assert not wiring.is_patched(my_func)
    assert sig_before == sig_unwired
    assert doc_before == doc_unwired


def test_patch_lazy():
    """
    Test that our wiring implementation lazily evaluates providers.
    """
    mock = MagicMock()

    def func(v=None):
        return v

    assert not mock.call_count
    patched = wiring.patch_args_decorator(func, {"v": mock})
    assert not mock.call_count

    assert func() is None
    assert not mock.call_count
    assert isinstance(patched(), MagicMock)
    assert mock.call_count == 1
    assert isinstance(patched(), MagicMock)
    assert mock.call_count == 2
