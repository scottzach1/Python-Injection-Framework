import inspect

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
