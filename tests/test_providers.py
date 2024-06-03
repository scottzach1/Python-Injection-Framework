from pif import providers


def test_override_standard_shallow():
    """
    Testing basic override logic for providers.
    """
    provide_a = providers.Factory[str](lambda: "a")
    provide_b = providers.Factory[str](lambda: "b")
    assert provide_a() == "a"
    assert provide_b() == "b"

    provide_a.override(provide_b)
    assert provide_a() == "b"
    assert provide_b() == "b"

    provide_a.override(None)
    assert provide_a() == "a"
    assert provide_b() == "b"

    provide_b.override(provide_a)
    assert provide_a() == "a"
    assert provide_b() == "a"

    provide_b.override(None)
    assert provide_a() == "a"
    assert provide_b() == "b"


def test_override_contextmanager_shallow():
    """
    Testing basic override logic for providers with contextmanager.
    """
    provide_a = providers.Factory[str](lambda: "a")
    provide_b = providers.Factory[str](lambda: "b")

    assert provide_a() == "a"
    assert provide_b() == "b"

    with provide_a.override(provide_b):
        assert provide_a() == "b"
        assert provide_b() == "b"

    assert provide_a() == "a"
    assert provide_b() == "b"

    with provide_b.override(provide_a):
        assert provide_a() == "a"
        assert provide_b() == "a"


def test_override_standard_nested():
    """
    Testing nested override logic for providers.
    """
    provide_a = providers.Factory[str](lambda: "a")
    provide_b = providers.Factory[str](lambda: "b")
    provide_c = providers.Factory[str](lambda: "c")

    assert provide_a() == "a"
    assert provide_b() == "b"
    assert provide_c() == "c"

    provide_a.override(provide_b)
    provide_b.override(provide_c)

    assert provide_a() == "c"
    assert provide_b() == "c"
    assert provide_c() == "c"

    provide_b.override(None)
    assert provide_a() == "b"
    assert provide_b() == "b"
    assert provide_c() == "c"

    provide_a.override(None)
    assert provide_a() == "a"
    assert provide_b() == "b"
    assert provide_c() == "c"


def test_override_contextmanager_nested():
    """
    Testing nested override logic for providers with contextmanager.
    """
    provide_a = providers.Factory[str](lambda: "a")
    provide_b = providers.Factory[str](lambda: "b")
    provide_c = providers.Factory[str](lambda: "c")

    assert provide_a() == "a"
    assert provide_b() == "b"
    assert provide_c() == "c"

    with provide_a.override(provide_b):
        assert provide_a() == "b"
        assert provide_b() == "b"
        assert provide_c() == "c"

        with provide_b.override(provide_c):
            assert provide_a() == "c"
            assert provide_b() == "c"
            assert provide_c() == "c"

        assert provide_a() == "b"
        assert provide_b() == "b"
        assert provide_c() == "c"

    assert provide_a() == "a"
    assert provide_b() == "b"
    assert provide_c() == "c"
