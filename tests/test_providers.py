import pytest

from pif import exceptions, providers


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


def test_blank_provider():
    """
    Checking the blank provider raises a BlankProviderException when it hasn't been overridden.
    """
    provider = providers.BlankProvider()

    with pytest.raises(exceptions.BlankProviderException):
        provider()

    with provider.override_existing("some_value"):
        assert provider() == "some_value"

    with pytest.raises(exceptions.BlankProviderException):
        provider()


def test_existing_singleton():
    """
    Checking the existing singleton provider returns the exact same object.
    """
    obj_1 = object()
    obj_2 = object()

    provider = providers.ExistingSingleton(obj_1)

    assert obj_1 is not obj_2
    assert obj_1 is provider()
    assert obj_1 is provider()

    with provider.override_existing(obj_2):
        assert obj_2 is not obj_1
        assert obj_2 is provider()
        assert obj_2 is provider()

    assert obj_1 is not obj_2
    assert obj_1 is provider()
    assert obj_1 is provider()


def test_singleton():
    """
    Checking the singleton provider creates only once.
    """
    provider = providers.Singleton[dict](dict, a=1, b=2)

    dict_1 = provider()
    dict_2 = provider()

    with provider.override(providers.Singleton[dict](dict, a=1, b=2)):
        dict_alt = provider()

    dict_3 = provider()

    assert dict_1 == {"a": 1, "b": 2}
    assert dict_1 is not {"a": 1, "b": 2}
    assert dict_2 is dict_1
    assert dict_3 is dict_1

    assert dict_1 == dict_alt
    assert dict_1 is not dict_alt


def test_factory():
    """
    Checking the factory provider creates every single time.
    """
    provider = providers.Factory[dict](dict, a=1, b=2)

    dict_1 = provider()
    dict_2 = provider()

    with provider.override(providers.Factory[dict](dict, a=1, b=2)):
        dict_alt = provider()

    dict_3 = provider()

    assert dict_1 == {"a": 1, "b": 2}
    assert dict_1 is not {"a": 1, "b": 2}

    assert dict_2 == dict_1
    assert dict_2 is not dict_1

    assert dict_3 == dict_1
    assert dict_3 is not dict_1

    assert dict_alt == dict_1
    assert dict_alt is not dict_1
