import inspect
from unittest.mock import MagicMock

from pif import providers, wiring


def provide(s: str) -> providers.Singleton[str]:
    return providers.Singleton[str](lambda: f"{s}_injected")


def my_func(a: str = provide("a")):
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
    assert isinstance(my_func(), providers.Singleton)
    assert not wiring.is_patched(my_func)

    wiring.wire([__name__])
    sig_wired = inspect.signature(my_func)
    doc_wired = my_func.__doc__
    assert my_func() == "a_injected"
    assert sig_before == sig_wired
    assert doc_before == doc_wired
    assert wiring.is_patched(my_func)

    wiring.unwire([__name__])
    sig_unwired = inspect.signature(my_func)
    doc_unwired = my_func.__doc__
    assert isinstance(my_func(), providers.Singleton)
    assert not wiring.is_patched(my_func)
    assert sig_before == sig_unwired
    assert doc_before == doc_unwired


def test_patch_lazy():
    """
    Test that our wiring implementation lazily evaluates providers.
    """
    mock = MagicMock()
    assert not mock.call_count

    @wiring.inject
    def func(v=providers.Singleton[MagicMock](lambda: mock)):
        return v()

    assert not mock.call_count
    assert isinstance(func(), MagicMock)
    assert mock.call_count == 1
    assert isinstance(func(), MagicMock)
    assert mock.call_count == 2


def test_patch_positional_only():
    """
    Test patching for POSITIONAL_ONLY arguments.
    """

    @wiring.inject
    def p1(a, b=provide("b"), c="c_default", /):
        return a, b, c

    assert p1(None) == (None, "b_injected", "c_default")
    assert p1(None, None) == (None, None, "c_default")

    @wiring.inject
    def p2(a, b=None, c=provide("c"), /):
        return a, b, c

    assert p2(None) == (None, None, "c_injected")
    assert p2(None, None) == (None, None, "c_injected")
    assert p2(None, None, "c_override") == (None, None, "c_override")


def test_patch_positional():
    """
    Test patching for POSITIONAL_OR_KEYWORD arguments.
    """

    @wiring.inject
    def p1(a, b=provide("b"), c="c_default"):
        return a, b, c

    assert p1(None) == (None, "b_injected", "c_default")
    assert p1(None, None) == (None, None, "c_default")
    assert p1(a=None) == (None, "b_injected", "c_default")
    assert p1(a=None, b=None) == (None, None, "c_default")

    @wiring.inject
    def p2(a, b=None, c=provide("c")):
        return a, b, c

    assert p2(None) == (None, None, "c_injected")
    assert p2(None, None) == (None, None, "c_injected")
    assert p2(None, None, "c_override") == (None, None, "c_override")
    assert p2(a=None) == (None, None, "c_injected")
    assert p2(a=None, b=None) == (None, None, "c_injected")
    assert p2(a=None, b=None, c="c_override") == (None, None, "c_override")


def test_patch_positional_or_keyword():
    """
    Test patching for VAR_POSITIONAL argument.
    """

    @wiring.inject
    def p1(a, b=provide("b"), *c, d="d_default", e=provide("e")):
        return a, b, *c, d, e

    assert p1("a") == ("a", "b_injected", "d_default", "e_injected")
    assert p1("a", "b") == ("a", "b", "d_default", "e_injected")
    assert p1("a", "b", "c1") == ("a", "b", "c1", "d_default", "e_injected")
    assert p1("a", "b", "c1", "c2") == ("a", "b", "c1", "c2", "d_default", "e_injected")
    assert p1("a", "b", "c1", "c2", d="d") == ("a", "b", "c1", "c2", "d", "e_injected")
    assert p1("a", "b", "c1", "c2", d="d", e="e") == ("a", "b", "c1", "c2", "d", "e")
